from gcmap import GCMapper
import gzip, csv
from datetime import datetime
import maidenhead as mh
import numpy as np

filename = 'wsprspots-2020-12.csv.gz'

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
            self.lats1.append(txloc[0])
            self.lons1.append(txloc[1])
            self.lats2.append(rxloc[0])
            self.lons2.append(rxloc[1])
            #print(txgrid,rxgrid,txloc,rxloc)
    def draw(self, filename):
        gcm = GCMapper()
        gcm.set_data(self.lons1, self.lats1, self.lons2, self.lats2)
        img = gcm.draw()
        img.save(filename)


def drawmap(freq):
    maps = {}
    with gzip.open(filename, mode='rt') as f:
        reader = csv.reader(f)
        for row in reader:
            band = int(row[12])
            if band == freq:
                time = datetime.utcfromtimestamp(int(row[1]))
                rxgrid = row[3][0:4]
                txgrid = row[7][0:4]
                dbm = int(row[8])
                key = (time.month,time.hour,band,dbm)
                map = maps.get(key)
                if not map:
                    map = RouteMap()
                    maps[key] = map
                    print(key)
                    #snr = int(row[4])
                    #dist = int(row[10])
                map.addroute(txgrid,rxgrid)
    return maps

allmaps = drawmap(10)
for k,m in allmaps.items():
    print (k,m)
    fn = 'output/map-%d-%d-%d-%d.png' % k
    m.draw(fn)
#img = gcm.draw()
#img.save('output.png')
