import numpy as np
from stores import locations
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.cluster import KMeans
from credentials import API_KEY
import urllib.request
import json
import pandas as pd
import sys
from htmlparser import duration

COLOR = ('red', 'blue')
locations = np.array(locations)
#seeds = [(30, 33), (30, 6),  (23, 28), (19, 31), (23, 28), ]

URL = 'https://maps.googleapis.com/maps/api/directions/json?key={0}&origin={1}&destination={1}&waypoints=optimize:true|{2}'

results = []

best = 1e9

seeds = combinations(range(len(locations)), 2)
for seed in list(seeds):
    start = np.array([locations[seed[0]], locations[seed[1]]])
    clusters = KMeans(init=start, n_init=1, n_clusters=2, random_state=0).fit(locations).labels_
    s = clusters.sum()
    if s < 13 or s > 23:
        continue
    print(s, flush=True)
    both = 0
    html = ['','']
    t = [0, 0]
    for i in range(2):
        group = locations[clusters==i]
        waypoints = '|'.join([('%s,%s' % tuple(x)) for x in group[1:]])
        start ='%s,%s' % tuple(group[0])
        url = URL.format(API_KEY, start, waypoints)

        html[i] = urllib.request.urlopen(url).read()
        t[i] = duration(html[i])
        both += t[i]
    results.append((seed[0], seed[1], both, t[0], t[1]))
    print(results[-1], flush=True)
    if both < best:
        best = both
        open('temp0.html', 'wb').write(html[0])
        open('temp1.html', 'wb').write(html[1])

df = pd.DataFrame(results)
df.to_csv('results.csv')
