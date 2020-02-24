from tsp2 import get_tsp, grid
import numpy as np
best = open('evolve.log', 'r').readlines()[-1]
mapping = np.array(eval(best))
c0,r0 = get_tsp(np.where(mapping == 0)[0], True)
c1,r1 = get_tsp(np.where(mapping == 1)[0], True)
def actual(route):
    total = 0
    start = route[0]
    for node in route[1:]:
        total += grid[(node, start)]
        start = node
    return total/3600.0

print(r0)
print('TSP: {:4.3} hrs\nA-Z: {:4.3} hrs\n'.format(c0, actual(r0)))
print(r1)
print('TSP: {:4.3} hrs\nA-Z: {:4.3} hrs\n'.format(c1, actual(r1)))


