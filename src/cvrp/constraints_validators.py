# -*- coding: utf-8 -*-

"""
This module holds the various constraint validators used to configure the ECVRP

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
class CapacityValidator(ConstraintValidator[ECVRPSolution]):
    """ Class in charge of checking the battery capacity is never exeded
    """
    def is_valid(self, individual: ECVRPSolution) -> bool:
        instance = individual.get_instance()
        for road in individual.get_roads():
            latest = road[0]
            battery = instance.get_ev_battery()
            for i in road:
                battery -= instance.get_batterie_consuption(latest, i)
                if battery < 0:
                    return False
                if instance.is_charger(i):
                    battery = instance.get_ev_battery()
                latest = i
        return True


# pylint: disable=too-few-public-methods
class VehiculeCountValidator(ConstraintValidator[ECVRPSolution]):
    def is_valid(self, individual: ECVRPSolution) -> bool:
        return len(individual.get_roads()) <= individual.get_instance().get_ev_count()
