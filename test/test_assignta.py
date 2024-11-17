"""
File: test_assignta.py
Description: Unit tests for assignta.py

python -m pytest -v --cov --cov-report term-missing

"""

from assignta import *
import numpy as np
import pytest
import pandas as pd

@pytest.fixture
def A():
    df = pd.read_csv('test/test1.csv', header=None)
    return df.values.tolist()

@pytest.fixture
def B():
    df = pd.read_csv('test/test2.csv', header=None)
    return df.values.tolist()

@pytest.fixture
def C():
    df = pd.read_csv('test/test3.csv', header=None)
    return df.values.tolist()

@pytest.fixture
def D():
    df = pd.read_csv('solutions/solution_matrix.csv', header=None)
    return df.values.tolist()


def test_allocation(A, B, C, D):
    
    assert allocation(A) == 37, "Expected 37, but got a different output."
    assert allocation(B) == 41, "Expected 41, but got a different output."
    assert allocation(C) == 23, "Expected 23, but got a different output."
    assert allocation(D) == 0, "Expected 0, but got a different output."


def test_conflicts(A, B, C, D):
    
    assert conflicts(A) == 8, "Expected 8, but got a different output."
    assert conflicts(B) == 5, "Expected 5, but got a different output."
    assert conflicts(C) == 2, "Expected 2, but got a different output."
    assert conflicts(D) == 0, "Expected 0, but got a different output."


def test_undersupport(A, B, C, D):
   
    assert undersupport(A) == 1, "Expected 1, but got a different output."
    assert undersupport(B) == 0, "Expected 0, but got a different output."
    assert undersupport(C) == 7, "Expected 7, but got a different output."
    assert undersupport(D) == 1, "Expected 213, but got a different output."


def test_unwilling(A, B, C, D):
    
    assert unwilling(A) == 53, "Expected 53, but got a different output."
    assert unwilling(B) == 58, "Expected 58, but got a different output."
    assert unwilling(C) == 43, "Expected 43, but got a different output."
    assert unwilling(D) == 0, "Expected 0, but got a different output."

def test_unpreferred(A, B, C, D):
    
    assert unpreferred(A) == 15, "Expected 15, but got a different output."
    assert unpreferred(B) == 19, "Expected 19, but got a different output."
    assert unpreferred(C) == 10, "Expected 10, but got a different output."
    assert unpreferred(D) == 3, "Expected 3, but got a different output."

