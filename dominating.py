from itertools import combinations
import networkx as nx

def findMinimalDominatingSet(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if nx.is_dominating_set(g, c):
                return c
    return {}

for (name, fn) in [('Path Graph', nx.path_graph),
                 ('Cycle Graph', nx.cycle_graph),
                 ('Complete Graph', nx.complete_graph),
                 ('Circular Ladder Graph', nx.circular_ladder_graph)]:
    
    print(name)
    for n in range(2, 13):
        g = fn(n)
        s = findMinimalDominatingSet(g)
        print('    ', n, len(s), s)
