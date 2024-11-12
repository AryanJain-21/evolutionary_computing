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
def sections():
    return pd.read_csv('data/sections.csv')

@pytest.fixture
def tas():
    return pd.read_csv("data/tas.csv")


def test_allocation(A, B, C, tas):
    
    assert allocation(A, tas) == 37, "Expected 37, but got a different output."
    assert allocation(B, tas) == 41, "Expected 41, but got a different output."
    assert allocation(C, tas) == 23, "Expected 23, but got a different output."


def test_conflicts(A, B, C, sections):
    
    conflicts(A, sections)
    #assert isinstance(result, int), "Expected an integer count of conflicts."

"""
def test_undersupport(sample_assign):
   
    result = undersupport()
    assert isinstance(result, int), "Expected an integer indicating undersupport level."

def test_non_perferable(sample_assign):
    
    result = non_perferable()
    assert isinstance(result, int), "Expected an integer count of non-preferable assignments."




"""