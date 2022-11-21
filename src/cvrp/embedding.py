import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from abc import ABC, abstractmethod
from ecvrp import ECVRPInstance

class Embedding(ABC):
    """
    Embedding interface to help the OOP
    """

    @abstractmethod
    def embed(self, g : ECVRPInstance) -> list: #Jsp comment on représente les vecteur j'ai mis liste pour le moment, je vous laisse modifier si c'est pas bon
        """
        :param g: the graph represented as an ECVRPInstance

        :return: an embedded vector representation of the problem
        """
        pass

class EmbeddingClass(Embedding):
    """
    Graph embedding layer.
    """
    def __init__(self) -> None:

        features = ['x', 'z', 'e',	'l',	'd']
        data_x = pd.DataFrame(
            np.array([
                [1, 2, 3, 4, 5],
                [4, 5, 6, 7, 8],
                [7, 8, 9, 10, 11],
                [41, 51, 61, 71, 81],
                [14, 15, 16, 17, 18],
                [14, 15, 16, 17, 18]]), columns=features)
        print(data_x)

    def _data_processing(self, data):

        sc = StandardScaler()
        data = sc.fit_transform(data)
        return data

    def _predict(self, data):
        pass

    def embed(self, g):
        pass


emb = Embedding()
