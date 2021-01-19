from gcmap import GCMapper, Gradient
import gzip, csv, sys, random, os
from datetime import datetime
import maidenhead as mh
import numpy as np

#grad = Gradient([(   0,   32,   32,   32),
#                 (   1,  255,  255,  255)])

grad = Gradient(((0, 64, 64, 64), (0.5, 64, 160, 255), (1, 255, 255, 255)))

def fixlon(x):
    return max(-179.999, min(179.999, x))

class RouteMap:
    def __init__(self):
        self.lons1 = []
        self.lats1 = []
        self.lons2 = []
        self.lats2 = []
        self.counts = []
        self.routes = set()
    def addroute(self, txgrid, rxgrid, snr):
        route = (txgrid,rxgrid)
        if txgrid != rxgrid and not route in self.routes:
            self.routes.add(route)
            rxloc = mh.to_location(rxgrid)
            txloc = mh.to_location(txgrid)
            if len(txloc) == 2 and len(rxloc) == 2:
                self.lats1.append(txloc[0])
                self.lons1.append(fixlon(txloc[1]))
                self.lats2.append(rxloc[0])
                self.lons2.append(fixlon(rxloc[1]))
                intens = max(0, snr + 40)
                self.counts.append(intens)
            #print(txgrid,rxgrid,txloc,rxloc)
    def draw(self, filename):
        if len(self.lons1) == len(self.lats1) == len(self.lons2) == len(self.lats2) and len(self.lons1) > 5:
            gcm = GCMapper(width=640, cols=grad, line_width=1.5)
            gcm.set_data(self.lons1, self.lats1, self.lons2, self.lats2, self.counts)
            img = gcm.draw()
            if os.fork() == 0:
                img.save(filename)
                sys.exit(0)


def drawmaps():
    maps = {}
    reader = csv.reader(sys.stdin)
    for row in reader:
        band = int(row[12])
        time = datetime.utcfromtimestamp(int(row[1]))
        rxgrid = row[3][0:4]
        txgrid = row[7][0:4]
        dbm = int(row[8])
        snr = int(row[4])
        #dist = int(row[10])
        key = (time.year,time.month,time.hour,band,dbm)
        map = maps.get(key)
        if not map:
            map = RouteMap()
            maps[key] = map
            print(key,snr)
        map.addroute(txgrid,rxgrid,snr)
        #if key[2] == 3:
        #    break
    return maps

allmaps = drawmaps()
for k,m in allmaps.items():
    pngfn = 'output/map-%04d-%02d-%02d-%d-%d.png' % k
    pngfn = pngfn.replace('--','-m')
    print (pngfn)
    try:
        m.draw(pngfn)
    except ValueError: # TODO???
        print(pngfn, sys.exc_info())
    except IndexError: # TODO???
        print(pngfn, sys.exc_info())
