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
from copy import copy


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
def apply_hierarchy_current(
    data: typing.Union[typing.List, np.ndarray],
    hierarchies: dict,
    level: int,
    actual: int,
) -> typing.Union[typing.List, np.ndarray]:
    """Apply certain level of a hierarchy for a quasi-identifier given the current one.

    :param data: data under study.
    :type data: list, numpy array

    :param hierarchies: hierarchies for generalizing a given QI.
    :type hierarchies: dictionary with the hierarchies and the levels

    :param level: level of the hierarchy to be applied.
    :type level: int

    :param actual: current level of the hierarchy applied.
    :type actual: int

    :return: column with the given level of hierarchy applied.
    :rtype: numpy array
    """
    num_level = len(hierarchies.keys()) - 1
    if level > num_level:
        raise ValueError("Error, invalid hierarchy level")
    if not isinstance(hierarchies[level], pd.Series):
        hierarchies[level] = pd.Series(hierarchies[level])
    if not isinstance(hierarchies[actual], pd.Series):
        hierarchies[actual] = pd.Series(hierarchies[actual])

    pos = []
    for elem in data:
        pos.append(np.where(hierarchies[actual].values == elem)[0][0])
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
        if qi in hierarchies.keys():
            for level in hierarchies[qi].keys():
                hierarchy_level = set(hierarchies[qi][level])
                if set(data[qi].values).issubset(hierarchy_level):
                    gen_level[qi] = level

    return gen_level


@beartype()
def get_transformation(
    data_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    hierarchies: dict,
) -> list:
    """Get the transformation applied for anonymizing the data.

    Example: a transformation [0,1,2,0] means:
    - Level 0 of generalization for th 1st QI
    - Level 1 of generalization for th 2nd QI
    - Level 2 of generalization for th 3rd QI
    - Level 0 of generalization for the 4th QI

    :param data_anon: data under study.
    :type data_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: transformation applied
    :rtype: list
    """
    gen_level = check_gen_level(data_anon, quasi_ident, hierarchies)
    transformation = []
    for qi in quasi_ident:
        if qi in gen_level.keys():
            transformation.append(gen_level[qi])
        else:
            transformation.append(0)

    return transformation


@beartype()
def apply_transformation(
    data: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    hierarchies: dict,
    transformation: list,
) -> pd.DataFrame:
    """Apply a given transformation to the data.

    :param data: data under study.
    :type data: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :param transformation: transformation to be applied
    :type transformation: list

    :return: dataset generalized with the transformation given
    :rtype: pandas dataframe
    """
    data_anon = copy(data)
    actual_transform = check_gen_level(data_anon, quasi_ident, hierarchies)
    for i, qi in enumerate(quasi_ident):
        hierarchy_qi = hierarchies[qi]
        level = transformation[i]
        if level < 0:
            raise ValueError("Error, invalid hierarchy level")
        if level > max(hierarchies[qi].keys()):
            raise ValueError("Error, invalid hierarchy level")
        actual = actual_transform[qi]
        if level != actual:
            column = apply_hierarchy_current(
                data_anon[qi].values, hierarchy_qi, level, actual
            )
            data_anon[qi] = column

    return data_anon


@beartype()
def generate_intervals(
    quasi_ident: typing.Union[typing.List, np.ndarray],
    inf: typing.Union[int, float],
    sup: typing.Union[int, float],
    step: int,
) -> list:
    """
    Generate intervals as hierarchies.

    Given a quasi-identifier of numeric type, creates a list containing an
    interval-based generalization (hierarchy) of the values of the quasi-identifier.
    The intervals will have the length entered in step.

    :param quasi_ident: values of the quasi-identifier on which the interval-based
        generalization is to be obtained
    :type quasi_ident: list or numpy array

    :param inf: lower value of the set of intervals
    :type inf: int or float

    :param sup: bigger value of the set of intervals
    :type sup: int or float

    :param step: spacing between values of the intervals
    :type step: int

    :return: list with the intervals associated with the given values
    :rtype: list
    """
    values = np.arange(inf, sup + 1, step)
    interval = []
    for num in quasi_ident:
        lower = np.searchsorted(values, num)
        if lower == 0:
            lower = 1
        interval.append(f"[{values[lower - 1]}, {values[lower]})")

    return interval
