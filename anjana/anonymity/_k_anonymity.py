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
import pycanon.anonymity
from anjana.anonymity.utils import utils
from copy import copy
from beartype import beartype
from beartype import typing


@beartype
def k_anonymity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    k: int,
    supp_level: typing.Union[float, int],
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
    data_anon, _, _ = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )
    return data_anon


@beartype()
def alpha_k_anonymity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    alpha: typing.Union[float, int],
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using (alpha,k)-anonymity.

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

    :param k: desired level of k-anonymity.
    :type k: int

    :param alpha: desired level of alpha for (alpha,k)-anonymity.
    :type alpha: float

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    data_kanon, supp_records, gen_level = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    if alpha > 1 or alpha < 0:
        raise ValueError(
            f"Invalid value of alpha for (alpha,k)-anonymity " f"alpha={alpha}"
        )

    alpha_real, _ = pycanon.anonymity.alpha_k_anonymity(
        data_kanon, quasi_ident, [sens_att]
    )
    quasi_ident_gen = copy(quasi_ident)

    while alpha_real > alpha:
        if len(quasi_ident_gen) == 0:
            print(f"(alpha,k)-anonymity cannot be achieved for alpha={alpha}")
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

        alpha_real, _ = pycanon.anonymity.alpha_k_anonymity(
            data_kanon, quasi_ident, [sens_att]
        )

        if alpha_real <= alpha:
            return data_kanon

        equiv_class = pycanon.anonymity.utils.aux_anonymity.get_equiv_class(
            data_kanon, quasi_ident
        )

        k_ec = []
        alpha_ec = []
        for ec in equiv_class:
            data_temp = data_kanon.iloc[
                pycanon.anonymity.utils.aux_functions.convert(ec)
            ]
            values = np.unique(data_temp[sens_att].values)
            alpha_s = [
                len(data_temp[data_temp[sens_att] == s]) / len(data_temp)
                for s in values
            ]
            alpha_ec.append(max(alpha_s))
            k_ec.append(len(ec))

        if alpha > min(alpha_ec):
            if max(alpha_ec) <= alpha:
                return data_kanon

            data_ec = pd.DataFrame(
                {"equiv_class": equiv_class, "alpha": alpha_ec, "k": k_ec}
            )
            data_ec_alpha = data_ec[data_ec.alpha > alpha]
            records_sup = sum(data_ec_alpha.k.values)
            if (records_sup + supp_records) * 100 / len(data) <= supp_level:
                ec_elim = np.concatenate(
                    [
                        pycanon.anonymity.utils.aux_functions.convert(ec)
                        for ec in data_ec_alpha.equiv_class.values
                    ]
                )
                anonim_data = data_kanon.drop(ec_elim).reset_index()
                alpha_supp, _ = pycanon.anonymity.alpha_k_anonymity(
                    anonim_data, quasi_ident, [sens_att]
                )
                if alpha_supp <= alpha:
                    return anonim_data

    return data_kanon


def k_anonymity_inner(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    k: int,
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> (pd.DataFrame, int, dict):
    """Auxiliary function for applying k-anonymity.

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
    if k < 1:
        raise ValueError(f"Invalid value of k for k-anonymity k={k}")

    if supp_level > 100 or supp_level < 0:
        raise ValueError(f"Invalid value of for the suppression level {supp_level}")

    data = copy(data)
    data = utils.suppress_identifiers(data, ident)
    n = len(data)

    gen_level = utils.check_gen_level(data, quasi_ident, hierarchies)

    k_real = pycanon.anonymity.k_anonymity(data, quasi_ident)
    quasi_ident_gen = copy(quasi_ident)

    if k_real >= k:
        print(f"The data verifies k-anonymity with k={k_real}")
        supp_records = n - len(data)
        return data, supp_records, gen_level

    while k_real < k:
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
                    k_supp = pycanon.anonymity.k_anonymity(anonim_data, quasi_ident)
                    if k_supp >= k:
                        return anonim_data, supp_records, gen_level

        if len(quasi_ident_gen) == 0:
            print(f"The anonymization cannot be carried out for the given value k={k}")
            supp_records = n - len(data)
            return pd.DataFrame(), supp_records, gen_level

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

    supp_records = n - len(data)

    return data, supp_records, gen_level
