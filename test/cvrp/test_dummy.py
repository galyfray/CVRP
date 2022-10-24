"""
Simple test module used to check that pytest config is working fine
"""
# pylint: disable=E0401 # False positive. This import works fine.
from src.cvrp.dummy import hello


def test_hello():
    assert hello("World") == "Hello World !"
