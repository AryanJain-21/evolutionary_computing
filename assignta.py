"""
assignta.py: An evolutionary computing framework.
"""

from evo import Evo
import numpy as np
import pandas as pd
from collections import defaultdict
from profiler import profile, Profiler
import time
import random as rnd

sections = pd.read_csv('data/sections.csv')
tas = pd.read_csv("data/tas.csv")

def allocation(A):
    
    sums = [sum(TA) for TA in A]
    return sum([sums[i] - tas.at[i, 'max_assigned'] for i in range(len(sums)) if sums[i] > tas.at[i, 'max_assigned']])


def conflicts(A):

    D = defaultdict(list)
    
    L = [(i, j) for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1]

    for i, j in L:
        D[i].append(j)

    
    return sum([len(set(sections.loc[indexes, 'daytime'])) != len(indexes) for _, indexes in D.items()])


def undersupport(A):

    return sum([max(0, sections.loc[i, "min_ta"] - sum(ta[i] for ta in A)) for i in range(len(A[1]))])
    
def unwilling(A):

    return sum([A[i][j] for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1 and tas.loc[i, str(j)] == 'U'])

def unpreferred(A):

    return sum([A[i][j] for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1 and tas.loc[i, str(j)] == 'W'])

def mutation(solutions, mutation_rate=0.3):

    sol = solutions[0]
    rows, cols = len(sol), len(sol[0])

    mutated_sol = [[1 - sol[i][j] if rnd.random() < mutation_rate else sol[i][j] for j in range(cols)] for i in range(rows)]

    return mutated_sol


@profile
def main():

    E = Evo()

    E.add_fitness_criteria("o_allocation", allocation)
    E.add_fitness_criteria("time_conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)


    base_sol = [[0 for _ in range(17)] for _ in range(43)]
    E.add_solution(base_sol)

    E.evolve(n=10000, dom=100, status=1000)

    print(E)

    


if __name__ == '__main__':

    main()

    Profiler.report()
