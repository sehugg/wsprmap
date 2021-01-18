from gcmap import GCMapper, Gradient
import gzip, csv, sys, random
from datetime import datetime
import maidenhead as mh
import numpy as np

filename = 'wsprspots-2020-12.csv.gz'

grad = Gradient([(   0,   32,   32,   32),
                 (   1,  255,  255,  255)])

def r():
    return random.random()*0.5

class RouteMap:
    def __init__(self):
        self.lons1 = []
        self.lats1 = []
        self.lons2 = []
        self.lats2 = []
        self.routes = set()
    def addroute(self, txgrid, rxgrid):
        route = (txgrid,rxgrid)
        if txgrid != rxgrid and not route in self.routes:
            self.routes.add(route)
            rxloc = mh.to_location(rxgrid)
            txloc = mh.to_location(txgrid)
            if len(txloc) == 2 and len(rxloc) == 2:
                self.lats1.append(txloc[0]+r())
                self.lons1.append(txloc[1]+r())
                self.lats2.append(rxloc[0]+r())
                self.lons2.append(rxloc[1]+r())
            #print(txgrid,rxgrid,txloc,rxloc)
    def draw(self, filename):
        if len(self.lons1) == len(self.lats1) == len(self.lons2) == len(self.lats2) and len(self.lons1) > 5:
            gcm = GCMapper(width=640, cols=grad, line_width=1)
            gcm.set_data(self.lons1, self.lats1, self.lons2, self.lats2)
            img = gcm.draw()
            img.save(filename)


def drawmaps():
    maps = {}
    with gzip.open(filename, mode='rt') as f:
        reader = csv.reader(f)
        for row in reader:
            band = int(row[12])
            time = datetime.utcfromtimestamp(int(row[1]))
            rxgrid = row[3][0:4]
            txgrid = row[7][0:4]
            dbm = int(row[8])
            #snr = int(row[4])
            #dist = int(row[10])
            key = (time.year,time.month,time.hour,band,dbm)
            map = maps.get(key)
            if not map:
                map = RouteMap()
                maps[key] = map
                print(key)
            map.addroute(txgrid,rxgrid)
            #if key[2] == 12:
            #    break
    return maps

allmaps = drawmaps()
for k,m in allmaps.items():
    print (k,m)
    pngfn = 'output/map-%d-%d-%d-%d-%d.png' % k
    try:
        m.draw(pngfn)
    except ValueError: # TODO???
        print(pngfn, sys.exc_info())
    except IndexError: # TODO???
        print(pngfn, sys.exc_info())
