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
def sample_assign():

    array = np.zeros((43, 17), dtype=int)
    array[0] = 1

    return array

@pytest.fixture
def sections():

    return pd.read_csv('sections.csv')

@pytest.fixture
def tas():

    return pd.read_csv("tas.csv")


def test_allocation(sample_assign, tas):
    
    result = allocation(sample_assign, tas)
    assert result == 1, "Expected 1, but got a different output."

"""
def test_conflicts(sample_assign):
    
    result = conflicts()
    assert isinstance(result, int), "Expected an integer count of conflicts."

def test_undersupport(sample_assign):
   
    result = undersupport()
    assert isinstance(result, int), "Expected an integer indicating undersupport level."

def test_non_perferable(sample_assign):
    
    result = non_perferable()
    assert isinstance(result, int), "Expected an integer count of non-preferable assignments."




"""