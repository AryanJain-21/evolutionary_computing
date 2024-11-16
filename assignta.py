"""
assignta.py: An evolutionary computing framework.
"""

from evo import Evo
import numpy as np
import pandas as pd
from collections import defaultdict
import csv
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
    """ Agent to randomly mutate solutions """

    sol = solutions[0]
    rows, cols = len(sol), len(sol[0])

    mutated_sol = [[1 - sol[i][j] if rnd.random() < mutation_rate else sol[i][j] for j in range(cols)] for i in range(rows)]

    return mutated_sol

def support(solutions):
    """ Agent targeted to eliminate undersupport """

    sol = solutions[0]
    
    assigned_sol = [[1 if ta in [rnd.randint(0, len(sol) - 1) for _ in range(sections.loc[j, "min_ta"])] else 0 for j in range(len(sol[0]))] for ta in range(len(sol))]

    return assigned_sol

def eliminate_unwanted(solutions):
    """ Agent to eliminate unwilling and non-preferable assignments """
    sol = solutions[0]

    # Iterate over the solution matrix and set to 0 for unwanted assignments
    adjusted_sol = [
        [0 if (tas.loc[i, str(j)] == 'U' or tas.loc[i, str(j)] == 'W') and sol[i][j] == 1 else sol[i][j]
         for j in range(len(sol[0]))]
        for i in range(len(sol))
    ]

    return adjusted_sol

def crossover(solutions):
    """Combine two parent solutions using single-point crossover"""
    parent1, parent2 = solutions  # Two solutions required
    rows, cols = len(parent1), len(parent1[0])
    crossover_point = rnd.randint(0, rows - 1)

    # Create a child by combining rows from both parents
    child = [parent1[i] if i <= crossover_point else parent2[i] for i in range(rows)]
    return child

def row_mutation(solutions):
    """ Agent to mutate entire rows randomly """
    sol = solutions[0]
    rows, cols = len(sol), len(sol[0])

    row = rnd.randint(0, rows - 1)  # Choose a random row
    sol[row] = [rnd.randint(0, 1) for _ in range(cols)]  # Randomize the row

    return sol

def column_mutation(solutions):
    """ Agent to mutate entire columns randomly """
    sol = solutions[0]
    rows, cols = len(sol), len(sol[0])

    col = rnd.randint(0, cols - 1)  # Choose a random column
    for i in range(rows):
        sol[i][col] = 1 - sol[i][col]  # Flip the value

    return sol

def csv_maker(evo_object):
   """ CSV File create """
   rows = []
   group_name = "TA"
   for eval, sol in evo_object.pop.items():
        row = [group_name]
        for name, score in eval:
            row.append(score)
        rows.append(row)
        
   headers = ["groupname", "overallocation", "conflicts", "undersupport", "unwilling", "unpreferred"]


   with open('summary_table.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write each row



def main():

    E = Evo()

    E.add_fitness_criteria("o_allocation", allocation)
    E.add_fitness_criteria("time_conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    E.add_agent("mutation", mutation, k=1)
    E.add_agent("unwanted", eliminate_unwanted, k=1)
    E.add_agent("row_mutation", mutation, k=1)
    E.add_agent("column_mutation", mutation, k=1)
    E.add_agent("support", support, k=1)
    E.add_agent("crossover", crossover, k=2)

    base_sol = [[0 for _ in range(17)] for _ in range(43)]
    E.add_solution(base_sol)

    E.evolve(n=100000, dom=100, status=1000, time_limit=300)

    csv_maker(E)

    


if __name__ == '__main__':

    main()
