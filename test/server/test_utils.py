# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of the backend server that communicate
with the CVRP solver.
@author: Axel Velez
@license: GPL-3
@date: 2022-11-19
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

from pathlib import Path
import pytest
from src.server.utils.utils import get_datasets, parse_dataset, compute_distance_matrix, \
                                   create_ecvrp

PATH = Path('test/server/test_datasets')
DATASET = 'E-n5-k4-s2.evrp'

cities = {1: (145, 215), 2: (151, 264), 3: (159, 261), 4: (130, 254), 5: (200, 176)}

parsed_data = {
    'VEHICLES': 4,
    'CAPACITY': 6000,
    'ENERGY_CAPACITY': 99,
    'ENERGY_CONSUMPTION': 1.0,
    'NODES': cities,
    'DEMANDS': {1: 0, 2: 1100, 3: 700},
    'STATIONS': {4, 5},
    'TIME_WINDOWS': {
        1: (0, float('inf')), 2: (0, float('inf')), 3: (0, float('inf')),
        4: (0, float('inf')), 5: (0, float('inf'))},
    'DEPOT': 1}

distance_matrix = [
    [0.0, 49.36, 48.08, 41.78, 67.42],
    [49.36, 0.0, 8.54, 23.25, 100.72],
    [48.08, 8.54, 0.0, 29.83, 94.37],
    [41.78, 23.25, 29.83, 0.0, 104.80],
    [67.42, 100.72, 94.37, 104.80, 0.0]
]


def test_get_datasets():
    """ Test if it lists the datasets for a given path."""

    file = get_datasets(PATH)[0]
    assert file == DATASET


def test_parse_dataset():
    """ Test if the parser correctly extracts the data from the dataset."""
    data = parse_dataset(DATASET, PATH)
    assert data == parsed_data


def test_create_evrp():
    """ Test if the EVRPInstance is created with the right parameters."""

    evrp = create_ecvrp(parsed_data)

    assert evrp.get_ev_capacity() == 6000
    assert evrp.get_demand(2) == 1100
    assert evrp.get_ev_count() == 4
    assert evrp.get_tw(2) == (0, float('inf'))
    # assert evrp.get_towns() == [2, 3]  # TODO: Fix get_towns()
    assert evrp.get_ev_battery() == 99
    assert evrp.is_charger(3) is False and evrp.is_charger(4) is True
    assert evrp.get_batterie_charging_rate() == 1.00
    assert evrp.is_depot(1) is True
    assert pytest.approx(evrp.get_distance(0, 1), 0.001) == 49.37


def test_compute_distance_matrix():
    """ Check if the distance matrix computation is correct."""

    matrix = compute_distance_matrix(cities)

    for line, distances in enumerate(matrix):
        assert pytest.approx(distances, 0.001) == distance_matrix[line]
