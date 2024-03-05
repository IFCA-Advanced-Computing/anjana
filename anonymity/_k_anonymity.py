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
import pycanon
from pycanon import anonymity
from anonymity.utils import utils
from copy import copy

def k_anonymity(
        data: pd.DataFrame,
        ident: typing.Union[typing.List, np.ndarray],
        quasi_ident: typing.Union[typing.List, np.ndarray],
        k: int,
        supp_level: float,
        hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using k-anonymity.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param k: desired level of k-anonymity.
    :type k: int

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """

    data_anon = k_anonymity_aux(data, ident, quasi_ident, k, supp_level, hierarchies)
    return data_anon


def k_anonymity_aux(
        data: pd.DataFrame,
        ident: typing.Union[typing.List, np.ndarray],
        quasi_ident: typing.Union[typing.List, np.ndarray],
        k: int,
        supp_level: float,
        hierarchies: dict,
) -> (pd.DataFrame, int, dict):
    """Anonymize a dataset using k-anonymity.

    :param data: data under study.
    :type data: pandas dataframe

    :param ident: list with the name of the columns of the dataframe
        that are identifiers.
    :type ident: list of strings

    :param quasi_ident: list with the name of the columns of the dataframe
        that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param k: desired level of k-anonymity.
    :type k: int

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe

    :return: number of records suppressed.
    :rtype: int

    :return: level of generalization applied to each QI.
    :rtype: dict
    """
    data = utils.suppress_identifiers(data, ident)
    n = len(data)

    gen_level = {}
    for qi in quasi_ident:
        gen_level[qi] = 0

    k_real = pycanon.anonymity.k_anonymity(data, quasi_ident)
    quasi_ident_gen = copy(quasi_ident)

    if k_real >= k:
        print(f"The data verifies k-anonymity with k={k_real}")
        supp_records = n - len(data)
        return data, supp_records, gen_level

    while k_real < k:
        if len(quasi_ident_gen) == 0:
            print(f"The anonymization cannot be carried out for the given value k={k}")
            supp_records = n - len(data)
            return data, supp_records, gen_level

        qi_gen = quasi_ident_gen[
            np.argmax([len(np.unique(data[qi])) for qi in quasi_ident_gen])
        ]

        try:
            generalization_qi = utils.apply_hierarchy(
                data[qi_gen].values, hierarchies[qi_gen], gen_level[qi_gen] + 1
            )
            data[qi_gen] = generalization_qi
            gen_level[qi_gen] = gen_level[qi_gen] + 1
        except ValueError:
            if qi_gen in quasi_ident_gen:
                quasi_ident_gen.remove(qi_gen)

        k_real = pycanon.anonymity.k_anonymity(data, quasi_ident)
        if k_real >= k:
            supp_records = n - len(data)
            return data, supp_records, gen_level
        else:
            equiv_class = pycanon.anonymity.utils.aux_anonymity.get_equiv_class(
                data, quasi_ident
            )
            len_ec = [len(ec) for ec in equiv_class]

            if k <= max(len_ec):
                data_ec = pd.DataFrame({"equiv_class": equiv_class, "k": len_ec})
                data_ec_k = data_ec[data_ec.k < k]
                records_sup = sum(data_ec_k.k.values)
                if records_sup * 100 / len(data) <= supp_level:
                    ec_elim = np.concatenate(
                        [
                            pycanon.anonymity.utils.aux_functions.convert(ec)
                            for ec in data_ec_k.equiv_class.values
                        ]
                    )
                    anonim_data = data.drop(ec_elim).reset_index()
                    supp_records = n - len(anonim_data)
                    assert pycanon.anonymity.k_anonymity(anonim_data, quasi_ident) >= k
                    return anonim_data, supp_records, gen_level

    supp_records = n-len(data)

    return data, supp_records, gen_level
