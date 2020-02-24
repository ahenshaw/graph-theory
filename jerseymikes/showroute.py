import numpy as np
from stores import locations, station
from credentials import API_KEY
import urllib.request
import json
import htmlparser

def get_polys(route):
    nodes = locations + [station]
    points = [nodes[x] for x in route]
    URL = 'https://maps.googleapis.com/maps/api/directions/json?key={0}&origin={1}&destination={2}&waypoints={3}'

    waypoints = '|'.join([('%s,%s' % tuple(x)) for x in points[1:-1]])
    start ='%s,%s' % tuple(points[0])
    end   ='%s,%s' % tuple(points[-1])
    url = URL.format(API_KEY, start, end, waypoints)

    html = urllib.request.urlopen(url).read()
    return htmlparser.path(html)

if __name__ == '__main__':
    #route = [37, 9, 5, 11, 24, 4, 17, 31, 35, 34, 22, 21, 23, 18, 25, 8, 2, 26, 29, 30]
    route = [37, 13, 12, 10, 7, 20, 3, 0, 14, 15, 16, 1, 19, 27, 36, 28, 32, 33, 6]
    encoded = json.dumps(get_polys(route)).replace(', ', ',\n')
    print(encoded)


