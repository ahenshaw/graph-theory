import json

def duration(html):
    data = json.loads(html)
    total = 0
    for route in data['routes']:
        for leg in route['legs']:
            total += leg['duration']['value']
    return total/3600.0

def path(html):
    data = json.loads(html)
    total = 0
    polylines = []
    for route in data['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                polylines.append(step['polyline']['points'])
    return polylines

if __name__ == '__main__':
    html = open('temp1.html', 'rb').read()
    print(path(html))
