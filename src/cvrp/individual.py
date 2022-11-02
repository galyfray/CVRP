# -*- coding: utf-8 -*-

""" This module holds the abstract class Individual.
This class represent a generic individual that is deseigned to be used
with our current genetic algorithm implementation

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
from typing import TypeVar, Generic


TypeIndividual = TypeVar("TypeIndividual", bound="Individual")


class Individual(Generic[TypeIndividual], ABC):
    """
    Abstract class handling the concept of individual in our implementation of a Genetic algorithm
    """

    def __init__(self, validators: list["ConstraintValidator"]) -> None:
        super().__init__()
        self._validators = validators

    @abstractmethod
    def get_fitness(self) -> float:
        pass

    def mutate(self) -> None:
        """ Mutate the current individual according to its internal rules.
            This changement is done in place.
        """

    @abstractmethod
    def crossover(self, other: TypeIndividual) -> list[TypeIndividual]:
        """ Generate a list of children according to the rules of the individual.
            The returned list might be empty or contains duplicated children.
            This function might not return the same result with the same argument and
            will probably not be comutative.
        """

    @abstractmethod
    def __copy__(self) -> TypeIndividual:
        pass


# pylint: disable=wrong-import-position
from .constraint_validator import ConstraintValidator  # noqa: E402
