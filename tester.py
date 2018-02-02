from itertools import combinations
import networkx as nx

from vertexcover import findMinimalVertexCover
from dominating  import findMinimalDominatingSet

def is_independent_set(G, s):
    edges = set()
    for v in s:
        these_edges = [tuple(sorted((a,b))) for a, b in G.edges([v])]
        if edges.intersection(these_edges):
            return False
        else:
            edges.update(these_edges)
    return True


def findMaximumIndependentSet(G):
    k = len(g)
    for i in range(k-1, 0, -1):
        for c in combinations(range(k), i):
            if is_independent_set(g, c):
                return c
    return {}


for title, find_fn in [('Maximum Independent Set', findMaximumIndependentSet),
                       ('Minimal Vertex Cover', findMinimalVertexCover),
                       ('Minimal Dominating Set', findMinimalDominatingSet)
                       ]:
    print(title)
    for name, fn in [('Path Graph', nx.path_graph),
                    ('Cycle Graph', nx.cycle_graph),
                    ('Complete Graph', nx.complete_graph),
                    ('Circular Ladder Graph', nx.circular_ladder_graph)]:
        
        
        print('    '+name)
        for n in range(2, 11):
            g = fn(n)
            s = find_fn(g)
            print('        n={:2}:  {:2}  {}'.format(n, len(s), s))
        print()

    print('    Complete Bipartite')
    for m in range(2, 7):
        for n in range(2, 7):
            g = nx.complete_bipartite_graph(m, n)
            s = find_fn(g)
            print('        m={} n={}:  {:2}  {}'.format(m, n, len(s), s))
    print()