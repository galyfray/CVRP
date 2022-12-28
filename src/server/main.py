# -*- coding: utf-8 -*-

"""
This module holds the rest server that bridge the solvers and the front end.

@author: Cyril Obrecht
@author: Sonia Kwassi
@license: GPL-3
@date: 2022-11-02
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import time
import random
import json
from copy import copy

from flask import Flask, request
from flask_cors import CORS

from src.cvrp.ecvrp import ECVRPSolution, ECVRPInstance
from src.cvrp.json_io import JsonWriter, read_json, get_header
from src.cvrp.ga import GA
from src.cvrp import constraints_validators
from .utils import utils

HYPER_LIST = {
    "ga": [
        "nb_epochs",
        "pop_size",
        "mutation_rate",
        "seed"
    ]
}


def build_first_gen(size: int, instance: ECVRPInstance):
    """Build a first generation of n valid individuals."""
    validators = [
        constraints_validators.BatteryTWValidator(),
        constraints_validators.CapacityValidator(),
        constraints_validators.VehiculeCountValidator()
    ]

    towns = instance.get_towns()

    first_gen: list[ECVRPSolution] = []

    while len(first_gen) < size:
        solution = [*towns]
        roads = [
            [instance.get_depot()]
            for _ in range(instance.get_ev_count())
        ]
        cumulatives = [0] * instance.get_ev_count()
        random.shuffle(solution)
        not_inserted = True
        for point in solution:
            not_inserted = True
            i = 0
            while not_inserted:
                if i >= len(cumulatives):
                    print("i is too big")
                    break
                if cumulatives[i] + instance.get_demand(point) <= instance.get_ev_capacity():
                    cumulatives[i] += instance.get_demand(point)
                    roads[i].append(point)
                    not_inserted = False
                i += 1
            if not_inserted:
                print("not inserted")
                break
        if not_inserted:
            continue

        solution = []
        for road in roads:
            solution.extend(road)
        solution.append(instance.get_depot())
        element = ECVRPSolution(validators, solution, instance)

        element.validate()

        if element.is_valid():
            first_gen.append(element)

    return first_gen


class Server:
    """This class holds the server, its state and routes."""

    def __init__(self, name: str) -> None:
        """
        Initialize the server. Does not start it.

        :param name: The name of the Flask application
        """
        self._runner = None
        self._snapshot = None
        self._nb_it = 0
        self._count = 0
        self._tot_time = 0
        self._override = True
        self._name = ""
        self._rate = 0
        self._latest = {}

        self.app = Flask(name)
        # app = Flask(__name__, static_url_path='', static_folder='react_client/build')

        CORS(self.app)

        self.app.add_url_rule("/run", view_func=self.route_run, methods=["POST"])
        self.app.add_url_rule("/status", view_func=self.route_status, methods=["GET"])
        self.app.add_url_rule("/snapshot", view_func=self.route_snapshot, methods=["GET"])
        self.app.add_url_rule("/benchmarks", view_func=self.route_benchmarks, methods=["GET"])
        self.app.add_url_rule(
                "/benchmark/<bench_id>", view_func=self.route_benchmark, methods=["GET"]
                )
        self.app.add_url_rule("/logs", view_func=self.route_logs, methods=["GET"])
        self.app.add_url_rule("/log/<log_id>", view_func=self.route_log, methods=["GET"])
        self.app.add_url_rule("/results", view_func=self.route_results, methods=["GET"])

    def run(self, **kwargs):
        """Run the application on a local development server.

        Do not use ``run()`` in a production setting. It is not intended to
        meet security and performance requirements for a production server.
        Instead, see :doc:`/deploying/index` for WSGI server recommendations.

        If the :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        If you want to run the application in debug mode, but disable the
        code execution on the interactive debugger, you can pass
        ``use_evalex=False`` as parameter.  This will keep the debugger's
        traceback screen active, but disable code execution.

        It is not recommended to use this function for development with
        automatic reloading as this is badly supported.  Instead you should
        be using the :command:`flask` command line script's ``run`` support.

        This documentation comes from the Flask module
        and is protected according to the licence of the said module :
        BSD 3-Clause "New" or "Revised" License. Please see
        https://github.com/pallets/flask/blob/main/LICENSE.rst
        for more information.

        .. admonition:: Keep in Mind
           Flask will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to ``True`` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.
        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well. Defaults to
            ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
            if present.
        :param port: the port of the webserver. Defaults to ``5000`` or the
            port defined in the ``SERVER_NAME`` config variable if present.
        :param debug: if given, enable or disable debug mode. See
            :attr:`debug`.
        :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
            files to set environment variables. Will also change the working
            directory to the directory containing the first file found.
        :param options: the options to be forwarded to the underlying Werkzeug
            server. See :func:`werkzeug.serving.run_simple` for more
            information.
        .. versionchanged:: 1.0
            If installed, python-dotenv will be used to load environment
            variables from :file:`.env` and :file:`.flaskenv` files.
            The :envvar:`FLASK_DEBUG` environment variable will override :attr:`debug`.
            Threaded mode is enabled by default.
        .. versionchanged:: 0.10
            The default port is now picked from the ``SERVER_NAME``
            variable.

        """
        self.app.run(**kwargs)

    def route_run(self):
        """
        Handle the start of an instance.

        expected data :

        {
            "type":"drl|ga",
            "params":{
                "nb_epochs":"int",
                "pop_size?":"int",
                "mutation_rate?":"float",
                "crossover_rate?":"float",
                "learning_rate?":"float",
                "batch_size?":"int",
                "momentum?":"float",
                "seed":"int"
            },
            "override":"bool",
            "bench_id":"string",
            "snapshot_rate":"int"
        }

        Returns :
        {
            “busy”:”bool”
        }


        """
        if self._runner is not None:
            return {"busy": True}

        if request.method == "POST":
            data = json.loads(request.data)["data"]
            
            metho = data["type"]
            if metho not in HYPER_LIST:
                raise TypeError(f"Unkown method {metho}")

            hyper = {key: data["params"][key] for key in HYPER_LIST[metho]}

            self._nb_it = hyper["nb_epochs"]
            self._count = 0

            self._rate = int(data["snapshot_rate"])

            bench = utils.create_ecvrp(utils.parse_dataset(data["bench_id"]))

            random.seed(int(hyper["seed"]))

            self._name = f"{data['bench_id']}_{metho}_{hyper['seed']}"
            for param in hyper.values():
                self._name += f"_{param}"

            if metho == "ga":
                g_a = GA(
                        build_first_gen(hyper["pop_size"], bench),
                        hyper["mutation_rate"],
                        hyper["seed"]
                    )
                self._runner = g_a.run(hyper["nb_epochs"])
                self._tot_time = 0

            self._override = data["override"]

            self._snapshot = JsonWriter(
                str(utils.PATH_TO_LOGS),
                self._name,
                data["bench_id"],
                metho
            )

            return {"busy": False}

        return None

    def route_status(self):
        """Provide a way to check the status of the server."""
        return {"status": "free"} if self._runner is None else {"status": "busy"}

    def route_snapshot(self):
        """
        Return the latest computed snapshot of the current solving.

        If no solving is running a placeholder is returned with generation set to -1.

        No expected input

        Returns :

        {
            "has_next":"bool",
            "snapshot":"[Individual]",
            "generation":"int"
        }

        The snapshot type is defined in the json_io class.

        """
        if self._runner is None:
            return {
                "has_next": False,
                "snapshot": [],
                "generation": -1
            }

        self._count += 1
        compute = time.thread_time()
        gen = next(self._runner)

        while self._count != self._nb_it and self._count % self._rate != 0:
            gen = next(self._runner)
            self._count += 1

        compute = time.thread_time() - compute
        self._tot_time += compute

        base = {
                "has_next": not self._count == self._nb_it,
                "snapshot": [],
                "generation": self._count
            }

        base["snapshot"] = self._snapshot.add_snapshot(gen, self._tot_time)

        self._latest = copy(base)

        base["snapshot"] = base["snapshot"]["individuals"]

        if self._count == self._nb_it:
            if self._override or self._name not in utils.get_logs():
                self._snapshot.dump()
            self._runner = None

        return base

    def route_benchmarks(self):
        """Provide a list of all the available benchmarks."""
        return [{"name": b, "details": utils.get_ds_description(b)} for b in utils.get_datasets()]

    def route_benchmark(self, bench_id: str):
        """
        Load and return a specific benchmark.

        The benchmark is returned in the same format as provider by the benchmark reader.
        """
        bench = utils.parse_dataset(bench_id)
        bench["STATIONS"] = list(bench["STATIONS"])
        return bench

    def route_logs(self):
        """
        Provide a list of all available logs.

        The snapshot provided is the last used.

        returns :

        [
            {
                bench_id: str,
                method: ga|drl
                snapshots: "snapshot"
            }
        ]

        """
        logs = []

        for log in utils.get_logs():
            logs.append(get_header(utils.PATH_TO_LOGS, log))

        return logs

    def route_log(self, log_id):
        """
        Load a log file and provide its content.

        returns the same json as stored.
        """
        return read_json(utils.PATH_TO_LOGS, log_id)

    def route_results(self):
        """Return the latest snapshot to date or an empty dict if no snapshot was computed."""
        return self._latest


if __name__ == "__main__":
    Server(__name__).run()
