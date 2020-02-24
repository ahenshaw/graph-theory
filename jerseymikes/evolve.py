#!/usr/bin/python3
# standard library
import random
import time
import sys
import argparse

# third-party libraries
import wx
import numpy
import arrow
from deap import base
from deap import creator
from deap import tools
from deap import algorithms

# custom modules
import strategy
from tsp2 import cost

UPDATE_INTERVAL = 1 # second

class evolution:
    def __init__(self, population_size):
        
        
        self.population_size = population_size
        self.best_fitness    = 1e100 # exceedingly large number
        self.best_gen        = 0
        self.last_update     = 0

        self.start_time = time.time()
        print()
        print('Generation  Elapsed      Fitness   Best Gen')
        print('----------  -----------  -------   --------')
    
    def evaluate(self, individual):
        fitness = cost(individual)
        return (fitness,)
        
    def update(self, generation, population, fittest):
        elapsed = time.time() - self.start_time
        fitness, = fittest[0].fitness.values
        if fitness >= self.best_fitness:
            # stuck on previous best result
            if elapsed - self.last_update < UPDATE_INTERVAL:
                return
        else:
            open('evolve.log', 'a').write('{}\n'.format(fittest[0]))
            self.best_fitness = fitness
            self.best_gen = generation
 
        self.last_update = elapsed
        sys.stdout.write('\r{:10}  {}  {:4.3}      {} '.format(generation, 
                                             arrow.get(elapsed).format('HH:mm:ss.SS'), 
                                             fitness, self.best_gen))
        
        
    def mutate(self, individual):
        for i in range(3):
            individual[random.randint(0, len(individual)-1)] = random.randint(0,1)
                
    def start(self):
        num_genes = 37
        
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("gene",       lambda: random.randint(0,1))
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.gene, n=num_genes)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate",   self.evaluate)
        toolbox.register("mate",       tools.cxTwoPoint)
        toolbox.register("mutate",     self.mutate)
        toolbox.register("select",     tools.selTournament, tournsize=3)

        self.population = toolbox.population(n=self.population_size)
        crossover_prob  = 0.5
        mutation_prob   = 0.3

        self.fittest = tools.HallOfFame(1)

        self.population = strategy.simple(self.population, 
                                          toolbox,
                                          cxpb       = crossover_prob,
                                          mutpb      = mutation_prob,
                                          ngen       = 1000000,
                                          halloffame = self.fittest,
                                          report     = self.update,
                                          interval   = 1)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=20, type=int, help='population size')
    args = parser.parse_args()
    
    ga = evolution(population_size=args.p)
    ga.start()