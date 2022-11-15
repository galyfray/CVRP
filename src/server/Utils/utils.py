import numpy as np
import os

PATH_TO_DATASETS='src/server/datasets'

#TODO: Parse .ecvrp
def read_data(filename):
    # using loadtxt()
    path = "./Utils/Datasets/" + filename
    data = np.loadtxt(path,
                    delimiter=";", dtype=str)
    return data

def sending_to_solver(data, algoParams):
    return ""

def parse_dataset(filename):

    # Instanciate ECVRP instance


    # Parsing the file
    with open(PATH_TO_DATASETS + '/' + filename) as f:
        
        arr =[word for line in f for word in line.split()]

        for i, value in enumerate(arr):
            if value == 'VEHICLES:':
                nb_vehicles = arr[i+1]
                print(nb_vehicles)


def get_datasets():
    return os.listdir(PATH_TO_DATASETS)

parse_dataset('E-n29-k4-s7.evrp')
#print(get_datasets())
