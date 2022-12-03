# -*- coding: utf-8 -*-

"""
This module holds the embedding part of the deep reinforcement learning algorithm.
@author: Axel Velez
@license: GPL-3
@date: 2022-12-03
@version: 0.2
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

from abc import ABC, abstractmethod
import sys
from os import path
from random import randint
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# from src.cvrp.ecvrp import ECVRPInstance

# pylint: disable=wrong-import-position disable=E0401
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from cvrp.ecvrp import ECVRPInstance # noqa E402
from server.utils.utils import parse_dataset, get_datasets, create_ecvrp # noqa E402
# pylint: enable=wrong-import-position enable=E0401


class Embedding(ABC):
    """
    Embedding interface to help the OOP
    """

    @abstractmethod
    def embed(self, graph: ECVRPInstance) -> list:
        """
        :param g: the graph represented as an ECVRPInstance

        :return: an embedded vector representation of the problem
        """


class EmbeddingClass(Embedding):
    """
    Graph embedding layer.
    """
    def __init__(self) -> None:
        pass

    def _data_processing(self, data):

        scaler = StandardScaler()
        data = scaler.fit_transform(data)
        return data

    def _predict(self, data):

        num_inputs = len(data)
        # Reshape dataframe
        data = data.reshape(-1, num_inputs, 5)
        print('N:', num_inputs)

        # Convolutional layer for x_vector
        x_model = tf.keras.models.Sequential([
            # 128 filters, sliding window of size 1 (1 city at a time)
            tf.keras.layers.Conv1D(128, 1, activation='relu', input_shape=(num_inputs, 5))
        ])

        x_model.compile()

        y_predicted = x_model.predict(data)
        print(y_predicted)
        print(y_predicted.shape)
        return y_predicted

    def embed(self, graph: ECVRPInstance) -> list:

        # Vector X

        # Each Xi has the following data:
        # x : x coordinate
        # z : z coordinate
        # e : start of time window
        # l : end of time window
        # d : remaining demand at step t

        # TODO: Get number of total nodes (not just towns)
        num_nodes = len(graph.get_towns())
        print('TOWNS', num_nodes)

        features = ['x', 'z', 'e', 'l', 'd']

        x_vector = pd.DataFrame(columns=features)
        coordinates = []
        time_windows = []
        demands = []

        # For each node get the necessary informations
        for i in range(num_nodes):
            # Get the coordinates
            # TODO: Replace with the real coordinates
            coordinates.append((randint(0, 200), randint(0, 200)))
            # Get the demand
            demands.append(graph.get_demand(i))
            # Get the time windows
            time_windows.append(graph.get_tw(i))

        coordinates = np.array(coordinates)
        demands = np.array(demands)
        time_windows = np.array(time_windows)

        # Building the dataframe
        x_vector['x'] = coordinates[:, 0]
        x_vector['z'] = coordinates[:, 1]
        x_vector['e'] = time_windows[:, 0]
        # TODO: Fix bug. Having inf values causes problem in the predictions.
        # It returns an array with values either set to 0 or inf.
        # x_vector['l'] = time_windows[:, 1]
        x_vector['l'] = np.zeros(num_nodes)
        x_vector['d'] = demands

        print(x_vector)

        # Passing the data through the conv1D layer
        x_vector = self._predict(x_vector.to_numpy())

        print(x_vector)

        # Passing data through embedding layer
        print(x_vector)
        print(type(x_vector[0][0][0]))
        print(x_vector[0][0][1])

        print('First line', x_vector[0][0])
        print(len(x_vector[0][0]))
        print(x_vector.shape)

        # print('0', x_vector[0])

        # TODO: Do the same for the g_vector
        # Vector G

        # G vector :
        # b : battery
        # t : time
        # ev : number of electric vehicles

        # g_vector = [[[50, 0, 6]]]
        g_vector = [[[graph.get_ev_battery(), 0, graph.get_ev_count()]]]
        print(g_vector)

        g_model = tf.keras.models.Sequential([
            tf.keras.layers.Conv1D(128, 1, activation='relu', input_shape=(1,  3))
        ])

        g_model.compile()
        g_vector = g_model.predict(g_vector)
        print(g_vector.shape)
        print(g_vector)

        # TODO: feed x_vector and g_vector to a custom embedding layer

        # Returning x_vector for now
        return x_vector


emb = EmbeddingClass()

parsed_data = parse_dataset(get_datasets()[0])
evrp = create_ecvrp(parsed_data)
emb.embed(evrp)
