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


@app.route("/operation_params/ag", methods=["POST"])
def parameter_ag():
    """ Instanciates an ECVRP instance and launches the GA solver.
    """
    if request.method == "POST":
        dataset_choice = request.form["d_c"]
        hyper_params = json.loads(request.form["hyper_params"])
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
        log.error("Error!")
        return "error"


@app.route("/operation_params/drl", methods=["POST"])
def parameter_drl():
    """ Instanciate an ECVRP instance and launches the DRL solver.
    """
    if request.method == "POST":
        dataset_choice = request.form["d_c"]
        hyper_params = json.loads(request.form["hyper_params"])
        # TODO: implementation for the drl solver lauching
        return str([dataset_choice, hyper_params])

    log.error("Error!")
    return "error"


# get final result
#@app.route('/result/<string:bench_id>', methods=['GET'])
#def get_result_graph(bench_id):
    #Get the resulting path graph for a given benchmark.

    #:param bench_id: The id of the benchmark.
    #:type bench_id: string
    #:return: The path graph.
    #:rtype: json

    #print(bench_id)
    # data=JsonWriter(bench_id).read_json()
    # TODO: a function to get solutions (points with their coordinates
    # and a fiel to know if the point is a charge station)
    # necessary for more understandable graphics
    # return data
    #return ""


@app.route("/get_first_sol", methods=["GET"])
def get_first_sol() :
    #d_c = int(request.args.get('dataset_choice'))
    sol = [19,21,26,7,6,5,13,1,27,17,11,8,25,29,24,14,1,18,15,9,1,12,3,20,1,28,16,22,2,23,4,10,1]
    links = []
    i=0
    while(i < (len(sol)-1)):
        link = {
        "source": sol[i],
        "target": sol[i+1]
        }
        i +=1
        links.append(link)
    #df = parser_to_df(get_datasets()[dataset_choice]) #id,coord_x, coord_y, is_station
    data_df = pd.read_csv("./Utils/Datasets/E-n29-k4-s7-c200-ecap100.csv", delimiter=";")
    coord_x = []
    coord_y = []
    station_bool = []
    for iter_s in sol:
        c_x = data_df[data_df["ID"] == iter_s]["NODE_COORD_X"].iloc[0]
        c_y = data_df[data_df["ID"] == iter_s]["NODE_COORD_Y"].iloc[0]
        s_b = data_df[data_df["ID"] == iter_s]["is_station"].iloc[0]
        coord_x.append(c_x)
        coord_y.append(c_y)
        station_bool.append(s_b)
    nodes = [{
        "id" : z[0],
        "coord_x" :z[1],
        "coord_y" :z[2],
        "is_station" :z[3]
        } for z in zip(sol, coord_x, coord_y, station_bool)
    ]

    return {"nodes" : json.dumps(str(nodes)), "links":json.dumps(str(links))}

# TODO: get snapshots
@app.route("/get_snapshots", methods=["GET"])
def get_snapshots() :
    # d_c = int(request.args.get('dataset_choice'))
    # method_choice = request.args.get('method_choice')

    #get the snap from json.io
    # result like below
    # res = .....
    # finished = False if res["has_next"] else True
    # snapshots = [{"time": t1,
    #         "individuals": [{"solution": [], "fitness": 200}
    #         },
    #         {"time": t2,
    #          "individuals": [{"solution": [], "fitness": 100}]
    #         },
    #         {"time": t3,
    #          "individuals": [{"solution": [], "fitness": 97}]
    #          }
    #     ]
    # snapshots = [{"time" = d["time"], "individuals" =d["individuals"][0].fitness } for d in snaps]
    # if(finished){
    #     return []
    # }
    # else{
    #     return snapshots
    # }

    test = [{
            "time": 11,
            "fitness": 17
        },
        {
            "time": 20,
            "fitness": 26
        },{
            "time": 39,
            "fitness": 19
        },
        {
            "time": 50,
            "fitness": 67
        },
        {
            "time": 94,
            "fitness": 55
        } ]
    return {"data" :test}

@app.route("/get_points", methods=["GET"])
def get_solution() :
    # d_c = int(request.args.get('dataset_choice'))
    # method_choice = request.args.get('method_choice')

    # #get the last snap from json.io
    # # result like below
    # snap = {"time": t,
    #         "individuals": [{"solution": [], "fitness": 200}]
    #     }
    # sol = snap.individuals[0].solution

    sol = [19,21,26,7,6,5,13,1,27,17,11,8,25,29,24,14,1,18,15,9,1,12,3,20,1,28,16,22,2,23,4,10,1]
    links = []
    i=0
    while(i < (len(sol)-1)):
        link = {
        "source": sol[i],
        "target": sol[i+1]
        }
        i +=1
        links.append(link)
    #df = parser_to_df(get_datasets()[dataset_choice]) #id,coord_x, coord_y, is_station
    data_df = pd.read_csv("./Utils/Datasets/E-n29-k4-s7-c200-ecap100.csv", delimiter=";")
    coord_x = []
    coord_y = []
    station_bool = []
    for iter_s in sol:
        c_x = data_df[data_df["ID"] == iter_s]["NODE_COORD_X"].iloc[0]
        c_y = data_df[data_df["ID"] == iter_s]["NODE_COORD_Y"].iloc[0]
        s_b = data_df[data_df["ID"] == iter_s]["is_station"].iloc[0]
        coord_x.append(c_x)
        coord_y.append(c_y)
        station_bool.append(s_b)
    nodes = [{
        "id" : z[0],
        "coord_x" :z[1],
        "coord_y" :z[2],
        "is_station" :z[3]
        } for z in zip(sol, coord_x, coord_y, station_bool)
    ]

    return {"nodes" : json.dumps(str(nodes)), "links":json.dumps(str(links))}

@app.route("/get_performance", methods=["GET"])
def get_final_results() :
    # res = get_final_snapshots() with bench_id
    # bench_id = res.bench_id
    # snapshots = [{"time": t1,
    #         "individuals": [{"solution": [], "fitness": 200}
    #         },
    #         {"time": t2,
    #          "individuals": [{"solution": [], "fitness": 100}]
    #         },
    #         {"time": t3,
    #          "individuals": [{"solution": [], "fitness": 97}]
    #          }
    #     ]
    # snapshots = [{"time" = d["time"], "individuals" =d["individuals"][0].fitness } for d in snaps]
    # return snapshots
    test = [{
            "time": 11,
            "fitness": 17
        },
        {
            "time": 20,
            "fitness": 26
        },{
            "time": 39,
            "fitness": 19
        },
        {
            "time": 50,
            "fitness": 67
        },
        {
            "time": 94,
            "fitness": 55
        }]
    return {"bench_id":"something", "data" : test}

@app.route("/get_logs", methods=["GET"])
def get_logs() :
    #res = util.get_logs_of_directory
    #return {"id" : , "logs": []}
    test_logs = [{
            "id" : "sdxdfcgfhgjb",
            "method": "ga",
            "logs" : [{
                        "time": 11,
                        "fitness": 17
                    },
                    {
                        "time": 20,
                        "fitness": 26
                    },{
                        "time": 39,
                        "fitness": 19
                    },
                    {
                        "time": 50,
                        "fitness": 67
                    },
                    {
                        "time": 94,
                        "fitness": 55
                    }]
            },
            {
            "id": "qsdsflmdkwglj",
            "method": "ga",
            "logs" : [{
                        "time": 11,
                        "fitness": 17
                    },
                    {
                        "time": 20,
                        "fitness": 26
                    },{
                        "time": 39,
                        "fitness": 19
                    },
                    {
                        "time": 50,
                        "fitness": 67
                    },
                    {
                        "time": 94,
                        "fitness": 55
                    }]
            },
            {
            "id": "mljnjdcsqeio",
            "method": "drl",
            "logs" : [{
                        "time": 11,
                        "fitness": 17
                    },
                    {
                        "time": 20,
                        "fitness": 26
                    },{
                        "time": 39,
                        "fitness": 19
                    },
                    {
                        "time": 50,
                        "fitness": 67
                    },
                    {
                        "time": 94,
                        "fitness": 55
                    }]
            },
            ]
    return {"data": test_logs}

# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
