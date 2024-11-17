"""
assignta.py: Managing Fitness Criteria and Agents for variation in Evolutionary Computing, 
    using evo.py (Evolution Framework)
Date: November 16, 2024
"""

from evo import Evo
import pandas as pd
from collections import defaultdict
import csv
import random as rnd

# TA and Course Section Data to be used. Setting as global variables
sections = pd.read_csv('data/sections.csv')
tas = pd.read_csv("data/tas.csv")

def allocation(A):
    """ Assigns penalities if TAs are overallocated, assigned to more sections than specfied as their maximum.
    Input:
    - A: 2D list of assignments for all the TAs

    Returns: Penalty score based off of overallocation """
    
    sums = [sum(TA) for TA in A]
    return sum([sums[i] - tas.at[i, 'max_assigned'] for i in range(len(sums)) if sums[i] > tas.at[i, 'max_assigned']])


def conflicts(A):
    """ Assigns penalities if TAs are assigned to sections with overlapping times.
    Input:
    - A: 2D list of assignments for all the TAs

    Returns: Penalty score based off of conflicts """

    D = defaultdict(list)
    
    # Stores each TA and the section they are assigned to
    L = [(i, j) for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1]

    # Stores TA as a key and their sections as values
    for i, j in L:
        D[i].append(j)

    # Identifying conflicts by converting to set to filter duplicates
    return sum([len(set(sections.loc[indexes, 'daytime'])) != len(indexes) for _, indexes in D.items()])


def undersupport(A):
    """ Assigns penalities if sections do not have enough TAs assigned to them.
    Input:
    - A: 2D list of assignments for all the TAs

    Returns: Penalty score based off of undersupport """

    return sum([max(0, sections.loc[i, "min_ta"] - sum(ta[i] for ta in A)) for i in range(len(A[1]))])
    
def unwilling(A):
    """ Assigns penalities if TAs are assigned to sections they are unwilling to support.
    Input:
    - A: 2D list of assignments for all the TAs

    Returns: Penalty score based off of unwillingness """

    return sum([A[i][j] for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1 and tas.loc[i, str(j)] == 'U'])

def unpreferred(A):
    """ Assigns penalities if TAs are assigned to sections they do not prefer, but are willing, to support.
    Input:
    - A: 2D list of assignments for all the TAs

    Returns: Penalty score based off of unpreferredness """

    return sum([A[i][j] for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1 and tas.loc[i, str(j)] == 'W'])

def mutation(solutions):
    """ Agent to randomly mutate each indivudal assignment based off of a given chance. 
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution with mutations """

    sol = solutions[0]
    mutation_rate = 0.3

    # Iterates through all assignments, with a 30% chance to mutate the assignment, if 1 --> 0, if 0 --> 1.
    adjusted_sol = [
        [1 - sol[i][j] if rnd.random() < mutation_rate else sol[i][j] 
         for j in range(len(sol[0]))] 
         for i in range(len(sol))
    ]

    return adjusted_sol

def support(solutions):
    """ Agent targeted to eliminate undersupport penalties.
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]
    
    # Iterates through each section, assigning the minimum necessary TAs for each section randomly 
    adjusted_sol = [
        [1 if ta in [rnd.randint(0, len(sol) - 1) for _ in range(sections.loc[j, "min_ta"])] else 0 
         for j in range(len(sol[0]))] 
         for ta in range(len(sol))
    ]

    return adjusted_sol

def eliminate_unwanted(solutions):
    """ Agent to eliminate unwilling and unpreferable assignment penalties.
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    # Iterates through each assignment, setting all unwilling and unpreferred assignments as 0
    adjusted_sol = [
        [0 if (tas.loc[i, str(j)] == 'U' or tas.loc[i, str(j)] == 'W') and sol[i][j] == 1 else sol[i][j]
         for j in range(len(sol[0]))]
        for i in range(len(sol))
    ]

    return adjusted_sol

def eliminate_overallocation(solutions):
    """ Agent to eliminate overallocation penalties using list comprehension.
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    # Iterates through each TA, calculating if their assignments exceeds their maximum, and setting random
    # assignments to 0 if it does exceed their maximum.
    adjusted_sol = [
        [
            0 if j in rnd.sample(
                [k for k in range(len(sol[i])) if sol[i][k] == 1],
                sum(sol[i]) - tas.at[i, "max_assigned"]
            ) and sum(sol[i]) > tas.at[i, "max_assigned"] else sol[i][j]
            for j in range(len(sol[i]))
        ]
        for i in range(len(sol))
    ]

    return adjusted_sol


def crossover(solutions):
    """ Agent that combines two parent solutions using a random single-point crossover
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Child solution """

    parent1, parent2 = solutions
    crossover_point = rnd.randint(0, len(parent1) - 1)

    # Create a child by combining rows from both parents
    child = [parent1[i] if i <= crossover_point else parent2[i] for i in range(len(parent1))]

    return child

def row_mutation(solutions):
    """ Agent to mutate entire rows randomly 
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    # Selecting random row to completely mutate
    row = rnd.randint(0, len(sol) - 1)
    sol[row] = [rnd.randint(0, 1) for _ in range(len(sol[0]))]

    return sol

def column_mutation(solutions):
    """ Agent to mutate entire columns randomly 
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    # Selecting entire column to completely mutate
    col = rnd.randint(0, len(sol[0]) - 1)

    for i in range(len(sol)):
        sol[i][col] = 1 - sol[i][col]

    return sol

def ensure_nonzero(solutions):
    """ Agent that ensures no row in the solution matrix has all zeros,
    unless a TA has a maximum of zero assigned listed
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    # If max_assigned is not 0, seeing if all cells are 0, if they are randomly assigning one or two of them to one.
    adjusted_sol = [
        [
            1 if tas.loc[i, "max_assigned"] != 0 and all(cell == 0 for cell in sol[i]) and j in rnd.sample(range(len(sol[i])), rnd.choice([1, 2]))
            else sol[i][j]
            for j in range(len(sol[i]))
        ]
        for i in range(len(sol))
    ]

    return adjusted_sol


def reassign_unwilling(solutions):
    """ Agent to reassign TAs from sections they are unwilling to other random sections 
    whether it is preferred or not. Done with loops because I couldn't figure out how to write it
    functionally.
    Input:
    - solutions: 2D list of assignments for all the TAs

    Returns: Adjusted solution """

    sol = solutions[0]

    for i in range(len(sol)):

        for j in range(len(sol[0])):

            # If assigned to an unwilling section
            if sol[i][j] == 1 and tas.loc[i, str(j)] == 'U':

                # All sections this TA is willing to be assigned to
                willing_sections = [k for k in range(len(sol[0])) if tas.loc[i, str(k)] != 'U' and sol[i][k] == 0]

                # In case there are no willing sections that are left at 0, chooses random willing_sections to assign
                if willing_sections:

                    new_section = rnd.choice(willing_sections)

                    # Sets unwilling assignment at 0 and the new section at 1
                    sol[i][j] = 0
                    sol[i][new_section] = 1

    return sol



def csv_maker(evo_object):
   """ Saves solutions into CSV files.
    Input:
    - evo_object: The Evolution object post evolve
    """
   
   rows = []
   group_name = "AC"
   sol_lst = []
   for eval, sol in evo_object.pop.items():
        row = [group_name]
        for name, score in eval:
            row.append(score)
        rows.append(row)
        sol_lst.append(sol)
        
   headers = ["groupname", "overallocation", "conflicts", "undersupport", "unwilling", "unpreferred"]


   with open('solutions/summary_table.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

   with open('solutions/sol_table.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sol_lst)


def main():

    E = Evo()

    # All objectives
    E.add_fitness_criteria("o_allocation", allocation)
    E.add_fitness_criteria("time_conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    # All Agents
    E.add_agent("mutation", mutation, k=1)
    E.add_agent("reassign_unwilling", reassign_unwilling, k=1)
    E.add_agent("unwanted", eliminate_unwanted, k=1)
    E.add_agent("allocation", eliminate_overallocation, k=1)
    E.add_agent("row_mutation", mutation, k=1)
    E.add_agent("column_mutation", mutation, k=1)
    E.add_agent("support", support, k=1)
    E.add_agent("crossover", crossover, k=2)
    E.add_agent("noassignments", ensure_nonzero, k=1)

    # Solution will all 0s, acting as a base solution
    base_sol = [[0 for _ in range(17)] for _ in range(43)]
    E.add_solution(base_sol)

    # Evolve for 5 minutes, finding a near optimized solution, then save results to CSVs
    E.evolve(n=100000, dom=100, status=1000, time_limit=300)

    csv_maker(E)

    


if __name__ == '__main__':

    main()
