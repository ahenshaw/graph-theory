from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np


times = np.loadtxt('output/times.csv',delimiter=',',skiprows=1, dtype=int)  
grid = {}
# the radio station is now included, so num_stores is len-1
num_stores = max(set(times[:,1]) | set(times[:,0]))
station_id = num_stores
for f, t, w in times:
    grid[(f, t)] = w
    grid[(t, f)] = w

# manipulate the grid, so that there is no cost to get back to the radio station
for f in range(num_stores):
    grid[(f, station_id)] = 0


def get_tsp(subset, plusroute=False):
    def distance(from_node, to_node):
        return grid[subset[from_node], subset[to_node]]
    # Always start with the station
    subset = [station_id] + list(subset)
    routing = pywrapcp.RoutingModel(len(subset), 1, 0)
    routing.SetArcCostEvaluatorOfAllVehicles(distance)
    assignment  = routing.Solve()

    index = routing.Start(0)
    index_next = assignment.Value(routing.NextVar(index))
    route_dist = 0
    route      = [subset[index]]
    travel_time = assignment.ObjectiveValue()/3600.0
    if plusroute:
        while True :
            #travel_time += distance(index, index_next)
            route.append(subset[index_next])
            node_index = routing.IndexToNode(index)
            node_index_next = routing.IndexToNode(index_next)
            index = index_next
            index_next = assignment.Value(routing.NextVar(index))
            if routing.IsEnd(index_next):
                break
    #travel_time /= 3600.0
    return travel_time, route

def cost(mapping):
    mapping = np.array(mapping)
    c0,_ = get_tsp(np.where(mapping == 0)[0])
    c1,_ = get_tsp(np.where(mapping == 1)[0])
    return max(c0, c1)




if __name__ == '__main__':
    mapping = np.random.choice(2, num_stores)
    print(cost(mapping))




