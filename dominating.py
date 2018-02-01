from itertools import combinations
import networkx as nx
N = 6

def findMinimalDominatingSet(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if nx.is_dominating_set(g, c):
                return c
    return {}

import sys
for n in range(2,114):
    g = nx.circular_ladder_graph(n)
    s = findMinimalDominatingSet(g)
    print(n, len(s), s)
    sys.stdout.flush()
