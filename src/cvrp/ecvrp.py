# -*- coding: utf-8 -*-

"""
<<<<<<< HEAD
This module holds parts of the implementation of
the genetic algorithm applyed to the ECVRP problem.

@author: Cyril Obrecht
@license: GPL-3
@date: 2022-11-02
@version: 0.1
=======
This module holds parts of the implementation of \
the genetic algorithm applyed to the ECVRP problem.

@author: Cyril Obrecht and Marie Aspro
@license: GPL-3
@date: 2022-11-17
@version: 0.6
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
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
<<<<<<< HEAD


class ECVRPSolution(Individual["ECVRPSolution"]):
    """ Holds a solution to the ECVRP problem and methods to help with a GA
        Mutations is either done via 2-opt or a special algorithm.
        See the mutate method for more information on this subject
=======
import random


class ECVRPSolution(Individual["ECVRPSolution"]):
    """
    Holds a solution to the ECVRP problem and methods to help with a GA.

    Mutations is either done via 2-opt or a special algorithm.
    See the mutate method for more information on this subject.
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
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
<<<<<<< HEAD
=======
        """
        Initialise the ECVRPSolution class.

        :param validators: A list of validator used to determine if the instance is valid.
        This list will be trasmitted to children.
        :param solution: A list of indexes that represent a solution to the ECVRP instace
        :param instance: The instance this object aims to represent a solution.
        """
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        super().__init__(validators)
        self._solution = solution
        self.__instance = instance
        self._roads = None
        self._fitness = None

    def get_instance(self) -> "ECVRPInstance":
<<<<<<< HEAD
        return self.__instance

    def get_points(self) -> tuple[int, ...]:
        return tuple(self._solution)

    def get_roads(self) -> tuple[tuple[int, ...], ...]:
        """ Split the solution in individual roads that can be manipulated
            without altering the main object.
        """
=======
        """Return the instance linked to this solution."""
        return self.__instance

    def get_points(self) -> tuple[int, ...]:
        """Return the solution in an imutable form."""
        return tuple(self._solution)

    def get_roads(self) -> tuple[tuple[int, ...], ...]:
        """Split the solution in individual roads that can be manipulated \
        without altering the main object."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
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
<<<<<<< HEAD
        """ Compute the fitness of the solution held in this individual
            The fitness is here defined as the maximum amount
            of time taken by an EV to travel a road.
            The time taken to go from the town A to B is equals to the distance between those towns
=======
        """
        Compute the fitness of the solution held in this individual.

        The fitness is here defined as the maximum amount
        of time taken by an EV to travel a road.
        The time taken to go from the town A to B is equals to the distance between those towns.
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
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

<<<<<<< HEAD
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
        return len([v for v in self._validators if not v.is_valid(self)]) == 0

    def __copy__(self) -> "ECVRPSolution":
=======
    def best_place_for(self, solution: list[list[int]], I_point: int) -> int:
        """
        Find the best place to add a point to delivery.

        This function will be use to find the best place to add a point in a
        new road at the end of the crossover process.
        It will return the index of the best place and do not do the insertion
        """
        minFit = float('inf')
        bestPosition = -1
        solution = self.merge_roads(solution)
        size = len(solution)

        for position in range(size):
            solution.insert(position, I_point)
            fitness = solution.get_fitness()
            if (fitness < minFit):
                minFit = fitness
                bestPosition = position
            solution.remove(I_point)

        if (minFit == float('inf')):
            bestPosition = size + 1

        return bestPosition

    def closest_charger(self, point: int) -> int:
        """
        Find the closest charger of a point.

        This function will find the closest charger of a point and will return the id
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

    def road_correction(self, road: list[int], Battery: int) -> list[int]:
        """
        Add the closest electric charge beatween 2 points.

        Algorithm which is able to add the closest electric charger to the point
        where the battery would not be enough to go to the next point.
        It will use the function closestCharger() to find the most efficient solution.
        """
        validRoad = [int]
        b = Battery

        for point in road:
            charger = self.closest_charger(point)
            if (b - self.get_batterie_consumption(self.last(validRoad), point)
                    < self.get_batterie_consumption(point, charger)):
                validRoad.append(self.closest_charger(self.last(validRoad)))
                b = Battery
            b = b - self.get_batterie_consumption(self.last(validRoad), point)
            validRoad.append(point)

        return validRoad

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
                if (point == element):
                    road.remouve(element)
        return solution

    """
    def insert_point(self, position: tuple[int, int], solution: list[list[int]], element: int) -> list[list[int]]:

        Insert a point at the best place for the crossover process.

        This function will take the best position to add a point into a solution.
        It will be call at the end of the crossover method and required the method
        best_place_for to obtain which road and before which client it will be insert.

        for road in solution:
            if (road == position[0]):
                for point in road:
                    if (point == position[1]):
                        solution.insert((road, point), element)
        return solution
    """

    def tuple_to_list(self, t: tuple[tuple[int]]) -> list[list[int]]:
        """Convert a tuple[tuple[int] into a list[list[int]]."""
        return [list(x) for x in t]

    def merge_roads(self, solution: list[list[int]]) -> list[int]:
        """
        Merge roads to obtain a solution in a simple list.

        The goal is to merge a list of road (which each is a list of int)
        to obtain a solution which is a list of integer (ID point).
        """
        fusionSolution = list[int]
        for index_road, road in enumerate(solution):
            for index_point, point in enumerate(road):
                if (index_point == 0) and (index_road == 0):
                    fusionSolution.append(point)
                elif (index_point != 0):
                    # the goal is to not have 0 in duplicate
                    # which is all the time in index 0 for each road
                    fusionSolution.append(point)
        return fusionSolution

    def pull_off_chargers(self, solution: list[list[int]]) -> tuple[list[list[int]], list[int]]:
        listChargers = list[int]
        for road in solution:
            for point in road:
                if (self.is_charger(point)):
                    listChargers.append(point)
                    solution.remove(point)
        return solution, listChargers

    def get_road_distance(self, road: list[int]) -> float:
        """
        Calculate the total distance of a road.

        This function will use get_distance which is able to determine
        the distance between 2 points given.
        """
        total = 0.0
        size = len(road)
        for i in range(size):
            if (i != (size - 1)):
                total = total + self.get_distance(road[i], road[i + 1])
            else:
                total = total + self.get_distance(road[i], road[0])
        return total

    def reversed_content(self, road: list[int], point1: int, point2: int) -> list[int]:
        """Reverse the content of a road between the point 1 and 2 (included)."""
        index1 = road.index(point1)
        index2 = road.index(point2)
        size = len(road)

        if (index1 < index2):
            indexMin = index1
            indexMax = index2
        else:
            indexMin = index2
            indexMax = index1

        begining = road[0:indexMin]
        middle = road[indexMin:(indexMax+1)]
        middle.reversed()
        ending = road[(indexMax+1):size]

        reversedRoad = begining + middle + ending

        return reversedRoad

    def two_opt(self, road: list[int]) -> list[int]:
        """
        2-opt variance algorithm.

        Algorithm which find the best mutation for this road by calculating
        the distance for each mutation of road. The shortest distance will 
        determine the best muatation road.
        """
        bestDistance = self.get_road_distance(road)
        bestRoad = road

        road.remove(0)  # remove the first depot
        road.remove(0)  # remove the last depot

        for point1 in road:
            for point2 in road:
                if (point1 != point2):
                    tmpRoad = self.reversed_content(road, point1, point2)
                    tmpRoad.insert(0, 0)  # add the depot at the begining
                    tmpRoad.append(0)  # add the depot at the end
                    distance = self.get_road_distance(tmpRoad)
                    if (distance < bestDistance):
                        bestDistance = distance
                        bestRoad = tmpRoad

        return bestRoad

    def mutate(self) -> None:
        """
        Mutate the current individual according to its internal rules.

        This changement is done in place.
        """
        solution = self.get_roads()
        solution = self.tuple_to_list(solution)

        choice = random(0, len(solution))
        road = solution[choice]

        road, listChargers = self.pull_off_chargers(road)

        # algo 2-opt
        mutantRoad = self.two_opt(road)

        newRoad = self.road_correction(mutantRoad, self.get_ev_battery())

        newSolution = list[list[int]]
        newSolution = solution
        newSolution[choice] = newRoad

        self._solution = newSolution
        return

    def crossover(self, parent2: TypeIndividual) -> list[TypeIndividual]:
        """
        Generate a list of children according to the rules of the individual.

        The returned list might be empty or contains duplicated children.
        This function might not return the same result with the same argument and
        will probably not be comutative.
        """
        S1 = self.get_roads()  # self is the parent 1
        S2 = parent2.get_roads()

        # convert S1 and S2 in list[list[int]]
        S1 = self.tuple_to_list(S1)
        S2 = self.tuple_to_list(S2)

        num_r1 = random(0, len(S1))
        num_r2 = random(0, len(S2))
        road1 = list(map(lambda r: r[num_r1], S1))
        road2 = list(map(lambda r: r[num_r2], S2))

        listPointS2 = list[int]
        for point in road1:
            element, S2 = self.remove_point(point, S2)
            listPointS2.append(element)

        listPointS1 = list[int]
        for point in road2:
            if (point != 0):
                S1 = self.remove_point(point, S1)
                listPointS1.append(point)

        # convert into list[int] S1 and S2 and delate depot excess
        S1 = self.merge_roads(S1)
        S2 = self.merge_roads(S2)

        for point in listPointS1:
            S1.insert(self.best_place_for(S1, point), point)

        for point in listPointS2:
            S2.insert(self.best_place_for(S2, point), point)

        E1 = TypeIndividual()
        E1._solution = S1

        E2 = TypeIndividual()
        E2._solution = S2

        return [E1, E2]

    def is_valid(self) -> bool:
        """Run all of its validator and return False if one of them fail."""
        return len([v for v in self._validators if not v.is_valid(self)]) == 0

    def __copy__(self) -> "ECVRPSolution":
        """Create a copy."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        copy = ECVRPSolution(list(self._validators), list(self._solution), self.__instance)
        copy._fitness = self._fitness
        copy._roads = self._roads
        return copy


class ECVRPInstance:
<<<<<<< HEAD
    """
        holding class for most of the information that describe an instance of the ECVRP problem
    """
=======
    """Holding class for most of the information that describe an instance of the ECVRP problem."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1

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
<<<<<<< HEAD
=======
        """Initialize the instance class."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
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
<<<<<<< HEAD
        return index == self.__depot

    def get_distance(self, start: int, end: int) -> float:
        return self.__d_matrix[start][end]

    def get_time_used(self, start: int, end: int) -> float:
        return self.__d_matrix[start][end]

    def is_charger(self, index: int) -> bool:
        return index in self.__chargers

    def get_demand(self, index: int) -> int:
        return self.__demands[index]

    def get_batterie_consuption(self, start: int, end: int) -> int:
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
=======
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
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        return [
            i for i in range(len(self.__d_matrix)) if not (self.is_depot(i) or self.is_charger(i))
        ]
