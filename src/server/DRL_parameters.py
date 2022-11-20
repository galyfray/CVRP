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


class DRLParameters:
    """ Holds our DRL parameters.
    """
    def __init__(self, nb_epochs: int, learning_rate: float, batch_size: int, momentum: float):
        self.nb_epochs = nb_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.momentum = momentum

    def get_parameters(self):
        return {
            "nbEpochs": self.nb_epochs,
            "learningRate": self.learning_rate,
            "batchSize": self.batch_size,
            "momentum": self.momentum
        }

    def set_parameters(self, params):
        """ Set the parameters for our DRL instance.

        :param params: The parameters needed by our GA solver.
        """
        self.nb_epochs = params["nb_epochs"]
        self.learning_rate = params["learning_rate"]
        self.batch_size = params["batch_size"]
        self.momentum = params["momentum"]
