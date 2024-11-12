"""
assignta.py: An evolutionary computing framework.
"""

from evo import Evo
import random as rnd
import numpy as np
import pandas as pd

def allocation(A, tas):
    
    sums = [sum(TA) for TA in A]
    return sum([sums[i] > tas.at[i, 'max_assigned'] for i in range(len(sums))])


def conflicts():
    pass

def undersupport():
    pass

def non_perferable():
    pass

def main():

    sections = pd.read_csv('sections.csv')
    print(sections)
    tas = pd.read_csv("tas.csv")
    print(tas)

    E = Evo()
    assign = np.random.randint(2, size=(43, 17))

    array = np.zeros((43, 17), dtype=int)
    array[0] = 1

    allocation(array, tas)

    E.add_solution(assign)

main()
