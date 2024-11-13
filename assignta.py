"""
assignta.py: An evolutionary computing framework.
"""

from evo import Evo
import numpy as np
import pandas as pd
from collections import defaultdict

def allocation(A, tas):
    
    sums = [sum(TA) for TA in A]
    return sum([sums[i] - tas.at[i, 'max_assigned'] for i in range(len(sums)) if sums[i] > tas.at[i, 'max_assigned']])


def conflicts(A, sections):

    D = defaultdict(list)
    
    L = [(i, j) for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1]

    for i, j in L:
        D[i].append(j)

    
    return sum([len(set(sections.loc[indexes, 'daytime'])) != len(indexes) for _, indexes in D.items()])


def undersupport(A, sections):

    return sum([max(0, sections.loc[i, "min_ta"] - sum(ta[i] for ta in A)) for i in range(len(A[1]))])
    


def non_perferable(A, tas):

    return sum([A[i][j] for i in range(len(A)) for j in range(len(A[i])) if A[i][j] == 1 and tas.loc[i, str(j)] != 'P'])

def main():

    sections = pd.read_csv('data/sections.csv')
    print(sections)
    tas = pd.read_csv("data/tas.csv")
    print(tas)

    E = Evo()
    assign = np.random.randint(2, size=(43, 17))

    #allocation(array, tas)

    df = pd.read_csv('test/test1.csv', header=None)
    array = df.values.tolist()

    conflicts(array, sections)

    E.add_solution(assign)



main()
