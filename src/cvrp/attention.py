from abc import ABC, abstractmethod
from typing import Generator

class Attention(ABC):
    """
    Attention interface to help the OOP
    """

    @abstractmethod
    def attention(v: list) -> Generator: #Les vecteurs sont représentés comme des listes mais ça peut être changé
        """
        :param v: a vector on which we want to execute the attention mecanism

        :return: a Generator TODO define the type and what do the generator
        """
        pass