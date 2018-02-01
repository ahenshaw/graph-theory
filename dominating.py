import networkx as nx
from itertools import combinations

N = 6

def makeCircularLadder(n):
    g = nx.Graph()
    g.add_nodes_from(range(2*n))
    for i in range(n-1):
        g.add_edge(i, (i+1))
        g.add_edge(i, n+i)
    for i in range(n, 2*n-1):
        g.add_edge(i, (i+1))
    g.add_edge(0, n-1)
    g.add_edge(n, 2*n-1)
    return g

def findMinimalDominatingSet(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if nx.is_dominating_set(g, c):
                return c
    return {}

import sys
for n in range(2,114):
    g = makeCircularLadder(n)
    s = findMinimalDominatingSet(g)
    print(n, len(s), s)
    sys.stdout.flush()
