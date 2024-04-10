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

"""Module with utils for the anonymization tools."""

import numpy as np
import pandas as pd
from beartype import beartype
from beartype import typing


@beartype()
def suppress_identifiers(
    data: pd.DataFrame, ident: typing.Union[typing.List, np.ndarray]
) -> pd.DataFrame:
    """Remove the identifiers from a dataset.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :return: data with the identifiers suppressed.
    :rtype: pandas dataframe
    """
    for i in ident:
        if i not in data.columns:
            raise ValueError(f"Identifier {i} is not a column in the given dataset")
        data[i] = ["*"] * len(data)

    return data


@beartype()
def apply_hierarchy(
    data: typing.Union[typing.List, np.ndarray], hierarchies: dict, level: int
) -> typing.Union[typing.List, np.ndarray]:
    """Apply the given level of a hierarchy for a quasi-identifier.

    :param data: data under study.
    :type data: list, numpy array

    :param hierarchies: hierarchies for generalizing a given QI.
    :type hierarchies: dictionary with the hierarchies and the levels

    :param level: level of the hierarchy to be applied.
    :type level: int

    :return: column with the given level of hierarchy applied.
    :rtype: numpy array
    """
    num_level = len(hierarchies.keys()) - 1
    if level > num_level:
        raise ValueError("Error, invalid hierarchy level")
    if not isinstance(hierarchies[level], pd.Series):
        hierarchies[level] = pd.Series(hierarchies[level])
    if not isinstance(hierarchies[level - 1], pd.Series):
        hierarchies[level - 1] = pd.Series(hierarchies[level - 1])

    pos = []
    for elem in data:
        pos.append(np.where(hierarchies[level - 1].values == elem)[0][0])
    data_anon = hierarchies[level].values[pos]
    return data_anon


@beartype()
def check_gen_level(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    hierarchies: dict,
) -> dict:
    """Check the generalization level for each quasi-identifier.

    :param data: data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: level of generalization applied to each QI.
    :rtype: dict
    """
    gen_level = {}
    for qi in quasi_ident:
        for level in hierarchies[qi].keys():
            hierarchy_level = set(hierarchies[qi][level])
            if set(data[qi].values).issubset(hierarchy_level):
                gen_level[qi] = level

    return gen_level
