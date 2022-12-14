# -*- coding: utf-8 -*-

"""
This module holds parts of the implementation of \
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

from typing import Generic
import random
import time
from .individual import TypeIndividual


class GA(Generic[TypeIndividual]):
    """
    Class in charge of the main logic.

    This class will breed and select various individual accros many generations.
    """

    def __init__(
                self,
                initial: list[TypeIndividual],
                mutation_rate: float,
                seed: int = None
            ):
        """
        Initialize the GA class.

        :param initial: The initial state of the GA: the first generation of individuals.
        :param mutation_rate: The percents of chance that a child is mutated.
        :param seed: The seed used to seed the random generator used by this class.
        """
        self._current_pop = initial

        if not 0 < mutation_rate < 1:
            raise ValueError("The mutation_rate rate must be between 0 and 1")
        self._mutation_rate = mutation_rate

        if seed is None:
            seed = time.thread_time_ns()

        random.seed(seed)

        self._len = 0

    def run(self, generations: int):
        """
        Run the Ga algorithm.

        this method will breed n generation and return each generation.
        """
        self._len = generations

        self._current_pop.sort()

        parents_count = len(self._current_pop) // 2
        children_count = len(self._current_pop) - parents_count

        for _ in range(generations):
            fitnesses = [i.get_fitness() for i in self._current_pop]
            sum_fit = sum(fitnesses)

            cum = [0]*len(fitnesses)
            parents = [None] * parents_count

            for j in range(parents_count):
                for i, fit in enumerate(fitnesses):
                    cum[i] = fit/sum_fit + (cum[i - 1] if i > 0 else 0)

                index = 0
                randi = random.random()
                while cum[index] < randi:
                    index += 1
                parents[j] = self._current_pop[index]

                fitnesses.pop(index)

            children = self._mutate(self._crossbreed(parents, children_count))
            self._current_pop = [*parents, *children]
            self._current_pop.sort()
            yield self._current_pop

    def _crossbreed(self, parents: list[TypeIndividual], count: int) -> list[TypeIndividual]:
        children = []
        while len(children) < count:

            first = random.randint(0, len(parents)-1)
            second = first
            while first == second:
                second = random.randint(0, len(parents)-1)

            children.extend(parents[first].crossover(parents[second]))

        return children

    def _mutate(self, children: list[TypeIndividual]) -> list[TypeIndividual]:
        for child in children:
            if random.random() < self._mutation_rate:
                child.mutate()
        return children

    def __len__(self):
        """Rturns he number of iteration given to the run method."""
        return self._len
