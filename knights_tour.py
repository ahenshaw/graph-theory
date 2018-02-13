class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
 
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
        edges = set()
        for v1 in self.vertices():
            for v2 in self.legal(*v1):
                edges.add(tuple(sorted((v1, v2))))
        return sorted(edges)


R = C = 3
print('data knights_{}_{};\ninput from $ to $;\ndatalines;'.format(R,C))

board = Board(R, C)
for (a, b), (c,d) in board.generate():
    print('{}_{} {}_{}'.format(a+1,b+1,c+1,d+1))

print(';')