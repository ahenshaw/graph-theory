import networkx as nx
from findset import findMinimalVertexCover, findMinimalDominatingSet, findMaximumIndependentSet


for title, find_fn in [('Maximal Matching', nx.maximal_matching),
                       ('Maximum Independent Set', findMaximumIndependentSet),
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