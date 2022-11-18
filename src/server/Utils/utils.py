# -*- coding: utf-8 -*-
"""
This module holds parts of the implementation of the backend server that communicate
with the CVRP solver.
@author: Axel Velez and Sonia KWASSI
@license: GPL-3
@date: 2022-11-18
@version: 0.2
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

import os
from io import StringIO
import ast

from ...cvrp.ecvrp import ECVRPInstance

PATH_TO_DATASETS = 'src/server/datasets'


def parse_dataset(filename: str) -> ECVRPInstance:
    """ Parses the dataset file and create an ECVRPInstance object from the extracted data.
    """

    # Variables needed to create our ECVRP Instance
    distance_matrix: list[list[float]] = [[]]

    parameters = {}
    nodes: dict[int, tuple[int, int]] = {}
    chargers: set[int] = set()
    demands: dict[int, int] = {}

    time_windows: dict[int, tuple[float, float]] = {}

    # Parsing the file
    with open(PATH_TO_DATASETS + '/' + filename, 'r', encoding='utf8') as f:

        data = StringIO(f.read().replace(':', ''))

        # Storing all words
        arr = [word for line in data for word in line.split()]

        # Extracting the values
        for i, value in enumerate(arr):
            if value == 'NODE_COORD_SECTION':
                for n in range((parameters['DIMENSION'])*3):
                    if n % 3 == 0:
                        nodes[int(arr[i+n+1])] = (int(arr[i+n+2]), int(arr[i+n+3]))
                        time_windows[int(arr[i+n+1])] = (0, float('inf'))
            elif value == 'DEMAND_SECTION':
                for n in range((parameters['DIMENSION']-parameters['STATIONS'])*2):
                    if n % 2 == 0:
                        demands[int(arr[i+n+1])] = int(arr[i+n+2])
            elif value == 'STATIONS_COORD_SECTION':
                for n in range(parameters['STATIONS']):
                    chargers.add(int(arr[i+n+1]))
            else:
                # Building the parameters dictionnary
                if not value.isdigit() and value.isupper() and value != 'EOF' \
                        and arr[i+1].replace('.', '', 1).isdigit():
                    val = ast.literal_eval(arr[i+1])
                    parameters[value] = float(val) if isinstance(val, float) else int(val)

        # TODO: Compute distance matrix from node coordinates
        # distance_matrix = compute_distance_matrix(nodes)

    # Detect if file is incomplete
    if not (parameters or nodes or chargers or demands):
        # The dataset is missing some parameters
        raise ValueError('The dataset file is imcomplete')

    # Instantiating the ECVRP instance
    ecvrp = ECVRPInstance(distance_matrix, depot_id=parameters['DEPOT_SECTION'], chargers=chargers,
                          demands=demands, batterie_cost_factor=parameters['ENERGY_CONSUMPTION'],
                          batterie_charge_rate=1.0, ev_count=parameters['VEHICLES'],
                          ev_capacity=parameters['CAPACITY'],
                          ev_battery=parameters['ENERGY_CAPACITY'], time_windows=time_windows)

    return ecvrp


def get_datasets() -> list[str]:
    """ List all the files in the dataset folder.
    """
    return os.listdir(PATH_TO_DATASETS)


# Debug
evrp = parse_dataset(get_datasets()[0])
