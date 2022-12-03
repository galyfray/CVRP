# -*- coding: utf-8 -*-

"""
This module holds the test of the graph embedding part of the deep reinforcement learning algorithm.
@author: Axel Velez
@license: GPL-3
@date: 2022-12-03
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

import pandas as pd
import numpy as np
import pytest
from src.cvrp.embedding import EmbeddingClass


features = ['x', 'z', 'e', 'l', 'd']
data_x = pd.DataFrame(
    np.array([
        [1, 2, 3, 4, 5],
        [4, 5, 6, 7, 8],
        [7, 8, 9, 10, 11],
        [41, 51, 61, 71, 81],
        [14, 15, 16, 17, 18],
        [14, 15, 16, 17, 18]]), columns=features)

expected_processed_data = np.array([
        [-0.94694252, -0.85518611, -0.79072371, -0.7433581, -0.70723594],
        [-0.71967632, -0.67193194, -0.63768041, -0.61217726, -0.59254903],
        [-0.49241011, -0.48867778, -0.48463711, -0.48099642, -0.47786212],
        [2.08327355,  2.13796528,  2.16811339,  2.18634735,  2.19816577],
        [0.0378777, -0.06108472, -0.12753608, -0.17490779, -0.21025933],
        [0.0378777, -0.06108472, -0.12753608, -0.17490779, -0.21025933]])


def test_data_processing():
    """Tests the data pre-processing."""
    emb = EmbeddingClass()
    data = emb._data_processing(data_x)
    assert pytest.approx(data, 0.0001) == expected_processed_data


def test_conv():
    pass
