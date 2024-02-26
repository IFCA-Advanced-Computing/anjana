# -*- coding: utf-8 -*-

# Copyright 2024 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import typing
import numpy as np
import pandas as pd


def suppress_identifiers(
    data: pd.DataFrame, ident: typing.Union[typing.List, np.ndarray]
):
    for i in ident:
        data[i] = ["*"] * len(data)
    return data


def apply_hierarchy(data: list, hierarchies: dict, level: int):
    num_level = len(hierarchies.keys()) - 1
    if level > num_level:
        raise ValueError("Error, invalid hierarchy level")
    pos = []
    for elem in data:
        pos.append(np.where(hierarchies[level - 1].values == elem)[0][0])
    data_anon = hierarchies[level].values[pos]
    return data_anon
