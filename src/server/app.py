from flask import Flask
import logging
#from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
#from FlaskApp.api_layer.HelloApiHandler import HelloApiHandler
from flask import abort, render_template, request, redirect, url_for, jsonify, json, make_response, escape
from DRL_parameters import DRL_parameters
from GA_parameters import GA_parameters
from Utils.utils import choose_data, read_data, sending_to_solver
import numpy as np

app = Flask(__name__)
# app = Flask(__name__, static_url_path='', static_folder='react_client/build')
CORS(app)  # Comment this on deployment
# api = Api(app)


@app.route('/test', methods=['POST'])
def hello():
    return make_response(escape(request.form['hyper_params']))


@app.route('/operation_params/ag', methods=['POST'])
def parameter_ag():
    if request.method == 'POST':
        dataset_choice_nb = request.form['d_c']
        hyper_params = json.loads(request.form['hyper_params'])

        ag_params = GA_parameters(hyper_params["nb_epochs"],
        hyper_params["pop_size"],
        hyper_params["crossover_rate"], 
        hyper_params["mutation_rate"])
        
        dataset_choice = choose_data(dataset_choice_nb)
        data = read_data(dataset_choice)
        ts = np.array2string(data, separator=',')

        # Return sending_to_solver(data, ag_params)
        return ts

    else:
        app.logger.error('Error!')
        return 'error'


@app.route('/operation_params/drl', methods=['POST'])
def parameter_drl():
    if request.method == 'POST':
        dataset_choice_nb = request.form['d_c']
        hyper_params = json.loads(request.form['hyper_params'])
        drl_params = DRL_parameters(hyper_params['nb_epochs'],
                    hyper_params['learning_rate'],
                    hyper_params['batch_size'],
                    hyper_params['momentum']
        )
       
        dataset_choice = choose_data(dataset_choice_nb)
        data = read_data(dataset_choice)

        # Return sending_to_solver(data, drl_params)
        return data

    else:
        app.logger.error('Error!')
        return 'error'


@app.route('/result', methods=['GET'])
def get_result_graphe():
    dps = [{
        'x': 1, 'y': 10}, {'x': 2, 'y': 13}, {'x': 3, 'y': 18}, {'x': 4, 'y': 20},
        {'x': 5, 'y': 17},{'x': 6, 'y': 10}, {'x': 7, 'y': 13}, 
        {'x': 8, 'y': 18}, {'x': 9, 'y': 20}, {'x': 10, 'y': 17}]
    return dps


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
