# -*- coding: utf-8 -*-

"""
This module holds the various constraint validators used to configure the ECVRP

@author: Jean Maccou
@license: GPL-3
@date: 2022-12-06
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
import tensorflow as tf
from keras import layers

class Attention(ABC):
    """
    Attention interface to help the OOP
    """

    @abstractmethod
    def attention(self, mu: tf.TensorArray, h : tf.Tensor = None) -> tf.Tensor:
        """
        :param mu: a tensor array on which we want to execute the attention mecanism
        :param h: the memory state of the learning method

        :return: a tensor of the probabilities to compute the learning on each element of the vector
        """
        pass


class AttentionFactory(ABC):
    @abstractmethod
    def generate(self) -> Attention:
        """
        :return: A parametrised Attention method for the ECVRP
        """
        pass


class AttentionClass(Attention, tf.keras.Model):
    def __init__(self):
        """
        Initialize the 4 layers of neurons used by the Attention.
        """
        super(AttentionClass,self).__init__(name = '')
        self._v = _Tan_H_Layer(128)
        self._a = layers.Dense(128, activation = "softmax")
        self._g = _Tan_H_Layer(128)
        self._p = layers.Dense(128, activation = "softmax")
        self.training = True

    def _context_vector(self, mu : tf.TensorArray, h : tf.Tensor = None):
        """
        :param mu: an embedded graph of an instance of E_CVRPTW
        :param h: the memory state of the learning method

        This method computes the context vector we use to determine probability to explore each node.

        :return: the context vector for this iteration.
        """
        value = 0
        for i in range(len(mu)):
            v_i = self._v(tf.concat([mu[i],h]))
            a_i = self._a(v_i)
            value+=a_i*mu[i]
        return value

    def _probability(self, mu : tf.TensorArray, h : tf.Tensor = None):
        """
        :param mu: an embedded graph of an instance of E_CVRPTW
        :param h: the memory state of the learning method

        This method computes the probability to explore each node.

        :return: the probability to explore each node
        """
        cv = self._context_vector(mu, h)
        p = []
        for i in range(len(mu)):
            g_i = self._g(tf.concat([mu[i], cv]))
            p_i = self._p(g_i)
            p.append(p_i)
        return p

    def call(self, mu, h):
        return self._probability(mu, h)


class _Tan_H_Layer(layers.Layer):
    def __init__(self, n_output : int):
        super(_Tan_H_Layer, self).__init__()
        self.n_output = n_output

    def build(self, input_shape):
        self._w1 = self.add_weight("w1", shape=[int(input_shape[-1]), self.n_output])
        self._w2 = self.add_weight("w2", shape=[int(input_shape[-1]), self.n_output])

    def call(self, inputs):
        return self._w1 * tf.nn.tanh(self._w2*inputs)

H = _Tan_H_Layer(64)