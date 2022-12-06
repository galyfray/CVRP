# -*- coding: utf-8 -*-

"""
This module holds tests for the cvrp.ecvrp module.

@author: Cyril Obrecht
@author: Marie Aspro
@license: GPL-3
@date: 2022-12-06
@version: 0.4
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


from copy import copy
import random
import pytest
# pylint: disable=E0401 # False positive. This import works fine.
from src.cvrp.ecvrp import ECVRPSolution, ECVRPInstance
from src.cvrp.constraints_validators import\
    VehiculeCountValidator,\
    TownUnicityValidator,\
    CapacityValidator

test_instance_1 = ECVRPInstance(
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


test_instance_2 = ECVRPInstance(
    [
        [0, 2, 4, 7],
        [2, 0, 6, 9],
        [4, 6, 0, 5],
        [7, 9, 5, 0]
    ],
    0,
    {},
    {
        1: 1,
        2: 1,
        3: 1,
    },
    1,
    3,
    3,
    10,
    14,
    {
        1: (),
        2: (),
        3: ()
    }
)


def test_road_building():
    """ Test the road building process: ensure the count is right.
    """

    solutions = {
        2: [0, 1, 2, 3, 0, 4, 5, 0],
        1: [0, 1, 0],
        3: [0, 1, 0, 2, 0, 3, 0],
        10: [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0]
    }
    for count, solution in solutions.items():
        test = ECVRPSolution([], solution, test_instance_1)
        assert len(test.get_roads()) == count


def test_road_content():
    """ Test the road building process: ensure the content of the roads are goods.
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
        instance = ECVRPSolution([], expected["source"], test_instance_1)
        roads = instance.get_roads()
        for i, road in enumerate(expected["roads"]):
            assert road == roads[i]


def test_fitness():
    """ Test if the fitness computation is good.
    """

    instance = ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0], test_instance_1)
    assert instance.get_fitness() == 8

    instance = ECVRPSolution([], [0, 2, 3, 4, 1, 0], test_instance_1)
    assert instance.get_fitness() == 11

    instance = ECVRPSolution([], [0, 4, 3, 0, 2, 1, 0], test_instance_1)
    assert instance.get_fitness() == 7


def test_is_valid():
    """ Test if the is_valid method works as expected.
    """

    town = TownUnicityValidator()
    capacity = CapacityValidator()
    count = VehiculeCountValidator()

    assert ECVRPSolution(
        [town],
        [0, 4, 3, 0, 2, 1, 0],
        test_instance_1
    ).is_valid()
    assert ECVRPSolution(
        [town, capacity],
        [0, 4, 3, 0, 2, 1, 0],
        test_instance_1
    ).is_valid()
    assert ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 0, 2, 1, 0],
        test_instance_1
    ).is_valid()

    assert not ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 0, 2, 1, 2, 0],
        test_instance_1
    ).is_valid()

    assert not ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 1, 2, 0],
        test_instance_1
    ).is_valid()

    assert not ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 0, 2, 1, 0, 0, 0],
        test_instance_1
    ).is_valid()


def test_copy():
    """ Test if the copy keyword works as expected.
    """

    town = TownUnicityValidator()
    capacity = CapacityValidator()
    count = VehiculeCountValidator()
    instance_1 = ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 0, 2, 1, 0],
        test_instance_1
    )
    instance_2 = ECVRPSolution(
        [town, capacity, count],
        [0, 4, 3, 1, 2, 0],
        test_instance_1
    )

    instance_1_copy = copy(instance_1)
    instance_2_copy = copy(instance_2)

    assert instance_1.get_fitness() == instance_1_copy.get_fitness()
    assert instance_1.is_valid() == instance_1_copy.is_valid()

    assert instance_2.get_fitness() == instance_2_copy.get_fitness()
    assert instance_2.is_valid() == instance_2_copy.is_valid()

    assert copy(instance_1_copy).get_fitness() == instance_1_copy.get_fitness()
    assert copy(instance_1_copy).is_valid() == instance_1_copy.is_valid()


def test_d_matrix():
    """ Test the distance matrix of the ECVRPInstance class.
    """

    assert test_instance_1.get_distance(0, 1) == 1
    assert test_instance_1.get_distance(0, 2) == 2
    assert test_instance_1.get_distance(1, 0) == 3


def test_depot():
    """ Test if the depot can be correctly detected.
    """
    assert test_instance_1.is_depot(0)
    assert not test_instance_1.is_depot(1)


def test_demand():
    """ Test the `get_demand` function of the ECVRPInstance class.
    """
    assert test_instance_1.get_demand(2) == 5

    with pytest.raises(KeyError):
        test_instance_1.get_demand(0)


def test_charger():
    """ Test if a charger can be correctly detected.
    """
    assert test_instance_1.is_charger(1)
    assert not test_instance_1.is_charger(2)


def test_crossover():
    """ Test if the crossover method works correctly.
    """
    random.seed(8)

    parent_1 = ECVRPSolution([], [0, 4, 2, 0, 3, 1, 0], test_instance_1)
    parent_2 = ECVRPSolution([], [0, 2, 3, 0, 1, 4, 0], test_instance_1)

    [enfant_1, enfant_2] = parent_1.crossover(parent_2)

    assert enfant_1.get_fitness() == 4
    assert enfant_2.get_fitness() == 4

    assert enfant_1.get_roads() == ((0, 2, 0), (0, 3, 4, 0))
    assert enfant_2.get_roads() == ((0, 3, 4, 0), (0, 2, 0))


def test_mutation():
    """ Test if the mutation method works correctly.
    """
    random.seed(3)

    mutant = ECVRPSolution([], [0, 4, 1, 2, 0, 3, 0], test_instance_1)
    mutant.mutate()
    assert mutant.get_roads() == ((0, 2, 4, 0), (0, 3, 0))


def test_empty_road():
    """ Test if an empty road can be find.
    """
    instance = ECVRPSolution([], [0, 4, 1, 0, 2, 3, 0, 0], test_instance_1)
    solution = instance.get_roads()
    solution = [list(x) for x in solution]
    assert instance.delete_empty_road(solution) == [[0, 4, 1, 0], [0, 2, 3, 0]]


def test_road_correction():
    """ Test the road correction algorithm.
    """
    instance = ECVRPSolution([], [0, 3, 1, 2, 0], test_instance_2)
    roads = instance.get_roads()
    list_roads = [list(x) for x in roads]
    new_road = instance._road_correction(list_roads[0])
    assert new_road == [0, 3, 0, 1, 2, 0]
