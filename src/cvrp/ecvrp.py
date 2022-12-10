# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of \
the genetic algorithm applyed to the ECVRP problem.

@author: Cyril Obrecht
@author: Marie Aspro
@license: GPL-3
@date: 2022-12-08
@version: 1.2
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


from typing import Union, Sequence
from random import randrange, shuffle
import random
from .individual import Individual, ConstraintValidator


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

        self._fitness = self._compute_fitness(self.get_roads())
        return self._fitness

    def _compute_fitness(self, solution: tuple[tuple[int, ...], ...]) -> float:
        """
        Compute the fitness of the solution held in this individual.

        The fitness is, in our case, the maximal time made by a vehicle to
        delivery the designated clients. Because all the vehicle are leaving
        the depot at the same time, the fitness will be the vehicle which is
        taken the most of the time.
        """
        max_time = 0.
        for road in solution:
            current = self._compute_road_fitness(road)
            if current > max_time:
                max_time = current
        return max_time

    def _compute_road_fitness(self, road: Sequence[int]) -> float:
        road_time = 0.
        latest = road[0]
        for i in road:
            road_time += self.get_instance().get_distance(latest, i)
            latest = i
        return road_time

    def best_place_for(self, solution: list[list[int]], point: int) -> tuple[int, int]:
        """
        Find the best place to add a point to delivery.

        This function will be use to find the best place to add a point in a
        new road at the end of the crossover process.
        It will return the index of the best place and do not do the insertion
        """
        min_fit = float("inf")
        best_position = (-1, -1)
        number_roads = len(solution)
        initial_solution = solution

        for index_road, road in enumerate(initial_solution):

            size_road = len(road)
            if size_road != 2:

                # we start at index 1 because the index 0 is depot
                for index_point in range(1, size_road):
                    road.insert(index_point, point)
                    fitness = self._compute_fitness(solution)
                    if fitness < min_fit:
                        min_fit = fitness
                        best_position = (index_road, index_point)
                    road.remove(point)
            else:
                road.insert(1, point)
                fitness = self._compute_fitness(solution)
                if fitness < min_fit:
                    min_fit = fitness
                    best_position = (index_road, 1)
                road.remove(point)

            if self.__instance.get_ev_count() > number_roads:
                # If the number of roads is less than the number of vehicules,
                # the better road can be an additionnal road.
                depot = self.__instance.get_depot()
                new_road = [depot, point, depot]
                solution.append(new_road)
                fitness = self._compute_fitness(solution)
                if fitness < min_fit:
                    min_fit = fitness
                    best_position = (number_roads, 1)
                solution.remove(new_road)

        if min_fit == float("inf"):
            best_position = (number_roads, 1)

        return best_position

    def __closest_charger(self, point: int) -> int:
        """
        Find the closest charger of a point.

        This function will find the closest charger of a point and will return the id
        of the charger founded. If there is no charger, the function will return the
        depot ID.
        """
        list_chargers = self.__instance.get_chargers()
        if len(list_chargers) == 0:
            size = len(self.get_roads())
            if self.__instance.get_ev_count() > size:
                return self.__instance.get_depot()

        d_min = float("inf")
        closest = self.__instance.get_depot()
        for charger in list_chargers:
            dist = self.__instance.get_distance(point, charger)
            if dist < d_min:
                d_min = dist
                closest = charger
        return closest

    def _road_correction(self, road: list[int]) -> list[int]:
        """
        Add the closest electric charge between 2 points.

        Algorithm which is able to add the closest electric charger to the point
        where the battery would not be enough to go to the next point.
        It will use the function closestCharger() to find the most efficient solution.
        """
        valid_road: list[int] = [road[0]]
        capacity_battery = self.__instance.get_ev_battery()

        for point in road[1:]:
            charger = self.__closest_charger(point)
            if (
                    capacity_battery
                    - self.__instance.get_batterie_consumption(valid_road[-1], point)
                    < self.__instance.get_batterie_consumption(point, charger)
                    ):

                valid_road.append(self.__closest_charger(valid_road[-1]))
                capacity_battery = self.__instance.get_ev_battery()

            capacity_battery -= self.__instance.get_batterie_consumption(valid_road[-1], point)
            valid_road.append(point)

        return valid_road

    def __remove_point(self, solution: list[list[int]], element: int) -> list[list[int]]:
        """
        Remove a precised point in a solution for the crossover process.

        This function will remove a point in a solution. This point comes from the road
        which have been randomly selected from another solution.
        The same process will be done for the other solution with a road which have been
        randomly selected in this solution previously.
        """
        for road in solution:
            if element in road:
                road.remove(element)
                break
        return solution

    def __merge_roads(self, solution: list[list[int]]) -> list[int]:
        """
        Merge roads to obtain a solution in a simple list.

        The goal is to merge a list of road (which each is a list of int)
        to obtain a solution which is a list of integer (ID point).
        """
        fusion_solution: list[int] = []
        for index_road, road in enumerate(solution):
            for index_point, point in enumerate(road):
                if (index_point == 0) and (index_road == 0):
                    fusion_solution.append(point)
                elif index_point != 0:
                    # the goal is to not have 0 in duplicate
                    # which is all the time in index 0 for each road
                    fusion_solution.append(point)
        return fusion_solution

    def __pull_off_chargers(self, road: list[int]) -> list[int]:
        """
        Remove all the chargers from a solution.

        This function is helping the mutation process by removing all the chargers
        of a road. It will retrun the road without it.
        """
        for point in road:
            if self.__instance.is_charger(point):
                road.remove(point)
        return road

    def __reversed_content(self, road: list[int], index1: int, index2: int) -> list[int]:
        """Reverse the content of a road between the point 1 and 2 (included)."""
        size = len(road)

        if index1 < index2:
            index_min = index1
            index_max = index2
        else:
            index_min = index2
            index_max = index1

        begining = road[0:index_min]
        middle = road[index_min:(index_max+1)]
        middle.reverse()
        ending = road[(index_max+1):size]

        reversed_road = begining + middle + ending

        return reversed_road

    def __two_opt(self, road: list[int]) -> list[int]:
        """
        2-opt variance algorithm.

        Algorithm which find the best mutation for this road by calculating
        the distance for each mutation of road. The shortest distance will
        determine the best muatation road.
        """
        best_distance = self._compute_road_fitness(road)
        best_road = road

        depot = self.__instance.get_depot()

        road.remove(depot)  # remove the first depot
        road.remove(depot)  # remove the last depot

        for index_point1 in range(len(road)):
            for index_point2 in range(index_point1):
                if index_point1 != index_point2:
                    tmp_road = self.__reversed_content(road, index_point1, index_point2)
                    tmp_road.insert(0, depot)  # add the depot at the begining
                    tmp_road.append(depot)  # add the depot at the end
                    distance = self._compute_road_fitness(tmp_road)
                    if distance < best_distance:
                        best_distance = distance
                        best_road = tmp_road

        return best_road

    def _delete_empty_road(self, solution: list[list[int]]) -> list[list[int]]:
        """Delete empty road which are represented by [0, 0] if depot is 0."""
        depot = self.__instance.get_depot()
        for road in solution:
            if road == [depot, depot]:
                solution.remove(road)
        return solution

    def mutate(self) -> None:
        """
        Mutate the current individual according to its internal rules.

        This changement is done in place.
        """
        solution_tuple = self.get_roads()
        solution = tuple_to_list(solution_tuple)

        index_road = random.choice(range(len(solution)))
        road = solution[index_road]

        road_without_chargers = self.__pull_off_chargers(road)

        # algo 2-opt
        mutant_road = self.__two_opt(road_without_chargers)

        new_road = self._road_correction(mutant_road)
        solution[index_road] = new_road

        solution = self._delete_empty_road(solution)

        self._solution = self.__merge_roads(solution)

    def __get_solution(self) -> list[list[int]]:
        """
        Get solutions from ECVRPSolution and prepare it for crossover process.

        It takes place at the beginning of the crossover method to get the solution from
        the ECVRPSolution and convert it into a list of list. Moreover, it will remove
        all the chargers from the solution.
        """
        s_tuple = self.get_roads()

        # convert tuple into list to modify th content
        solution = tuple_to_list(s_tuple)

        # pull of charger for the crossover opration
        for index_road, road in enumerate(solution):
            solution[index_road] = self.__pull_off_chargers(road)

        return solution

    def __choose_road(self, solution: list[list[int]]) -> list[int]:
        """Choose the roads from which the points will be removed from the solution."""
        # determine which road is chosen
        num_r = randrange(0, len(solution))

        # road are without depot at the begging and ending
        road = list(solution[num_r])[1:-1]

        return road

    def __insert_points(self, solution: list[list[int]], road: list[int]) -> list[list[int]]:
        """Insert at a better place the points removed previously."""
        # insert in the best place for removed points
        shuffle(road)
        for point in road:
            position = self.best_place_for(solution, point)
            if position[0] == len(solution):
                solution.append([0, 0])
            solution[position[0]].insert(position[1], point)

        return solution

    def __update_solution(self, solution: list[list[int]]) -> list[int]:
        """
        End of the crossover process by reshaping a validate solution.

        After the points have been removed and inserted at a better place, the solution
        must be correct to be valid by adding chargers if needed. Moreover, empty roads
        should be deleted to have a suitable solution and finally merge the roads to
        reshape it from his original form.
        """
        # add chargers
        for index_road, road in enumerate(solution):
            solution[index_road] = self._road_correction(road)

        # delete empty road
        solution = self._delete_empty_road(solution)

        # merge my list of road to list of point
        final_solution = self.__merge_roads(solution)

        return final_solution

    def crossover(self, other: "ECVRPSolution") -> list["ECVRPSolution"]:
        """
        Generate a list of children according to the rules of the individual.

        The returned list might be empty or contains duplicated children.
        This function might not return the same result with the same argument and
        will probably not be comutative.
        """

        s_1 = self.__get_solution()
        s_2 = other.__get_solution()

        road_1 = self.__choose_road(s_1)
        road_2 = self.__choose_road(s_2)

        # points are removed
        for point in road_1:
            s_2 = self.__remove_point(s_2, point)

        for point in road_2:
            s_1 = self.__remove_point(s_1, point)

        s_1 = self.__insert_points(s_1, road_2)
        s_2 = self.__insert_points(s_2, road_1)

        s_1 = self.__update_solution(s_1)
        s_2 = self.__update_solution(s_2)

        # create children
        e_1 = ECVRPSolution(self._validators, s_1, self.__instance)

        e_2 = ECVRPSolution(self._validators, s_2, self.__instance)

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


def tuple_to_list(tuple_element: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    """Convert a tuple[tuple[int]] into a list[list[int]]."""
    return [list(x) for x in tuple_element]


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

    def get_depot(self) -> int:
        """Return the ID of the depot."""
        return self.__depot

    def get_distance(self, start: int, end: int) -> float:
        """Return the distance between start and end."""
        return self.__d_matrix[start][end]

    def get_time_used(self, start: int, end: int) -> float:
        """Return the time took by a vehicule to go from start to end."""
        return self.__d_matrix[start][end]

    def get_chargers(self) -> set[int]:
        """Return the set of chargers."""
        return self.__chargers

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

    def get_ev_count(self) -> int:
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
