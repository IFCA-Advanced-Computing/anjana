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

import numpy as np
import pandas as pd
import pycanon
from anjana.anonymity.utils import utils
from copy import copy
from anjana.anonymity import k_anonymity_inner
from beartype import beartype
from beartype import typing


@beartype()
def basic_beta_likeness(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    beta: typing.Union[float, int],
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using basic beta-likeness and k-anonymity.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: string with the name of the sensitive attribute.
    :type sens_att: string

    :param k: value of k for k-anonymity to be applied.
    :type k: int

    :param beta: value of beta for basic beta-likeness to be applied.
    :type beta: float

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    if beta < 0:
        raise ValueError(f"Invalid value of beta for beta-likeness, beta={beta}")

    data_kanon, supp_records, gen_level = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    beta_real = pycanon.anonymity.basic_beta_likeness(
        data_kanon, quasi_ident, [sens_att]
    )
    quasi_ident_gen = copy(quasi_ident)

    if beta_real <= beta:
        print(f"The data verifies basic beta-likeness with beta={beta_real}")
        return data_kanon

    while beta_real > beta:
        if len(quasi_ident_gen) == 0:
            print(f"Basic beta likeness cannot be achieved for beta={beta}")
            return pd.DataFrame()

        qi_gen = quasi_ident_gen[
            np.argmax([len(np.unique(data_kanon[qi])) for qi in quasi_ident_gen])
        ]

        try:
            generalization_qi = utils.apply_hierarchy(
                data_kanon[qi_gen].values, hierarchies[qi_gen], gen_level[qi_gen] + 1
            )
            data_kanon[qi_gen] = generalization_qi
            gen_level[qi_gen] = gen_level[qi_gen] + 1
        except ValueError:
            if qi_gen in quasi_ident_gen:
                quasi_ident_gen.remove(qi_gen)

        beta_real = pycanon.anonymity.basic_beta_likeness(
            data_kanon, quasi_ident, [sens_att]
        )
        if beta_real <= beta:
            return data_kanon

    return data_kanon


@beartype()
def enhanced_beta_likeness(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    beta: typing.Union[float, int],
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using enhanced beta-likeness and k-anonymity.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: string with the name of the sensitive attribute.
    :type sens_att: string

    :param k: value of k for k-anonymity to be applied.
    :type k: int

    :param beta: value of beta for enhanced beta-likeness to be applied.
    :type beta: float

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    if beta < 0:
        raise ValueError(f"Invalid value of beta for beta-likeness, beta={beta}")

    data_kanon, supp_records, gen_level = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    beta_real = pycanon.anonymity.enhanced_beta_likeness(
        data_kanon, quasi_ident, [sens_att]
    )
    quasi_ident_gen = copy(quasi_ident)

    if beta_real <= beta:
        print(f"The data verifies enhanced beta-likeness with beta={beta_real}")
        return data_kanon

    while beta_real > beta:
        if len(quasi_ident_gen) == 0:
            print(f"Enhanced beta likeness cannot be achieved for beta={beta}")
            return pd.DataFrame()

        qi_gen = quasi_ident_gen[
            np.argmax([len(np.unique(data_kanon[qi])) for qi in quasi_ident_gen])
        ]

        try:
            generalization_qi = utils.apply_hierarchy(
                data_kanon[qi_gen].values, hierarchies[qi_gen], gen_level[qi_gen] + 1
            )
            data_kanon[qi_gen] = generalization_qi
            gen_level[qi_gen] = gen_level[qi_gen] + 1
        except ValueError:
            if qi_gen in quasi_ident_gen:
                quasi_ident_gen.remove(qi_gen)

        beta_real = pycanon.anonymity.enhanced_beta_likeness(
            data_kanon, quasi_ident, [sens_att]
        )
        if beta_real <= beta:
            return data_kanon

    return data_kanon
