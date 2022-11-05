# -*- coding: utf-8 -*-

"""
This module holds tests for the cvrp.ecvrp module.

@author: Cyril Obrecht
@license: GPL-3
@date: 2022-11-02
@version: 0.1
"""

# CVRP
# Copyright (C) 2022  A.Marie, K.Sonia, M.Jean, O.Cyril, V.Axel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pytest
# pylint: disable=E0401 # False positive. This import works fine.
from src.cvrp.ecvrp import ECVRPSolution, ECVRPInstance


test_instance = ECVRPInstance(
    [
        [0, 1, 2, 2, 2],
        [3, 0, 1, 3, 2],
        [1, 2, 0, 2, 1],
        [3, 1, 1, 0, 1],
        [1, 3, 2, 2, 0]
    ],
    0,
    {1},
    {
        2: 5,
        3: 4,
        4: 6
    },
    1,
    3,
    3,
    10,
    10,
    {
        2: (),
        3: (),
        4: ()
    }
)


def test_road_building():
    """ Test the road building process: ensure the count is right
    """
    solutions = {
        2: [0, 1, 2, 3, 0, 4, 5, 0],
        1: [0, 1, 0],
        3: [0, 1, 0, 2, 0, 3, 0],
        10: [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0]
    }
    for count, solution in solutions.items():
        test = ECVRPSolution([], solution, test_instance)
        assert len(test.get_roads()) == count


def test_road_content():
    """ Test the road building process: ensure the content of the roads are goods
    """
    roads_expected = [
        {
            "source": [0, 1, 2, 3, 0, 4, 5, 0],
            "roads": [
                (0, 1, 2, 3, 0),
                (0, 4, 5, 0)
            ]
        }
    ]

    for expected in roads_expected:
        instance = ECVRPSolution([], expected["source"], test_instance)
        roads = instance.get_roads()
        for i, road in enumerate(expected["roads"]):
            assert road == roads[i]


def test_fitness():
    """ Test if the fitness computation is good
    """
    instance = ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0], test_instance)
    assert instance.get_fitness() == 8

    instance = ECVRPSolution([], [0, 2, 3, 4, 1, 0], test_instance)
    assert instance.get_fitness() == 11

    instance = ECVRPSolution([], [0, 4, 3, 0, 2, 1, 0], test_instance)
    assert instance.get_fitness() == 7


def test_d_matrix():
    """ Test the distance matrix of the ECVRPInstance class
    """
    assert test_instance.get_distance(0, 1) == 1
    assert test_instance.get_distance(0, 2) == 2
    assert test_instance.get_distance(1, 0) == 3


def test_depot():
    assert test_instance.is_depot(0)
    assert not test_instance.is_depot(1)


def test_demand():
    """ Test the `get_demand` function of the ECVRPInstance class
    """
    assert test_instance.get_demand(2) == 5

    with pytest.raises(KeyError):
        test_instance.get_demand(0)


def test_charger():
    assert test_instance.is_charger(1)
    assert not test_instance.is_charger(2)
