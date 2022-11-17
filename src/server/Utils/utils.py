import numpy as np
import os
from io import StringIO
import ast

from ...cvrp.ecvrp import ECVRPInstance

PATH_TO_DATASETS='src/server/datasets'

def sending_to_solver(data, algoParams):
    return ""

def parse_dataset(filename: str) -> ECVRPInstance:
    """ Parses the dataset file and create an ECVRPInstance object from the extracted data.
    """

    # Variables needed to create our ECVRP Instance
    distance_matrix: list[list[float]] = [[]]

    parameters = dict()
    nodes = dict()
    chargers = set()
    demands = dict()

    time_windows = dict()

    # Parsing the file
    with open(PATH_TO_DATASETS + '/' + filename, ) as f:

        data = StringIO(f.read().replace(':', ''))

        # Storing all words
        arr = [word for line in data for word in line.split()]

        # Extracting the values
        for i, value in enumerate(arr):
            if value == 'NODE_COORD_SECTION':
                for n in range((parameters['DIMENSION'])*3):
                    if n % 3 == 0:
                        nodes[arr[i+n+1]] = (arr[i+n+2], arr[i+n+3])
            elif value == 'DEMAND_SECTION':
                for n in range((parameters['DIMENSION']-parameters['STATIONS'])*2):
                    if n % 2 == 0:
                        demands[arr[i+n+1]] = arr[i+n+2]
            elif value == 'STATIONS_COORD_SECTION' :
                for n in range(parameters['STATIONS']):
                    chargers.add(arr[i+n+1])
            else:
                # Building the parameters dictionnary
                if not value.isdigit() and value.isupper() and value!= 'EOF' and arr[i+1].replace('.', '', 1).isdigit():
                    val = ast.literal_eval(arr[i+1])
                    parameters[value] = float(val) if isinstance(val, float) else int(val)

        #TODO: Compute distance matrix from node coordinates
        #distance_matrix = compute_distance_matrix(nodes)

    # Detect if file is incomplete
    if not (parameters or nodes or chargers or demands):
        # The dataset is missing some parameters
        raise ValueError('The dataset file is imcomplete')

    # Instantiating the ECVRP instance
    ecvrp = ECVRPInstance(distance_matrix, depot_id=parameters['DEPOT_SECTION'], chargers=chargers, demands=demands, batterie_cost_factor=parameters['ENERGY_CONSUMPTION'], \
            batterie_charge_rate=1.0, ev_count=parameters['VEHICLES'], ev_capacity=parameters['CAPACITY'], ev_battery=parameters['ENERGY_CAPACITY'], \
            time_windows= time_windows)

    return ecvrp


def get_datasets() -> list[str]:
    """ List all the files in the dataset folder.
    """
    return os.listdir(PATH_TO_DATASETS)

# Debug
evrp = parse_dataset(get_datasets()[0])


