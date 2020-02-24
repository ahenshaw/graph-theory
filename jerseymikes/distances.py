import urllib.request
import json
from credentials import API_KEY
from stores import locations, station

BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=%s&' % API_KEY

def lookup(locations):
    grid = []
    for i in range(len(locations)-1):
        origin = '%s,%s' % locations[i]
        for j in range(i+1, len(locations)):
            print(i,j)
            dest = '%s,%s' % locations[j]
            url  = (BASE_URL + 'origins={}&destinations={}&mode=driving&sensor=false').format(origin, dest)
            seconds = 0
            if True:
                html = urllib.request.urlopen(url).read()
                data = json.loads(html)
                try:
                    seconds = data["rows"][0]["elements"][0]["duration"]["value"]
                except:
                    print('failed to get time')
                    print(field1, field2)
                    raise
                    return
            grid.append((i, j, seconds))
    table = pd.DataFrame(grid, columns=['from', 'to', 'weight'])
    return table

if __name__ == '__main__':
    import pandas as pd
    nodes = locations + [station]
    df = pd.DataFrame(nodes, columns=['lat', 'lon'])
    table = lookup(nodes)
    df.to_csv('output/nodes.csv', index_label='node')
    table.to_csv('output/times.csv', index=False)