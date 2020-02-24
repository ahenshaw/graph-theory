import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.generate()
 
    def vertices(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c
        
    def legal(self, r, c):
        offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                   (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for dr, dc in offsets:
            y = r + dr
            x = c + dc
            if (0 <= y < self.rows) and (0 <= x < self.cols):
                yield y, x

    def generate(self):
        self.edges = set()
        all_v = set()
        for v1 in self.vertices():
            all_v.add(v1)
            for v2 in self.legal(*v1):
                all_v.discard(v1)
                all_v.discard(v2)
                self.edges.add(tuple(sorted((v1, v2))))

        # process nodes with no neighbors
        for v in all_v:
            self.edges.add((v,v))

    def sas(self):
        print('data knights_{}_{};\ninput from $ to $;\ndatalines;'.format(self.rows, self.cols))
        for (a, b), (c,d) in sorted(self.edges):
            print('{}{} {}{}'.format(chr(ord('A')+a),b+1,chr(ord('A')+c),d+1))
        print(';')

    def plot(self):
        g = nx.Graph()
        pos = {}
        for (r1, c1), (r2, c2) in self.edges:
            u = '{},{}'.format(r1+1, c1+1)
            v = '{},{}'.format(r2+1, c2+1)
            g.add_edge(u,v)
            pos[u]=(c1, r1)
            pos[v]=(c2, r2)


        nx.draw(g, pos=pos, node_color="orange")
        # nx.draw_networkx_labels(g, pos)
        plt.show()


if __name__ == '__main__':
    board = Board(8, 8)
    board.sas()
    board.plot()
