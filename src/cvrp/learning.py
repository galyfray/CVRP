from abc import ABC, abstractmethod

class Learning(ABC):
    @abstractmethod
    def learn(v : list) -> list:
        """
        :param v: a vector we want to compute the learning on
        Define an interface for the learning model we want to use
        :return: the vector of the solution finded by the neural network
        """
        pass