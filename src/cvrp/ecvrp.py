# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of \
the genetic algorithm applyed to the ECVRP problem.

@author: Cyril Obrecht and Marie Aspro
@license: GPL-3
@date: 2022-11-17
@version: 0.6
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
from random import random
from .individual import Individual, TypeIndividual, ConstraintValidator


class ECVRPSolution(Individual["ECVRPSolution"]):
    """
    Holds a solution to the ECVRP problem and methods to help with a GA.

    Mutations is either done via 2-opt or a special algorithm.
    See the mutate method for more information on this subject.
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
        """
        Initialise the ECVRPSolution class.

        :param validators: A list of validator used to determine if the instance is valid.
        This list will be trasmitted to children.
        :param solution: A list of indexes that represent a solution to the ECVRP instace
        :param instance: The instance this object aims to represent a solution.
        """
        super().__init__(validators)
        self._solution = solution
        self.__instance = instance
        self._roads = None
        self._fitness = None

    def get_instance(self) -> "ECVRPInstance":
        """Return the instance linked to this solution."""
        return self.__instance

    def get_points(self) -> tuple[int, ...]:
        """Return the solution in an imutable form."""
        return tuple(self._solution)

    def get_roads(self) -> tuple[tuple[int, ...], ...]:
        """Split the solution in individual roads that can be manipulated \
        without altering the main object."""
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
        """
        Compute the fitness of the solution held in this individual.

        The fitness is here defined as the maximum amount
        of time taken by an EV to travel a road.
        The time taken to go from the town A to B is equals to the distance between those towns.
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

    def best_place_for(self, solution: list[list[int]], i_point: int) -> int:
        """
        Find the best place to add a point to delivery.

        This function will be use to find the best place to add a point in a
        new road at the end of the crossover process.
        It will return the index of the best place and do not do the insertion
        """
        min_fit = float('inf')
        best_position = -1
        solution = self.merge_roads(solution)
        size = len(solution)

        for position in range(size):
            solution.insert(position, i_point)
            fitness = solution.get_fitness()
            if fitness < min_fit:
                min_fit = fitness
                best_position = position
            solution.remove(i_point)

        if min_fit == float('inf'):
            best_position = size + 1

        return best_position

    def closest_charger(self, point: int) -> int:
        """
        Find the closest charger of a point.

        This function will find the closest charger of a point and will return the id
        of the charger founded.
        """
        list_chargers = self.__chargers
        if not list_chargers:
            return self.__depot

        d_min = self.get_distance(point, list_chargers[0])
        closest = list_chargers[0]
        for charger in list_chargers:
            dist = self.get_distance(point, charger)
            if dist < d_min:
                d_min = dist
                closest = charger
        return closest

    def last(self, road: list[int]) -> int:
        """ Useful function that will return the last point of a road."""
        return road[-1]

    def road_correction(self, road: list[int], battery: int) -> list[int]:
        """
        Add the closest electric charge beatween 2 points.

        Algorithm which is able to add the closest electric charger to the point
        where the battery would not be enough to go to the next point.
        It will use the function closestCharger() to find the most efficient solution.
        """
        valid_road = [int]
        capacity_battery = battery

        for point in road:
            charger = self.closest_charger(point)
            if (capacity_battery - self.get_batterie_consumption(self.last(valid_road), point)
                    < self.get_batterie_consumption(point, charger)):
                valid_road.append(self.closest_charger(self.last(valid_road)))
                capacity_battery = battery
            capacity_battery = capacity_battery
            - self.get_batterie_consumption(self.last(valid_road), point)
            valid_road.append(point)

        return valid_road

    def remove_point(self, solution: list[list[int]], element: int) -> list[list[int]]:
        """
        Remove a precised point in a solution for the crossover process.

        This function will remove a point in a solution. This point comes from the road
        which have been randomly selected from another solution.
        The same process will be done for the other solution with a road which have been
        randomly selected in this solution previously.
        """
        for road in solution:
            for point in road:
                if point == element:
                    road.remouve(element)
        return solution

    def tuple_to_list(self, tuple_element: tuple[tuple[int]]) -> list[list[int]]:
        """Convert a tuple[tuple[int] into a list[list[int]]."""
        return [list(x) for x in tuple_element]

    def merge_roads(self, solution: list[list[int]]) -> list[int]:
        """
        Merge roads to obtain a solution in a simple list.

        The goal is to merge a list of road (which each is a list of int)
        to obtain a solution which is a list of integer (ID point).
        """
        fusion_solution = list[int]
        for index_road, road in enumerate(solution):
            for index_point, point in enumerate(road):
                if (index_point == 0) and (index_road == 0):
                    fusion_solution.append(point)
                elif index_point != 0:
                    # the goal is to not have 0 in duplicate
                    # which is all the time in index 0 for each road
                    fusion_solution.append(point)
        return fusion_solution

    def pull_off_chargers(self, road: list[int]) -> list[int]:
        """
        Remove all the chargers from a solution.

        This function is helping the mutation process by removing all the chargers
        of a road. It will retrun the road without it.
        """
        for point in road:
            if self.is_charger(point):
                road.remove(point)
        return road

    def get_road_distance(self, road: list[int]) -> float:
        """
        Calculate the total distance of a road.

        This function will use get_distance which is able to determine
        the distance between 2 points given.
        """
        total = 0.0
        size = len(road)
        for i in range(size):
            if i != (size - 1):
                total = total + self.get_distance(road[i], road[i + 1])
            else:
                total = total + self.get_distance(road[i], road[0])
        return total

    def reversed_content(self, road: list[int], point1: int, point2: int) -> list[int]:
        """Reverse the content of a road between the point 1 and 2 (included)."""
        index1 = road.index(point1)
        index2 = road.index(point2)
        size = len(road)

        if index1 < index2:
            index_min = index1
            index_max = index2
        else:
            index_min = index2
            index_max = index1

        begining = road[0:index_min]
        middle = road[index_min:(index_max+1)]
        middle.reversed()
        ending = road[(index_max+1):size]

        reversed_road = begining + middle + ending

        return reversed_road

    def two_opt(self, road: list[int]) -> list[int]:
        """
        2-opt variance algorithm.

        Algorithm which find the best mutation for this road by calculating
        the distance for each mutation of road. The shortest distance will
        determine the best muatation road.
        """
        best_distance = self.get_road_distance(road)
        best_road = road

        road.remove(0)  # remove the first depot
        road.remove(0)  # remove the last depot

        for point1 in road:
            for point2 in road:
                if point1 != point2:
                    tmp_road = self.reversed_content(road, point1, point2)
                    tmp_road.insert(0, 0)  # add the depot at the begining
                    tmp_road.append(0)  # add the depot at the end
                    distance = self.get_road_distance(tmp_road)
                    if distance < best_distance:
                        best_distance = distance
                        best_road = tmp_road

        return best_road

    def mutate(self) -> None:
        """
        Mutate the current individual according to its internal rules.

        This changement is done in place.
        """
        solution = self.get_roads()
        solution = self.tuple_to_list(solution)

        choice = random(0, len(solution))
        road = solution[choice]

        road = self.pull_off_chargers(road)

        # algo 2-opt
        mutant_road = self.two_opt(road)

        new_road = self.road_correction(mutant_road, self.get_ev_battery())

        new_solution = list[list[int]]
        new_solution = solution
        new_solution[choice] = new_road

        self._solution = new_solution

    def crossover(self, other: TypeIndividual) -> list[TypeIndividual]:
        """
        Generate a list of children according to the rules of the individual.

        The returned list might be empty or contains duplicated children.
        This function might not return the same result with the same argument and
        will probably not be comutative.
        """
        s_1 = self.get_roads()  # self is the parent 1
        s_2 = other.get_roads()

        # convert tuple into list to modify th content
        s_1 = self.tuple_to_list(s_1)
        s_2 = self.tuple_to_list(s_2)

        num_r_1 = random(0, len(s_1))
        num_r_2 = random(0, len(s_2))
        road_1 = list(map(lambda r: r[num_r_1], s_1))
        road_2 = list(map(lambda r: r[num_r_2], s_2))

        list_point_s_2 = list[int]
        for point in road_1:
            element, s_2 = self.remove_point(point, s_2)
            list_point_s_2.append(element)

        list_point_s_1 = list[int]
        for point in road_2:
            if point != 0:
                s_1 = self.remove_point(point, s_1)
                list_point_s_1.append(point)

        s_1 = self.merge_roads(s_1)
        s_2 = self.merge_roads(s_2)

        for point in list_point_s_1:
            s_1.insert(self.best_place_for(s_1, point), point)

        for point in list_point_s_2:
            s_2.insert(self.best_place_for(s_2, point), point)

        e_1 = TypeIndividual()
        e_1._solution = s_1

        e_2 = TypeIndividual()
        e_2._solution = s_2

        return [e_1, e_2]

    def is_valid(self) -> bool:
        """Run all of its validator and return False if one of them fail."""
        return len([v for v in self._validators if not v.is_valid(self)]) == 0

    def __copy__(self) -> "ECVRPSolution":
        """Create a copy."""
        copy = ECVRPSolution(list(self._validators), list(self._solution), self.__instance)
        copy._fitness = self._fitness
        copy._roads = self._roads
        return copy


class ECVRPInstance:
    """Holding class for most of the information that describe an instance of the ECVRP problem."""

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
        """Initialize the instance class."""
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
        """Return True if the given index is a depot."""
        return index == self.__depot

    def get_distance(self, start: int, end: int) -> float:
        """Return the distance between start and end."""
        return self.__d_matrix[start][end]

    def get_time_used(self, start: int, end: int) -> float:
        """Return the time took by a vehicule to go from start to end."""
        return self.__d_matrix[start][end]

    def is_charger(self, index: int) -> bool:
        """Return True if the given index is a charger."""
        return index in self.__chargers

    def get_demand(self, index: int) -> int:
        """
        Return the demand of the point at the given index.

        May raise an exception if the index is a depot or a charger.
        Will raise one if the index is out of bounds
        """
        return self.__demands[index]

    def get_batterie_consumption(self, start: int, end: int) -> int:
        """Return the amount of energy consumed by a vehicule to go from start to end."""
        return round(self.get_distance(start, end) * self.__bat_cost)

    def get_batterie_charging_rate(self) -> float:
        """Return the speed at witch betteries charges."""
        return self.__bat_charge

    def get_ev_count(self) -> float:
        """Return the maximum number of EV allowed."""
        return self.__ev_count

    def get_ev_capacity(self) -> float:
        """Return the cargot capacity of an EV."""
        return self.__ev_capacity

    def get_ev_battery(self) -> float:
        """Return the battery capacity of an EV."""
        return self.__ev_battery

    def get_tw(self, index: int) -> tuple[float, float]:
        """Return tha time window to deliver the point at the given index."""
        return self.__time_windows[index]

    def get_towns(self) -> list[int]:
        """Return all points that are not a depot or a charger."""
        return [
            i for i in range(len(self.__d_matrix)) if not (self.is_depot(i) or self.is_charger(i))
        ]
