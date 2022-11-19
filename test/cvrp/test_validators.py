# -*- coding: utf-8 -*-

"""
This module holds tests for the cvrp.constraint_validators module.

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

import math

# pylint: disable=E0401 # False positive. This import works fine.
from src.cvrp.ecvrp import ECVRPSolution, ECVRPInstance
from src.cvrp.constraints_validators import \
    BatteryTWValidator,\
    VehiculeCountValidator,\
    TownUnicityValidator,\
    CapacityValidator

test_instance = ECVRPInstance(
    [
        [0, 1, 3, 2, 2],
        [3, 0, 1, 3, 2],
        [1, 2, 0, 2, 1],
        [3, 1, 1, 0, 3],
        [3, 3, 2, 2, 0]
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
        2: (0, math.inf),
        3: (0, math.inf),
        4: (5, 7)
    }
)


def test_battery_validator():
    """ Test if the battery validatation works."""
    validator = BatteryTWValidator()
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0], test_instance))
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 2, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 4, 2, 3, 2, 3, 0, 1, 0], test_instance))


def test_time_windows():
    """ Test if the time window validation works."""
    validator = BatteryTWValidator()

    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 1, 4, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 1, 2, 1, 4, 0], test_instance))


def test_vehicule_count():
    """ Test if the vehicule count validator works."""
    validator = VehiculeCountValidator()

    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0], test_instance))
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0, 0], test_instance))


def test_town_unicity():
    """ Test if the vehicule count validator works."""
    validator = TownUnicityValidator()

    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 4, 1, 0, 0, 0], test_instance))
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0, 4, 0], test_instance))
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 1, 0, 0, 1, 0], test_instance))
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 1, 0, 0, 1, 0], test_instance))


def test_capacity():
    """ Test if the vehicule capacity validator works."""
    validator = CapacityValidator()
    assert validator.is_valid(ECVRPSolution([], [0, 2, 3, 0, 4, 0], test_instance))
    assert not validator.is_valid(ECVRPSolution([], [0, 2, 3, 4, 0], test_instance))
