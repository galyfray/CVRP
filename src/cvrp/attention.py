from abc import ABC, abstractmethod
import tensorflow as tf
from keras import layers

class Attention(ABC):
    """
    Attention interface to help the OOP
    """

    @abstractmethod
    def attention(self, v: tf.Tensor) -> tf.Tensor:
        """
        :param v: a tensor on which we want to execute the attention mecanism
        
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
    def __init__(self, n:int):
        """:param n: the number of nodes that are not the depot
        Initialize the 4 layers of neurons used by the Attention.
        """
        super(AttentionClass,self).__init__(name = '')
        self._v = layers.Dense(64, activation = "tanh")
        self._a = layers.Dense(64, activation = "softmax")
        self._g = layers.Dense(64, activation = "tanh")
        self._p = layers.Dense(64, activation = "softmax")
        self._n = n
        self.training = True

    def _context_vector(self, mu : tf.TensorArray, h : tf.Tensor):
        value = 0
        for i in range(self._n + 1):
            v_i = self._v(tf.concat[mu[i],h])
            a_i = self._a(v_i)
            value+=a_i*mu[i]
        return value