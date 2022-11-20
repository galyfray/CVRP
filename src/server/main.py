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
    """This class holds the server, its state and routes"""

    def __init__(self, name: str) -> None:
        """
        Initialize the server. Does not start it.

        :param name: The name of the Flask application
        """
        self._runner = None

        self.app = Flask(name)
        # app = Flask(__name__, static_url_path='', static_folder='react_client/build')

        CORS(self.app)

        self.app.add_url_rule("/run", view_func=self.route_run, methods=["POST"])
        self.app.add_url_rule("/status", view_func=self.route_status, methods=["GET"])
        self.app.add_url_rule("/snapshot", view_func=self.route_snapshot, methods=["GET"])
        self.app.add_url_rule("/benchmarks", view_func=self.route_benchmarks, methods=["GET"])
        self.app.add_url_rule("/benchmark", view_func=self.route_benchmark, methods=["GET"])
        self.app.add_url_rule("/logs", view_func=self.route_logs, methods=["GET"])
        self.app.add_url_rule("/results", view_func=self.route_results, methods=["GET"])

    def run(self, **kwargs):
        """Runs the application on a local development server.
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
        """Method handling the start of an instance"""
        if self._runner is not None:
            return {"busy": True}

        if request.method == "POST":
            metho = request.form["type"]
            if metho not in HYPER_LIST:
                pass  # raise error
            hyper = {key: request.form["param"][key] for key in HYPER_LIST[metho]}

            # parsing benchmark
            # create a snapshot
            # Seed the random

            if metho == "ga":
                pass  # create the instance

        return None

    def route_status(self):
        """Provide a way to check the status of the server"""
        return {"status": "free"} if self._runner is None else {"status": "busy"}

    def route_snapshot(self):
        """
        Return the latest computed snapshot of the current solving.

        If no solving is running a placeholder is returned with generation set to -1.
        """
        if self._runner is None:
            return {
                "has_next": False,
                "snapshot": [],
                "generation": -1
            }

        # TODO : run a genration, send snap to json_io, handle the end of run.

        return {
                "has_next": True,
                "snapshot": [
                    {"time": time.thread_time(), "individuals": [
                        {"solution": (0, 1, 2, 0, 4, 3, 0), "fitness": 1}
                    ]}
                ],
                "generation": 0
            }

    def route_benchmarks(self):
        """Provide a list of all the available benchmarks"""
        # TODO: import bench_dir from parser and list all files in the directory
        # should I cache this information ?
        return ["None"]

    def route_benchmark(self):
        """Load and return a specific benchmark."""
        # load the bench
        # convert the bench to JSON
        return {}

    def route_logs(self):
        """Provide a list of all available logs."""
        # list all files from the logs folder
        # transform data according to what needs the front
        # return the data
        # This should be cached.

    def route_results(self):
        """Load a log file and provide its content."""
        # load the correct JSON
        # return it.


if __name__ == "__main__":
    Server(__name__).run(debug=True)
