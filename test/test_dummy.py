"""
Simple test module used to check that pytest config is working fine
"""
from cvrp.dummy import hello


def test_hello():
    assert hello("World") == "Hello World !"
