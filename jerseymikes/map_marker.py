import webbrowser
import gmplot
from gmplot import GoogleMapPlotter as gmp
import urllib.request
import json
from credentials import API_KEY
import pandas as pd
from stores import locations, station

KSU_GOLD  = "#FFC425"
DARK_GOLD = '#B8860B'
KSU_BLACK = "#231F20"

extra_js = '''
function pinSymbol(color) {
	    return {
			path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z',
			fillColor: color,
			fillOpacity: 1,
			strokeColor: '#000',
			strokeWeight: 2,
			scale: 1,
			labelOrigin: new google.maps.Point(0, -28),
	    };
	}

'''

fn = 'output/atlanta.html'
gmap = gmp(33.8490, -84.3880, 10, extra=extra_js)

nodes =  locations+[station]
# route1 = [37, 9, 5, 11, 24, 10, 12, 13, 3, 26, 15, 16, 1, 19, 27, 36, 28, 32, 33, 6]
# route2 = [37, 0, 14, 20, 7, 4, 17, 31, 35, 34, 22, 21, 23, 18, 25, 8, 2, 29, 30]
route1 = [37, 9, 5, 11, 24, 4, 17, 31, 35, 34, 22, 21, 23, 18, 25, 8, 2, 26, 29, 30]
route2 = [37, 13, 12, 10, 7, 20, 3, 0, 14, 15, 16, 1, 19, 27, 36, 28, 32, 33, 6]
dj1 = [nodes[x] for x in route1]
dj2 = [nodes[x] for x in route2]


gmap.marker(station[0], station[1])

for i, (lat, lon) in enumerate(dj1[1:]):
    text = chr(ord('A') + i)
    gmap.marker(lat, lon, label='{text: "%s", color: "%s"}' % (text, KSU_BLACK) , icon='pinSymbol("%s")' % KSU_GOLD)

for i, (lat, lon) in enumerate(dj2[1:]):
    text = chr(ord('A') + i)
    gmap.marker(lat, lon, label='{text: "%s", color: "%s"}' % (text, KSU_GOLD) , icon='pinSymbol("%s")' % KSU_BLACK)

lats, lons = zip(*dj1)
gmap.plot(lats, lons, color=DARK_GOLD, ew=3)

lats, lons = zip(*dj2)
gmap.plot(lats, lons, color=KSU_BLACK, ew=3)

gmap.draw(fn)
webbrowser.open(fn)

