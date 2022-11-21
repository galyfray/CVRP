from abc import ABC, abstractmethod

class Attention(ABC):
    """
    Attention interface to help the OOP
    """

    @abstractmethod
    def attention(v: list) -> list: #Les vecteurs sont représentés comme des listes mais ça peut être changé
        """
        :param v: a vector on which we want to execute the attention mecanism
        
        :return: a vector of the probabilities to compute the learning on each element of the vector
        """
        pass