#!/usr/bin/python
"""
Simple dummy module used to check that pytest works fine
"""


def hello(name: str):
    return "Hello " + name + " !"


if __name__ == "__main__":
    print(hello("Wolrd"))