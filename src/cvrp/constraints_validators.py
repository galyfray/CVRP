# -*- coding: utf-8 -*-

"""
<<<<<<< HEAD
This module holds the various constraint validators used to configure the ECVRP
=======
This module holds the various constraint validators used to configure the ECVRP.
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1

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


from .individual import ConstraintValidator
from .ecvrp import ECVRPSolution


# pylint: disable=too-few-public-methods
class BatteryTWValidator(ConstraintValidator[ECVRPSolution]):
<<<<<<< HEAD
    """
    Class in charge of checking if the battery capacity is never exceeded
    and if the time windows are respected
    """
    def is_valid(self, individual: ECVRPSolution) -> bool:
=======
    """Class in charge of checking if the battery capacity is never exceeded \
    and if the time windows are respected."""

    def is_valid(self, individual: ECVRPSolution) -> bool:
        """Check the validity of an individual according to the rules this instance implement."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        instance = individual.get_instance()
        for road in individual.get_roads():
            latest = road[0]
            battery = instance.get_ev_battery()
            time = 0.
            for i in road:
<<<<<<< HEAD
                battery -= instance.get_batterie_consuption(latest, i)
=======
                battery -= instance.get_batterie_consumption(latest, i)
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
                if battery < 0:
                    return False

                time += instance.get_time_used(latest, i)

                if instance.is_charger(i):
                    time += instance.get_batterie_charging_rate() * \
                        (instance.get_ev_battery() - battery)
                    battery = instance.get_ev_battery()

                elif not instance.is_depot(i):
                    time_w = instance.get_tw(i)
                    if time > time_w[1]:
                        return False
                    time = max(time, time_w[0])

                latest = i
        return True


# pylint: disable=too-few-public-methods
class VehiculeCountValidator(ConstraintValidator[ECVRPSolution]):
<<<<<<< HEAD
    def is_valid(self, individual: ECVRPSolution) -> bool:
=======
    """Class in charge of checking if the number of vehicule used is conform."""

    def is_valid(self, individual: ECVRPSolution) -> bool:
        """Check the validity of an individual according to the rules this instance implement."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        return len(individual.get_roads()) <= individual.get_instance().get_ev_count()


# pylint: disable=too-few-public-methods
class TownUnicityValidator(ConstraintValidator[ECVRPSolution]):
<<<<<<< HEAD
    """ Class in charge of checking if each town is only present exactly one time in the solution.
        Depots and chargers are ignored.
        This validator has a terrible complexity and is not intended to be used during the GA.
        It is intended to be used to check if the first generation is valid,
        the following generation should be build valdid according to this class.
    """
    def is_valid(self, individual: ECVRPSolution) -> bool:
=======
    """
    Class in charge of checking if each town is only present exactly one time in the solution.

    Depots and chargers are ignored.
    This validator has a terrible complexity and is not intended to be used during the GA.
    It is intended to be used to check if the first generation is valid,
    the following generation should be build valdid according to this class.
    """

    def is_valid(self, individual: ECVRPSolution) -> bool:
        """Check the validity of an individual according to the rules this instance implement."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        instance = individual.get_instance()
        visited = set()
        for i in individual.get_points():
            if not (instance.is_charger(i) or instance.is_depot(i)) and i in visited:
                return False
            visited.add(i)
        points = set(instance.get_towns())
        return len(points.intersection(visited)) == len(points)


class CapacityValidator(ConstraintValidator[ECVRPSolution]):
<<<<<<< HEAD
    """ Class in charge of checking if the cargo capacity of the EVs is not exceeded
    """
    def is_valid(self, individual: ECVRPSolution) -> bool:
=======
    """Class in charge of checking if the cargo capacity of the EVs is not exceeded."""

    def is_valid(self, individual: ECVRPSolution) -> bool:
        """Check the validity of an individual according to the rules this instance implement."""
>>>>>>> 192b80fca1d7728ab6b3fa31fa34440ffc1da9c1
        instance = individual.get_instance()
        for road in individual.get_roads():
            capacity = instance.get_ev_capacity()
            for i in road:
                if not (instance.is_charger(i) or instance.is_depot(i)):
                    capacity -= instance.get_demand(i)
                    if capacity < 0:
                        return False
        return True
