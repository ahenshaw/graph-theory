from itertools import combinations

def is_vertex_cover(g, s):
    h = g.copy()
    for v in s:
        h.remove_node(v)
    return len(h.edges()) == 0

def findMinimalVertexCover(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if is_vertex_cover(g, c):
                return c
    return {}

