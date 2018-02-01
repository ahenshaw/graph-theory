#! /usr/bin/env python
''' 
Draw graph from degree sequence
Andrew Henshaw
'''

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import warnings
warnings.filterwarnings("ignore")

def populate(g, ds):
    # take the highest degree first
    s = list(sorted([(b, a) for a, b in ds.items()], reverse=True))
    degree, src = s[0]

    if not degree:
        # our work is done
        return

    # then connect to the next (degree) nodes
    # and reduce their degree
    for i in range(degree):
        dst = s[i+1][1]
        ds[dst] -= 1
        if ds[dst] < 0:
            raise Exception('Invalid degree sequence')
        ds[src] -= 1
        g.add_edge(src, dst)
    return populate(g, ds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Draw graph from degree sequence")
    parser.add_argument('sequence', type=int, nargs='+', help='Degree Sequence (e.g. 2 1 1)')
    args = parser.parse_args()

    g = nx.Graph()
    ds = dict(enumerate(args.sequence))
    g.add_nodes_from(ds)
    populate(g, ds)

    nx.draw_circular(g)
    plt.show()
