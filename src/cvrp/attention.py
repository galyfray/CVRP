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

    def attention(self, mu: tf.TensorArray, h : tf.Tensor = None) -> tf.Tensor:
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