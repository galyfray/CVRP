# -*- coding: utf-8 -*-

"""
This module holds the rest server that bridge the solvers and the front end.

@author: Cyril Obrecht
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

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# app = Flask(__name__, static_url_path='', static_folder='react_client/build')

CORS(app)


HYPER_LIST = {
    "ga": [
        "nb_epochs",
        "pop_size",
        "mutation_rate",
        "crossover_rate"
    ]
}


def run():
    """Function handling the start of an instance"""
    if request.method == "POST":
        metho = request.form["type"]
        if metho not in HYPER_LIST:
            pass  # raise error
        hyper = {key: request.form["param"][key] for key in HYPER_LIST[metho]}

        # parsing benchmark

        if metho == "ga":
            pass


if __name__ == "__main__":
    app.add_url_rule("/run", view_func=run, methods=["POST"])

    app.run(debug=True)
