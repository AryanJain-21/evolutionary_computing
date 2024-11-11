"""
File: test_assignta.py
Description: Unit tests for assignta.py

python -m pytest -v --cov --cov-report term-missing

"""

from collections import defaultdict

from assignta import *
import pytest

def test_allocation():

    assert allocation() == None, "Not none"





