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
from copy import deepcopy
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
# tf.config.run_functions_eagerly(True)
print(tf.__version__)

# from src.cvrp.ecvrp import ECVRPInstance

# pylint: disable=wrong-import-position disable=E0401
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from cvrp.ecvrp import ECVRPInstance # noqa E402
from server.utils.utils import parse_dataset, get_datasets, create_ecvrp # noqa E402
# pylint: enable=wrong-import-position enable=E0401

class MyEmbeddingModel(tf.keras.Model):
    def __init__(self, num_outputs, graph):
        super(MyEmbeddingModel, self).__init__()
        self.num_outputs = num_outputs
        self.p = 5  # The lower, the bigger the number of unique values. if too high, just infs, unqiue values = 1
        self.graph = graph
        self.w1 = self.add_weight('w1', shape=(1, ))
        self.w2 = self.add_weight('w2', shape=(1, ))
        self.w3 = self.add_weight('w3', shape=(1, ))
        self.w4 = self.add_weight('w4', shape=(1, ))
        self.w5 = self.add_weight('w5', shape=(1, ))

    def call(self, inputs):
        x = inputs[0][0:-1]
        g = inputs[0][-1]

        #DEBUG
        #self.p = 1

        u_vect = x.numpy()

        new_u_vect = deepcopy(u_vect)
        # k iterations until p is reached
        for _ in range(self.p):
            print('ITERATION', _)
            u_vect = deepcopy(new_u_vect)  # Update vect once all nodes are calculated for step k
            # new_u_vect.clear()  # Emptying the vect
            for i in range(self.graph.get_node_number()):
                #print('Node', i)
                # u_sum = 0 # not valid = this is not an int, but an array of floats
                u_sum = np.zeros(128)
                # print('U= ', u_vect)
               # print(u_vect.shape)

                #print('N', self.graph.get_neighbors(i))
                travel_times = 0
                
                for j in self.graph.get_neighbors(i):
                    travel_times += self.w5 * self.graph.get_distance(i, j)  # TODO: travelling time
                    # TODO: append travel times
                    u_sum += u_vect[j]  # TODO: Fix this: NoneValues?
                    # + self.w4 * tf.nn.relu(travel_times)
                    #print('SUM', u_sum)
                new_u_vect[i] = self.w1 * x[i] + self.w2 * g + self.w3 * u_sum + self.w4 * tf.nn.relu(travel_times)
                #wprint(f'NEW FOR {i} :', new_u_vect[i])

        u_vect = deepcopy(new_u_vect)

        print('ORGINAL', x)
        """
        for y, value in enumerate(u_vect):
            if y > 0:
                if (u_vect[i-1] == value).all():
                    print('SAME')
                else:
                    print('DIFF')
        """
        print(f'UNIQUE values ({len(np.unique(u_vect, axis=0))}) : {np.unique(u_vect, axis=0)}')

        return tf.nn.relu(u_vect)

"""
class MyEmbeddingLayer(tf.keras.layers.Layer):
    def __init__(self, num_outputs, graph, g):
        super(MyEmbeddingLayer, self).__init__()
        self.num_outputs = num_outputs
        self.p = 10
        self.g = g
        self.graph = graph
        self.w1 = self.add_weight('w1', shape=(1, ))
        self.w2 = self.add_weight('w2', shape=(1, ))
        self.w3 = self.add_weight('w3', shape=(1, ))
        self.w4 = self.add_weight('w4', shape=(1, ))
        self.w5 = self.add_weight('w5', shape=(1, ))
        #self. u = tf.Variable()

    def build(self, input_shape):
        # self.kernel = self.add_weight("kernel", shape=[int(input_shape[-1]), self.num_outputs])
        pass

    # We have to define the N(i) and w(i, j) functions
    def call(self, inputs):
        x = inputs[0][0:-1]
        g = inputs[0][-1]
        print('TYPE', type(x))
        print('TEST')
        # tf.numpy_function()
        #proto = tf.make_tensor_proto(x)
        #u = tf.make_ndarray(proto)
        # tf.make_ndarray(proto)

        # Initializing Ui at step 0
        # u = copy(x)
        #print(u)
        
        # u = []
        # u_vect = []
        #u = x

        # tf.Variable(initial_value=tf.get, name='u_vect', shape=x.shape)
       
       

       # tf.print(self.u)

        new_u_vect = []
        for _ in range(self.p):
            u_vect = deepcopy(new_u_vect)  # Update vect once all nodes are calculated for step k
            new_u_vect.clear()  # Emptying the vect
            for i in range(self.graph.get_node_number()):
                u_sum = 0
                for j in self.graph.get_neighbors(i):
                    travel_times = self.w5 * self.graph.get_distance(i, j)  # TODO: travelling time
                    u_sum += u_vect[j]  # TODO: Fix this: NoneValues?
                u = self.w1 * x + self.w2 * g + self.w3 * u_sum + self.w4 * tf.nn.relu(travel_times)

                new_u_vect.append(u)

        u_vect = deepcopy(new_u_vect)

        
        return tf.nn.relu(x)  # Return relu of everything
"""

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


class EmbeddingFactory(ABC):
    @abstractmethod
    def generate(self) -> Embedding:
        """
        :return: A parametrised Embedding method for the ECVRP
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
        # num_nodes = len(graph.get_towns())
        num_nodes = 89
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

        # Using the functionnal API for embedding
        # input_x = tf.keras.Input(shape=(75, 128))
        # input_g = tf.keras.Input(shape=(1, 128))
        merged = tf.keras.layers.Concatenate(axis=1)([x_vector, g_vector])
        # print(merged)

        #TODO: Fix this dynamically
        num_inputs = 89
        """
        embedding_model = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=(num_inputs + 1, 128)),
            MyEmbeddingLayer(1, graph=graph)
        ])

        embedding_model.compile()
        #z = embedding_model.predict(merged)
        z = embedding_model.predict(merged)

        print('Output : ', z)
        print('shape', z.shape)

        """

        #custom_model = MyEmbeddingModel(1, graph)
        custom_model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=89, output_dim=89, input_length=128)
        ])
        custom_model.compile()
        #z = custom_model(merged)
        z = custom_model(merged[0])
        print('len', len(z))
        #print(z)
        #print(z[0])
        #print('Weights=', custom_model.get_weights())
        print(f'UNIQUE values ({len(np.unique(z, axis=0))}) : {np.unique(z, axis=0)}')

        #Embedding will sometime return only 0

        # Returning x_vector for now
        return x_vector


emb = EmbeddingClass()

parsed_data = parse_dataset(get_datasets()[0])
print(get_datasets()[0])
evrp = create_ecvrp(parsed_data)
emb.embed(evrp)

"""
a = [0, 1, 2, 3]
b = []
b = deepcopy(a)
print(b)
"""


# Custom Loss Function (12)
def loss():
    pass
