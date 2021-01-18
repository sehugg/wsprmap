from gcmap import GCMapper, Gradient
import gzip, csv, sys, random
from datetime import datetime
import maidenhead as mh
import numpy as np

def rnd(a,b):
    return random.random() * (b-a) + a

while 1:
    lats1 = [rnd(-89,89)]
    lons1 = [rnd(-179.99,179.99)]
    lats2 = [rnd(-89,89)]
    lons2 = [rnd(-179.99,179.99)]

    gcm = GCMapper(width=640, line_width=1)
    print (lats1,lons1,lats2,lons2)
    gcm.set_data(lons1, lats1, lons2, lats2)
    img = gcm.draw()
    #img.save('/tmp/test.png')
