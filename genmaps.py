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
        self.points = []
        self.routes = set()
    def addroute(self, txgrid, rxgrid, snr):
        route = (txgrid,rxgrid)
        if txgrid != rxgrid and not route in self.routes:
            self.routes.add(route)
            rxloc = mh.to_location(rxgrid)
            txloc = mh.to_location(txgrid)
            if len(txloc) == 2 and len(rxloc) == 2:
                rec = (txloc[0], txloc[1], rxloc[0], rxloc[1], max(0, snr+40))
                self.points.append(np.array(rec, np.int16))
            #print(txgrid,rxgrid,txloc,rxloc)
    def draw(self, filename):
        if len(self.points) > 5:
            lats1 = [r[0] for r in self.points]
            lons1 = [fixlon(r[1]) for r in self.points]
            lats2 = [r[2] for r in self.points]
            lons2 = [fixlon(r[3]) for r in self.points]
            counts = [r[4] for r in self.points]
            gcm = GCMapper(width=640, cols=grad, line_width=1.5)
            gcm.set_data(lons1, lats1, lons2, lats2, counts)
            img = gcm.draw()
            img.save(filename)


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
        if key[2] == 3:
            break
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
