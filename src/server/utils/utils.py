# -*- coding: utf-8 -*-
"""
This module contains the necessary functions to parse and create ECVRP instances.
@authors: Axel Velez
@license: GPL-3
@date: 2022-11-22
@version: 0.6
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
import sys
from os import path
from pathlib import Path
import numpy as np


# pylint: disable=wrong-import-position disable=E0401
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from cvrp.ecvrp import ECVRPInstance # noqa E402
# pylint: enable=wrong-import-position enable=E0401

PATH_TO_DATASETS = Path('src/server/datasets')

# Offset used to map the original cities id to their new values
OFFSET = 1


def parse_dataset(filename: str, dir_path: Path = PATH_TO_DATASETS) -> dict[str, any]:
    """Parses the dataset file and extracts the data.

    :param filename: The name of the dataset to parse
    :type filename: str
    :param dir_path: The path of the dataset's directory, defaults to PATH_TO_DATASETS
    :type dir_path: Path, optional
    :return: A parsed dataset object
    :rtype: dict[str, any]
    """

    # Variables needed to create our ECVRP Instance
    parameters: dict[str, any] = {}
    nodes: dict[int, tuple[float, float]] = {}
    chargers: set[int] = set()
    demands: dict[int, int] = {}
    time_windows: dict[int, tuple[float, float]] = {}

    # Parsing the file
    with open(dir_path / filename, 'r', encoding='utf8') as file:

        file = StringIO(file.read().replace(':', ''))

        # Storing all words
        data = [word for line in file for word in line.split()]

        # Extracting the values
        for i, value in enumerate(data):
            if value == 'NODE_COORD_SECTION':
                for index in range((parameters['DIMENSION'])*3):
                    # Extracts the id and coordinates of each node (3 values per line)
                    if index % 3 == 0:
                        nodes[int(data[i+index+1]) - OFFSET] = \
                            (float(data[i+index+2]), float(data[i+index+3]))
                        time_windows[int(data[i+index+1]) - OFFSET] = (0, sys.maxsize)
            elif value == 'DEMAND_SECTION':
                for index in range((parameters['DIMENSION']-parameters['STATIONS'])*2):
                    # Extracts the id and demand for each node (2 values per line)
                    if index % 2 == 0:
                        demands[int(data[i+index+1]) - OFFSET] = int(data[i+index+2])
            elif value == 'STATIONS_COORD_SECTION':
                for index in range(parameters['STATIONS']):
                    chargers.add(int(data[i+index+1]) - OFFSET)
            else:  # Building the parameters dictionnary
                # Making sure the selected word is a valid key
                # and not a numerical value or the end of the file
                if not value.isdigit() and value.isupper() and value != 'EOF' \
                        and data[i+1].replace('.', '', 1).isdigit():
                    if value == 'DEPOT_SECTION':
                        # If the value is a depot, we need to offset it as well
                        val = int(data[i+1]) - OFFSET
                    else:
                        val = ast.literal_eval(data[i+1])
                    parameters[value] = val if isinstance(val, float) else int(val)

    return {'VEHICLES': parameters['VEHICLES'],
            'CAPACITY': parameters['CAPACITY'],
            'ENERGY_CAPACITY': parameters['ENERGY_CAPACITY'],
            'ENERGY_CONSUMPTION': parameters['ENERGY_CONSUMPTION'],
            'NODES': nodes,
            'DEMANDS': demands,
            'STATIONS': chargers,
            'TIME_WINDOWS': time_windows,
            'DEPOT': parameters['DEPOT_SECTION']}


def create_ecvrp(parameters: dict[str, any]) -> ECVRPInstance:
    """Create an ECVRPInstance object from the parsed data.

    :param parameters: A parsed dataset object given by parse_dataset()
    :type parameters: dict[str, any]
    :return: An ECVRP instance
    :rtype: ECVRPInstance
    """

    distance_matrix = compute_distance_matrix(parameters['NODES'])

    # Instantiating the ECVRP instance
    ecvrp = ECVRPInstance(distance_matrix=distance_matrix,
                          depot_id=parameters['DEPOT'],
                          chargers=parameters['STATIONS'],
                          demands=parameters['DEMANDS'],
                          batterie_cost_factor=parameters['ENERGY_CONSUMPTION'],
                          batterie_charge_rate=1.0,
                          ev_count=parameters['VEHICLES'],
                          ev_capacity=parameters['CAPACITY'],
                          ev_battery=parameters['ENERGY_CAPACITY'],
                          time_windows=parameters['TIME_WINDOWS'])

    return ecvrp


def get_datasets(dir_path: Path = PATH_TO_DATASETS) -> list[str]:
    """List all the files in the dataset folder.

    :param dir_path: The path of the datasets directory, defaults to PATH_TO_DATASETS
    :type dir_path: Path, optional
    :return: A list of all files contained in the specified directory
    :rtype: list[str]
    """
    return os.listdir(dir_path)


def compute_distance_matrix(nodes: dict[int, tuple[float, float]]) -> list[list[float]]:
    """Compute the distance matrix of our nodes."""

    distance_matrix = np.zeros(shape=(len(nodes), len(nodes))).tolist()

    for node, (current_x, current_y) in nodes.items():
        for next_node, (next_x, next_y) in nodes.items():
            if node != next_node:
                dist = np.sqrt(np.power(current_x-next_x, 2) + np.power(current_y-next_y, 2))
                distance_matrix[node][next_node] = dist

    return distance_matrix
