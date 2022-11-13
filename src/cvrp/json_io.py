# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of
the genetic algorithm applyed to the ECVRP problem.

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

from pathlib import Path
from bz2 import BZ2File
import json

from .ecvrp import ECVRPSolution


class json_writer:
    """
    Class handling the writing of information to a specific JSON file with pre defined structure.
    In order to limit the space cost of those files they are compressed with bz2.
    """
    def __init__(
                self,
                root: str,
                name: str,
                bench_name: str
            ):
        self.__snapshots = []
        self.__root = Path(root)
        self.__name = name
        self.__bench_name = bench_name

    def add_snapshot(self, snapshot: list[ECVRPSolution], time: float):
        """
        Adds a snapshot to the structure. T
        he snapshots are dumped in the same order as provided.
        Hence if you want to retrosctively add new snapshots between existing,
        make sure that you handle this at read time.
        """
        generation = {"time": time, "individuals": []}

        for individual in snapshot:
            generation["individuals"].append({
                "solution": individual.get_points(),
                "fitness": individual.get_fitness()
            })

        self.__snapshots.append(generation)

    def dump(self):
        """
        Dumps all the collected data to the file name `root/name.json.bz2`.
        This method will override any existing file without warning.
        """
        data = {
            "bench_id": self.__bench_name,
            "snapshots": self.__snapshots
        }
        with BZ2File(str(self.__root.joinpath(f"{self.__name}.json.bz2")), "wb") as file:
            dump = bytearray(json.dumps(data).encode("ascii"))
            file.write(dump)
            file.close()
