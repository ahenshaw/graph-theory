from itertools import combinations
import networkx as nx

def findMinimalDominatingSet(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if nx.is_dominating_set(g, c):
                return c
    return {}

for name, fn in [('Path Graph', nx.path_graph),
                 ('Cycle Graph', nx.cycle_graph),
                 ('Complete Graph', nx.complete_graph),
                 ('Circular Ladder Graph', nx.circular_ladder_graph)]:
    
    
    print('\n'+name)
    for n in range(2, 13):
        g = fn(n)
        s = findMinimalDominatingSet(g)
        print('    n={:2}:  {:2}  {}'.format(n, len(s), s))

print('\nComplete Bipartite')
for m in range(2, 7):
    for n in range(2, 7):
        g = nx.complete_bipartite_graph(m, n)
        s = findMinimalDominatingSet(g)
        print('    m={} n={}:  {:2}  {}'.format(m, n, len(s), s))
