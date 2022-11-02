# -*- coding: utf-8 -*-

"""
This module holds the ConstraintValidator interface as well as several default implementation of it.

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

from abc import ABC, abstractmethod
from typing import Generic

# The cyclic import is handled in the individual module.
# pylint: disable=cyclic-import
from .individual import TypeIndividual


# According to the class diagram aprooved by the team this is normal.
# pylint: disable=too-few-public-methods
class ConstraintValidator(ABC, Generic[TypeIndividual]):
    """ Interface providing a standard methods to check if an Individual holds a valid solution
    """

    @abstractmethod
    def is_valid(self) -> bool:
        pass
