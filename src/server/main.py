# -*- coding: utf-8 -*-

"""
This module holds the rest server that bridge the solvers and the front end.

@authors: ["Cyril Obrecht", "Sonia Kwassi"]
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import math
import time
from flask import Flask, request
from flask_cors import CORS

from src.cvrp.ecvrp import ECVRPInstance

HYPER_LIST = {
    "ga": [
        "nb_epochs",
        "pop_size",
        "mutation_rate",
        "crossover_rate"
    ]
}


class Server:
    """Docs goes here"""

    def __init__(self, name: str):
        self._runner = None

        self.app = Flask(name)
        # app = Flask(__name__, static_url_path='', static_folder='react_client/build')

        CORS(self.app)

        self.app.add_url_rule("/run", view_func=self.route_run, methods=["POST"])

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def route_run(self):
        """Function handling the start of an instance"""
        if self._runner is not None:
            return {"busy": True}

        if request.method == "POST":
            metho = request.form["type"]
            if metho not in HYPER_LIST:
                pass  # raise error
            hyper = {key: request.form["param"][key] for key in HYPER_LIST[metho]}

            # parsing benchmark
            if metho == "ga":
                pass  # create the instance

        return None

    def route_status(self):
        return {"status": "free"} if self._runner is None else {"status": "busy"}

    def route_snapshot(self):
        """Doxumentation goes here"""
        if self._runner is None:
            return {
                "has_next": False,
                "snapshot": [],
                "generation": -1
            }

        return {
                "has_next": True,
                "snapshot": [
                    {"time": time.thread_time(), "individuals": [
                        {"solution": (0, 1, 2, 0, 4, 3, 0), "fitness": 1}
                    ]}
                ],
                "generation": 0
            }



if __name__ == "__main__":
    Server(__name__).run(debug=True)
