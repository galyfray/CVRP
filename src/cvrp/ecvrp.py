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

from .individual import Individual, TypeIndividual, ConstraintValidator


class ECVRPSolution(Individual["ECVRPSolution"]):
    """ Holds a solution to the ECVRP problem and methods to help with a GA
        Mutations is either done via 2-opt or a special algorithm.
        See the mutate method for more information on this subject
    """

    def __init__(
            self,
            validators: list[ConstraintValidator],
            solution: list[int],
            instance: "ECVRPInstance"
            ) -> None:
        super().__init__(validators)
        self._solution = solution
        self.__instance = instance
        self._roads = None
        self._fitness = None

    def get_instance(self) -> "ECVRPInstance":
        return self.__instance

    def get_points(self) -> tuple[int]:
        return tuple(self._solution)

    def get_roads(self) -> tuple[tuple[int]]:
        """ Split the solution in individual roads that can be manipulated
            without altering the main object.
        """
        if self._roads is not None:
            return self._roads

        i = 0
        roads = []
        while i < len(self._solution) - 1:
            current = []
            current.append(self._solution[i])
            i += 1
            while self._solution[i] != current[0]:
                current.append(self._solution[i])
                i += 1

            current.append(current[0])
            roads.append(tuple(current))
        self._roads = tuple(roads)
        return self._roads

    def get_fitness(self) -> float:
        """ Compute the fitness of the solution held in this individual
            The fitness is here defined as the maximum amount
            of time taken by an EV to travel a road.
            The time taken to go from the town A to B is equals to the distance between those towns
        """
        if self._fitness is not None:
            return self._fitness
        max_time = 0
        current = 0
        for road in self.get_roads():
            current = self._compute_road_fitness(road)
            if current > max_time:
                max_time = current
        self._fitness = max_time
        return self._fitness

    def _compute_road_fitness(self, road: tuple[int]) -> float:
        road_time = 0
        latest = road[0]
        for i in road:
            road_time += self.get_instance().get_distance(latest, i)
            latest = i
        return road_time

    def mutate(self) -> None:
        """ Mutate the current individual according to its internal rules.
            This changement is done in place.
        """

    def crossover(self, other: TypeIndividual) -> list[TypeIndividual]:
        """ Generate a list of children according to the rules of the individual.
            The returned list might be empty or contains duplicated children.
            This function might not return the same result with the same argument and
            will probably not be comutative.
        """

    def is_valid(self) -> bool:
        return True

    def __copy__(self) -> TypeIndividual:
        pass


class ECVRPInstance:
    """
        holding class for most of the information that describe an instance of the ECVRP problem
    """
    def __init__(
            self,
            distance_matrix: list[list[float]],
            depot_id: int,
            chargers: set[int],
            demands: dict[int, int],
            batterie_cost_factor: float,
            batterie_charge_rate: float,
            ev_count: int,
            ev_capacity: float,
            ev_battery: float
            ) -> None:
        self.__d_matrix = distance_matrix
        self.__depot = depot_id
        self.__chargers = chargers
        self.__demands = demands
        self.__bat_cost = batterie_cost_factor
        self.__bat_charge = batterie_charge_rate
        self.__ev_count = ev_count
        self.__ev_battery = ev_battery
        self.__ev_capacity = ev_capacity

    def is_depot(self, index: int) -> bool:
        return index == self.__depot

    def get_distance(self, start: int, end: int) -> float:
        return self.__d_matrix[start][end]

    def is_charger(self, index: int) -> bool:
        return index in self.__chargers

    def get_demand(self, index: int) -> int:
        return self.__demands[index]

    def get_batterie_consuption(self, start: int, end: int) -> int:
        return self.get_distance(start, end) * self.__bat_cost

    def get_batterie_charging_rate(self) -> float:
        return self.__bat_charge

    def get_ev_count(self) -> float:
        return self.__ev_count

    def get_ev_capacity(self) -> float:
        return self.__ev_capacity

    def get_ev_battery(self) -> float:
        return self.__ev_battery
