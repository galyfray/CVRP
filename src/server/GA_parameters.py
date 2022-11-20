# -*- coding: utf-8 -*-

"""
This module holds the parameters of our genetic algorithm.

@author: Sonia Kwassi and Axel Velez
@license: GPL-3
@date: 2022-11-20
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


class GAParameters:
    """ Holds our GA parameters.
    """
    def __init__(self, nb_epochs: int, pop_size: int, crossover_rate: float, mutation_rate: float):
        self.nb_epochs = nb_epochs
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def get_parameters(self):
        return {
            "nbEpochs": self.nb_epochs,
            "popSize": self.pop_size,
            "crossoverRate": self.crossover_rate,
            "mutationRate": self.mutation_rate
        }

    def set_parameters(self, params):
        """ Set the parameters for our GA instance.

        :param params: The parameters needed by our GA solver.
        """
        self.nb_epochs = params["nb_epochs"]
        self.pop_size = params["pop_size"]
        self.crossover_rate = params["crossover_rate"]
        self.mutation_rate = params["mutation_rate"]
