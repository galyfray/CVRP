# -*- coding: utf-8 -*-

"""
This module holds tests for the cvrp.ecvrp module.

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

from src.server.utils.utils import get_datasets, parse_dataset, compute_distance_matrix

PATH = 'test/server/test_datasets'
DATASET = 'E-n5-k4-s2.evrp'

cities = {1: (145, 215), 2: (151, 264), 3: (159, 261), 4: (130, 254), 5: (200, 176)}

expected_distance_matrix = [
    [0.0, 49.36598018878993, 48.08326112068523, 41.78516483155236, 67.42403132415029], 
    [49.36598018878993, 0.0, 8.54400374531753, 23.259406699226016, 100.72239075796404], 
    [48.08326112068523, 8.54400374531753, 0.0, 29.832867780352597, 94.37160589923221], 
    [41.78516483155236, 23.259406699226016, 29.832867780352597, 0.0, 104.80458005259122], 
    [67.42403132415029, 100.72239075796404, 94.37160589923221, 104.80458005259122, 0.0]
]


def test_get_datasets():
    """ Test if it lists the datasets for a given path.
    """

    file = get_datasets(PATH)[0]
    assert file == DATASET


def test_dataset_parser():
    """ Test if the parser creates an EVRPInstance with the right parameters.
    """

    evrp = parse_dataset(DATASET, PATH)

    assert evrp.get_ev_capacity() == 6000
    assert evrp.get_demand(2) == 1100
    assert evrp.get_ev_count() == 4
    assert evrp.get_tw(2) == (0, float('inf'))
    # assert evrp.get_towns() == [2, 3]  # TODO: Fix get_towns()
    assert evrp.get_ev_battery() == 99
    assert evrp.is_charger(3) is False and evrp.is_charger(4) is True
    assert evrp.get_batterie_charging_rate() == 1.00
    assert evrp.is_depot(1) is True
    assert evrp.get_distance(0, 1) == 49.36598018878993


def test_compute_distance_matrix():
    """ Check if the distance matrix computation is correct.
    """

    distance_matrix = compute_distance_matrix(cities)
    assert distance_matrix == expected_distance_matrix
