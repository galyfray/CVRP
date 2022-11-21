import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class Embedding():
    """ Graph embedding layer.
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

    def data_processing(self, data):

        sc = StandardScaler()
        data = sc.fit_transform(data)
        return data

    def predict(self, data):
        pass


emb = Embedding()
