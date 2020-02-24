from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
from math import ceil

times = np.loadtxt('output/times.csv',delimiter=',',skiprows=1, dtype=int)  
grid = {}
# the radio station is now included, so num_stores is len-1
num_stores = max(set(times[:,1]) | set(times[:,0]))
station_id = num_stores
for f, t, w in times:
    grid[(f, t)] = w
    grid[(t, f)] = w
for i in range(num_stores+1):
    grid[(i,i)] = 0

# manipulate the grid, so that there is no cost to get back to the radio station
for f in range(num_stores):
    grid[(f, station_id)] = 0


def get_tsp(subset, plusroute=False):
    def distance(from_node, to_node):
        return grid[subset[from_node], subset[to_node]]
    
    num_vehicles = 2
    # Always start with the station
    subset = [station_id] + list(subset)
    routing = pywrapcp.RoutingModel(len(subset), num_vehicles, 0)
    routing.SetArcCostEvaluatorOfAllVehicles(distance)
    
    # Add time dimension.
    fix_start_cumul_to_zero = True
    horizon = int(6.4*3600)
    time = "Time"

    routing.AddDimension(distance,
                        horizon,
                        horizon,
                        fix_start_cumul_to_zero,
                        time)
    for vehicle in range(num_vehicles):
        routing.AddVariableMinimizedByFinalizer(routing.CumulVar(routing.End(vehicle), time))

    assignment  = routing.Solve()

    route = []
    travel_time = []
    for vehicle in range(num_vehicles):
        index = routing.Start(vehicle)
        index_next = assignment.Value(routing.NextVar(index))
        while True :
            node_index = routing.IndexToNode(index)
            node_index_next = routing.IndexToNode(index_next)
            # first time through loop?
            if len(route) == vehicle:
                route.append([subset[node_index]])
                travel_time.append(0)
            route[vehicle].append(subset[node_index_next])
            travel_time[vehicle] += distance(node_index, node_index_next)/3600.0
            index = index_next
            index_next = assignment.Value(routing.NextVar(index))
            if routing.IsEnd(index_next):
                break
    return travel_time, route


if __name__ == '__main__':
    stores = list(range(num_stores))
    print(get_tsp(stores))




