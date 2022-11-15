# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of
the genetic algorithm applyed to the ECVRP problem.

@author: Cyril Obrecht and Marie Aspro
@license: GPL-3
@date: 2022-11-10
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


from typing import Union
from .individual import Individual, TypeIndividual, ConstraintValidator
import random


class ECVRPSolution(Individual["ECVRPSolution"]):
    """ Holds a solution to the ECVRP problem and methods to help with a GA
        Mutations is either done via 2-opt or a special algorithm.
        See the mutate method for more information on this subject
    """

    _roads: Union[tuple[tuple[int, ...], ...], None]
    _fitness: Union[float, None]
    _solution: list[int]
    __instance: "ECVRPInstance"

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

    def get_points(self) -> tuple[int, ...]:
        return tuple(self._solution)

    def get_roads(self) -> tuple[tuple[int, ...], ...]:
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
        max_time = 0.
        for road in self.get_roads():
            current = self._compute_road_fitness(road)
            if current > max_time:
                max_time = current
        self._fitness = max_time
        return self._fitness

    def _compute_road_fitness(self, road: tuple[int]) -> float:
        road_time = 0.
        latest = road[0]
        for i in road:
            road_time += self.get_instance().get_distance(latest, i)
            latest = i
        return road_time

    def bestPlaceFor(self, S: list[int], I_point: int) -> int:
        """ This function will be use to find the best place to add a point in a
            new road at the end of the crossover process.
            It will return the index of the best place and do not do the insertion
        """
        # TODO : continue here

    def closestCharger(self, point: int) -> int:
        """ This function will find the closest charger of a point and will return the id
            of the charger founded.
        """
        listChargers = self.__chargers
        if (not listChargers):
            return self.__depot
        else:
            d_min = self.get_distance(point, listChargers[0])
            closest = listChargers[0]
            for charger in listChargers:
                dist = self.get_distance(point, charger)
                if (dist < d_min):
                    d_min = dist
                    closest = charger
            return closest

    def last(self, road: list[int]) -> int:
        """ Useful function that will return the last point of a road."""
        return road[-1]

    def roadCorrection(self, road: list[int], Battery: int) -> list[int]:
        """ Algorithm which is able to add the closest electric charger to the point
            where the battery would not be enough to go to the next point.
            It will use the function closestCharger() to find the most efficient solution.
        """
        validRoad = [int]
        b = Battery
        for point in road:
            charger = self.closestCharger(point)
            if (b - self.get_batterie_consumption(self.last(validRoad), point) < self.get_batterie_consumption(point, charger)):
                validRoad.append(self.closestCharger(self.last(validRoad)))
                b = Battery
            b = b - self.get_batterie_consumption(self.last(validRoad), point)
            validRoad.append(point)
        return validRoad

    def cutInRoads(self, solution: list[int]) -> list[list[int]]:
        """ cutInRoads have to cut a list of solution made of more than 1 road
            (mean : you are going to the depot more than when you begin and you end)
            in a list of road (which are already smaller list).
        """
        new_solution = [[int]]
        list_temp = [int]
        id_depot = self.__depot
        for point in solution:
            if (point != id_depot) or (point.index() == 0):
                list_temp.append(point)
            elif (point == id_depot) and (point.index() != 0):
                list_temp.append(point)
                new_solution.append(list_temp)
                list_temp = []
                list_temp.append(point)
        return new_solution

    def mutate(self, S: list[int]) -> list[int]:
        """ Mutate the current individual according to its internal rules.
            This changement is done in place.
        """
        S = self.cutInRoads(S)
        # TODO : continue here
        return S

    def crossover(self, S1: list[int], S2: list[int]) -> list[TypeIndividual]:
        """ Generate a list of children according to the rules of the individual.
            The returned list might be empty or contains duplicated children.
            This function might not return the same result with the same argument and
            will probably not be comutative.
        """
        S1 = self.cutInRoads(S1)
        S2 = self.cutInRoads(S2)
        num_r1 = random(0, len(S1))
        num_r2 = random(0, len(S2))
        road1 = list(map(lambda r: r[num_r1], S1))
        road2 = list(map(lambda r: r[num_r2], S2))
        
        size_S1 = len(S1)
        for row in range(size_S1):
            for col in range(size_S1):
                

        # TODO : continue here

    def is_valid(self) -> bool:
        return len([v for v in self._validators if not v.is_valid(self)]) == 0

    def __copy__(self) -> "ECVRPSolution":
        copy = ECVRPSolution(list(self._validators), list(self._solution), self.__instance)
        copy._fitness = self._fitness
        copy._roads = self._roads
        return copy


class ECVRPInstance:
    """
        holding class for most of the information that describe an instance of the ECVRP problem
    """

    __d_matrix: list[list[float]]
    __depot: int
    __chargers: set[int]
    __demands: dict[int, int]
    __bat_cost: float
    __bat_charge: float
    __ev_count: int
    __ev_battery: float
    __ev_capacity: float
    __time_windows: dict[int, tuple[float, float]]

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
            ev_battery: float,
            time_windows: dict[int, tuple[float, float]]
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
        self.__time_windows = time_windows

    def is_depot(self, index: int) -> bool:
        return index == self.__depot

    def get_distance(self, start: int, end: int) -> float:
        return self.__d_matrix[start][end]

    def get_time_used(self, start: int, end: int) -> float:
        return self.__d_matrix[start][end]

    def is_charger(self, index: int) -> bool:
        return index in self.__chargers

    def get_demand(self, index: int) -> int:
        return self.__demands[index]

    def get_batterie_consumption(self, start: int, end: int) -> int:
        return round(self.get_distance(start, end) * self.__bat_cost)

    def get_batterie_charging_rate(self) -> float:
        return self.__bat_charge

    def get_ev_count(self) -> float:
        return self.__ev_count

    def get_ev_capacity(self) -> float:
        return self.__ev_capacity

    def get_ev_battery(self) -> float:
        return self.__ev_battery

    def get_tw(self, index: int) -> tuple[float, float]:
        return self.__time_windows[index]

    def get_towns(self) -> list[int]:
        return [
            i for i in range(len(self.__d_matrix)) if not (self.is_depot(i) or self.is_charger(i))
        ]
