# -*- coding: utf-8 -*-

"""
This module holds tests for the cvrp.json_io module.

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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
from pathlib import Path
# pylint: disable=E0401 # False positive. This import works fine.
from src.cvrp.json_io import JsonWriter, read_json
from src.cvrp.ecvrp import ECVRPSolution, ECVRPInstance


test_instance = ECVRPInstance(
    [
        [0, 1, 2, 2, 2],
        [3, 0, 2, 1, 2],
        [1, 2, 0, 2, 1],
        [3, 1, 2, 0, 2],
        [1, 3, 1, 2, 0]
    ],
    0,
    {1},
    {
        2: 5,
        3: 4,
        4: 6
    },
    1,
    3,
    3,
    12,
    12,
    {
        2: (),
        3: (),
        4: ()
    }
)


def test_snapshot_writting(tmpdir: Path):
    """ writes meta data and a snapshot to the JSON file format
    """
    writer = JsonWriter(
        str(tmpdir),
        "writter_snap",
        "bench_test",
        "ga"
    )

    writer.add_snapshot([
        ECVRPSolution([], [0, 1, 2, 3, 0, 4, 0], test_instance),
        ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0], test_instance),
        ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0, 4, 0], test_instance)
    ], time.thread_time())
    writer.dump()

    assert True


def test_snapshots_writting(tmpdir: Path):
    """ writes meta data and snapshots to the JSON file format
    """
    writer = JsonWriter(
        str(tmpdir),
        "writter_snaps",
        "bench_test",
        "ga"
    )
    for _ in range(9):
        writer.add_snapshot([
            ECVRPSolution([], [0, 1, 2, 3, 0, 4, 0], test_instance),
            ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0, 4, 0], test_instance),
            ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0], test_instance)
        ], time.thread_time())
    writer.dump()

    assert True


def test_snapshots_io(tmpdir: Path):
    """ writes meta data and snapshots to the JSON file format
    """
    writer = JsonWriter(
        str(tmpdir),
        "writter_snaps",
        "bench_test",
        "ga"
    )
    for _ in range(9):
        writer.add_snapshot([
            ECVRPSolution([], [0, 1, 2, 3, 0, 4, 0], test_instance),
            ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0, 4, 0], test_instance),
            ECVRPSolution([], [0, 1, 0, 2, 0, 3, 0], test_instance)
        ], time.thread_time())
    writer.dump()

    data = read_json(str(tmpdir), "writter_snaps")

    assert data["bench_id"] == "bench_test"
    assert len(data["snapshots"]) == 9

    assert "individuals" in data["snapshots"][0]
    assert "time" in data["snapshots"][0]

    assert len(data["snapshots"][0]["individuals"]) == 3
    assert "solution" in data["snapshots"][0]["individuals"][0]
    assert "fitness" in data["snapshots"][0]["individuals"][0]

    assert data["snapshots"][0]["individuals"][0]["solution"] == [0, 1, 2, 3, 0, 4, 0]
    assert data["snapshots"][0]["individuals"][1]["solution"] == [0, 1, 0, 2, 0, 3, 0, 4, 0]
    assert data["snapshots"][0]["individuals"][2]["solution"] == [0, 1, 0, 2, 0, 3, 0]
