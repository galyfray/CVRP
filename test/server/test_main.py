# -*- coding: utf-8 -*-

"""
This module holds the tests for the main part of the server
@author: Cyril OBRECHT
@license: GPL-3
@date: 2022-11-22
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

import json

import pytest

from src.server.main import Server

BENCHMARK = "E-n29-k4-s7.evrp"


@pytest.fixture()
def app():
    """Produce a fixture that ease the production of tests"""
    appli = Server(__name__).app
    appli.config.update({
        "TESTING": True,
    })

    yield appli


@pytest.fixture()
def client(app):
    return app.test_client()


def test_bench_list(client):
    """Test the benchmarks endpoint"""
    response = client.get("benchmarks")
    assert response.status_code == 200
    assert "README.txt" not in response.json


def test_log_list(client):
    """Test the benchmarks endpoint"""
    response = client.get("logs")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    if len(response.json) > 0:
        log = response.json[0]
        assert log["method"] is not None
        assert log["snapshots"] is not None
        assert log["bench_id"] is not None


def test_bench(client):
    response = client.get("benchmark/E-n29-k4-s7.evrp")
    assert response.status_code == 200


def test_run_busy(client):
    """Test if the busy flag is correctly set"""
    response = client.post("run", data={
        "type": "ga",
        "bench_id": BENCHMARK,
        "seed": 0,
        "override": "true",
        "snapshot_rate": 1,
        "param": json.dumps({
            "nb_epochs": 2,
            "pop_size": 4,
            "mutation_rate": 0.1,
            "crossover_rate": 1
        })
    })

    assert response.status_code == 200
    assert response.json["busy"] is False

    response = client.post("run", data={
        "type": "ga",
        "bench_id": BENCHMARK,
        "seed": 0,
        "override": "true",
        "snapshot_rate": 1,
        "param": json.dumps({
            "nb_epochs": 2,
            "pop_size": 4,
            "mutation_rate": 0.1,
            "crossover_rate": 1
        })
    })

    assert response.status_code == 200
    assert response.json["busy"]
