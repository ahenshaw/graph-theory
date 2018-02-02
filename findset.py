from itertools import combinations
import networkx as nx

def findMinimalDominatingSet(g):
    k = len(g)
    for i in range(1,k):
        for c in combinations(range(k), i):
            if nx.is_dominating_set(g, c):
                return c
    return {}

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

def is_independent_set(g, s):
    edges = set()
    for v in s:
        these_edges = [tuple(sorted((a,b))) for a, b in g.edges([v])]
        if edges.intersection(these_edges):
            return False
        else:
            edges.update(these_edges)
    return True

def findMaximumIndependentSet(g):
    k = len(g)
    for i in range(k-1, 0, -1):
        for c in combinations(range(k), i):
            if is_independent_set(g, c):
                return c
    return {}
