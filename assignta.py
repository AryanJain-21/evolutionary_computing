"""
assignta.py: An evolutionary computing framework.
"""

from evo import Evo
import random as rnd
import numpy as np


def allocation():
    pass

def conflicts():
    pass

def undersupport():
    pass

def non_perferable():
    pass

def main():

    E = Evo()
    assign = np.random.randint(2, size=(43, 17))

    E.add_solution(assign)

