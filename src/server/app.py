# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of the backend server that communicate
with the CVRP solver.
@author: Sonia Kwassi
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

from flask import Flask
from flask import request, json
from flask.logging import create_logger
from flask_cors import CORS


# from Utils.utils import parse_dataset, get_datasets
# from ..cvrp.json_io import JsonWriter
# from ..cvrp.ga import GA
# from ..cvrp.individual import Individual
# from ..cvrp.ecvrp import ECVRPSolution
import pandas as pd

app = Flask(__name__)
# comment this on deployment
CORS(app)
log = create_logger(app)


@app.route('/test', methods=['POST'])
def hello():
    return request.form['hyper_params']


@app.route('/operation_params/ag', methods=['POST'])
def parameter_ag():
    """ Instanciates an ECVRP instance and launches the GA solver.
    """
    if request.method == 'POST':
        dataset_choice = request.form['d_c']
        hyper_params = json.loads(request.form['hyper_params'])
        # instancing an ECVRP problem with the informations needed
        # ecvrp_instance = parse_dataset(get_datasets()[dataset_choice])
        # building the population with the random solutions
        # population = ECVRPSolution(ecvrp_instance) #to change if needed
        # instancing the ga with the hyperparameters sent by the frontend
        # ga = GA(population, hyper_params["mutation_rate"], hyper_params["seed"]) #change if needed
        # resolving the ecvrp problem with the ga instance
        # ga.run(hyper_params["nb_epochs"])
        # sps = JsonWriter("name", "benchname")
        return str([dataset_choice, hyper_params])

    else:
        log.error('Error!')
        return 'error'


@app.route('/operation_params/drl', methods=['POST'])
def parameter_drl():
    """ Instanciate an ECVRP instance and launches the DRL solver.
    """
    if request.method == 'POST':
        dataset_choice = request.form['d_c']
        hyper_params = json.loads(request.form['hyper_params'])
        # TODO: implementation for the drl solver lauching
        return str([dataset_choice, hyper_params])

    else:
        log.error('Error!')
        return 'error'


# get curve of the fitness evolution over time
@app.route('/get_snapshots', methods=['GET'])
def get_snapshots():
    """ Get the snapshots of a given log instance.
    """
    # TODO: get snapshots over time
    # [{"generation": tuple[int, ...],"fitness": tuple[float, ...]}]
    return 'nothing for the moment'


# get final result
@app.route('/result/<string:bench_id>', methods=['GET'])
def get_result_graph(bench_id):
    """ Get the resulting path graph for a given benchmark.

    :param bench_id: The id of the benchmark.
    :type bench_id: string
    :return: The path graph.
    :rtype: json
    """
    print(bench_id)
    # data=JsonWriter(bench_id).read_json()
    # TODO: a function to get solutions (points with their coordinates
    # and a fiel to know if the point is a charge station)
    # necessary for more understandable graphics
    # return data
    dataframe = pd.read_csv('./file_test/E-n29-k4-s7-c200-ecap100.csv', delimiter=';')
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    return dataframe.to_json(orient='records')


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
