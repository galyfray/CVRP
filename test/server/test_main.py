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
from copy import copy

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


BASE_DATA = {
        "type": "ga",
        "bench_id": BENCHMARK,
        "seed": 0,
        "override": "false",
        "snapshot_rate": 1,
        "params": json.dumps({
            "nb_epochs": 2,
            "pop_size": 4,
            "mutation_rate": 0.1,
            "crossover_rate": 1
        })
}


def test_run_busy(client):
    """Test if the busy flag is correctly set"""
    response = client.post("run", data=BASE_DATA)

    assert response.status_code == 200
    assert response.json["busy"] is False

    response = client.post("run", data=BASE_DATA)

    assert response.status_code == 200
    assert response.json["busy"]


def test_snapshot(client):
    """Test the snapshot route"""
    client.post("run", data=BASE_DATA)
    response = client.get("snapshot")

    assert response.status_code == 200
    assert response.json["has_next"]
    assert response.json["generation"] == 1
    assert len(response.json["snapshot"]) == 4

    response = client.get("snapshot")
    assert response.status_code == 200
    assert response.json["has_next"] is False
    assert response.json["generation"] == 2
    assert len(response.json["snapshot"]) == 4


def test_snapshot_rate(client):
    """Test if the snapshot rate works as intended"""
    data = copy(BASE_DATA)
    data["snapshot_rate"] = 2
    data["params"] = json.dumps({
            "nb_epochs": 7,
            "pop_size": 4,
            "mutation_rate": 0.1,
            "crossover_rate": 1
        })

    client.post("run", data=data)

    response = client.get("snapshot")
    responses = [response]

    while response.json["has_next"]:
        response = client.get("snapshot")
        responses.append(response)

        assert response.status_code == 200
        assert response.json["generation"] % 2 == 0 or response.json["generation"] == 7

    assert len(responses) == 4


def test_seed(client):
    """Test if the seed does make the whole process repeatable"""
    client.post("run", data=BASE_DATA)

    response = client.get("snapshot")
    firsts = [response.json]

    while response.json["has_next"]:
        response = client.get("snapshot")
        firsts.append(response.json)

    client.post("run", data=BASE_DATA)

    response = client.get("snapshot")
    seconds = [response.json]

    while response.json["has_next"]:
        response = client.get("snapshot")
        seconds.append(response.json)

    for first, second in zip(firsts, seconds):
        assert first == second
