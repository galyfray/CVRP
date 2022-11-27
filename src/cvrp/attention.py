from abc import ABC, abstractmethod
import tensorflow as tf
from tensorflow import keras
from keras import layers

class Attention(ABC):
    """
    Attention interface to help the OOP
    """

    @abstractmethod
    def attention(self, v: list) -> list: #Les vecteurs sont représentés comme des listes mais ça peut être changé
        """
        :param v: a vector on which we want to execute the attention mecanism
        
        :return: a vector of the probabilities to compute the learning on each element of the vector
        """
        pass


class AttentionFactory(ABC):
    @abstractmethod
    def generate(self) -> Attention:
        """
        :return: A parametrised Attention method for the ECVRP
        """
        pass


class AttentionClass(Attention):
    def __init__(self):
        """
        """
        pass

    def _context_vector(self):
        pass

    def _a(self, v : list) -> list:
        pass