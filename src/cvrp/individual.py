# -*- coding: utf-8 -*-

""" This module holds the abstract class Individual and the ConstraintValidator interface
The Individual class represent a generic individual that is deseigned to be used
with our current genetic algorithm implementation. Constraint Validators offer a generic,
and modulable way to check if an individual holds a valid solution.

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


# According to the class diagram aprooved by the team this is normal.
# pylint: disable=too-few-public-methods
class ConstraintValidator(ABC, Generic[TypeIndividual]):
    """ Interface providing a standard methods to check if an Individual holds a valid solution
    """

    @abstractmethod
    def is_valid(self, individual: TypeIndividual) -> bool:
        """
            Check the validity of an individual according to the rules this instance implement
        """


class Individual(Generic[TypeIndividual], ABC):
    """
    Abstract class handling the concept of individual in our implementation of a Genetic algorithm
    """

    def __init__(self, validators: list["ConstraintValidator"]) -> None:
        super().__init__()
        self._validators = validators

    @abstractmethod
    def get_fitness(self) -> float:
        """ Return the fitness of the individual.
        """

    @abstractmethod
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
        """ Produce a copy of the individual.
        """
