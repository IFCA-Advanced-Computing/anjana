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
def l_diversity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    l_div: int,
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using l-diversity.

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

    :param l_div: desired level of l-diversity.
    :type l_div: int

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    data_anon, _ = _l_diversity_inner(
        data, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
    )
    return data_anon


@beartype()
def entropy_l_diversity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    l_div: int,
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using entropy l-diversity.

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

    :param l_div: desired level of entropy l-diversity.
    :type l_div: int

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    data_kanon = l_diversity(
        data, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
    )

    l_real = pycanon.anonymity.entropy_l_diversity(data_kanon, quasi_ident, [sens_att])
    quasi_ident_gen = copy(quasi_ident)
    gen_level = utils.check_gen_level(data_kanon, quasi_ident, hierarchies)

    if l_real >= l_div:
        print(f"The data verifies entropy l-diversity with l={l_real}")
        return data_kanon

    while l_real < l_div:
        if len(quasi_ident_gen) == 0:
            print(f"Entropy l-diversity cannot be achieved for l={l_div}")
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

        l_real = pycanon.anonymity.entropy_l_diversity(
            data_kanon, quasi_ident, [sens_att]
        )
        if l_real >= l_div:
            return data_kanon

    return data_kanon


@beartype()
def recursive_c_l_diversity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    c: int,
    l_div: int,
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> pd.DataFrame:
    """Anonymize a dataset using recursive (c,l)-diversity.

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

    :param c: desired value of c for recursive (c,l)-diversity.
    :type c: int

    :param l_div: desired level of l-diversity.
    :type l_div: int

    :param supp_level: maximum level of record suppression allowed
        (from 0 to 100).
    :type supp_level: float

    :param hierarchies: hierarchies for generalizing the QI.
    :type hierarchies: dictionary containing one dictionary for QI
        with the hierarchies and the levels

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    if c < 1:
        raise ValueError(f"Invalid value of c for recursive (c,l)-diversity, c={c}")

    data = copy(data)
    data_kanon, supp_records = _l_diversity_inner(
        data, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
    )

    c_real, l_real = pycanon.anonymity.recursive_c_l_diversity(
        data_kanon, quasi_ident, [sens_att]
    )
    quasi_ident_gen = copy(quasi_ident)
    gen_level = utils.check_gen_level(data_kanon, quasi_ident, hierarchies)

    if l_real >= l_div and c_real >= c:
        print(
            f"The data verifies recursive (c,l)-diversity with l={l_real}, c={c_real}"
        )
        return data_kanon

    while l_real < l_div or c_real < c:
        if len(quasi_ident_gen) == 0:
            print(
                f"Recursive (c,l)-diversity cannot be achieved for l={l_div} and c={c}"
            )
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

        c_real, l_real = pycanon.anonymity.recursive_c_l_diversity(
            data_kanon, quasi_ident, [sens_att]
        )

        equiv_class = pycanon.anonymity.utils.aux_anonymity.get_equiv_class(
            data_kanon, quasi_ident
        )
        k_ec = []
        c_ec = []
        for ec in equiv_class:
            data_temp = data_kanon.iloc[
                pycanon.anonymity.utils.aux_functions.convert(ec)
            ]
            values = np.unique(data_temp[sens_att].values)
            r_ec = np.sort([len(data_temp[data_temp[sens_att] == s]) for s in values])
            c_ec.append(np.floor(r_ec[0] / sum(r_ec[(l_div - 1) :]) + 1))
            k_ec.append(len(ec))
            if max(c_ec) < c:
                f"Recursive (c,l)-diversity cannot be achieved for l={l_div} and c={c}"
            else:
                data_ec = pd.DataFrame(
                    {"equiv_class": equiv_class, "c_ec": c_ec, "k": k_ec}
                )
                data_ec_c = data_ec[data_ec.c_ec < c]
                records_sup = sum(data_ec_c.k.values)
                if (records_sup + supp_records) * 100 / len(data) <= supp_level:
                    ec_elim = np.concatenate(
                        [
                            pycanon.anonymity.utils.aux_functions.convert(ec)
                            for ec in data_ec_c.equiv_class.values
                        ]
                    )
                    anonim_data = data_kanon.drop(ec_elim).reset_index()
                    c_supp, l_supp = pycanon.anonymity.recursive_c_l_diversity(
                        anonim_data, quasi_ident, [sens_att]
                    )
                    if l_supp >= l_div and c_supp > c:
                        return anonim_data

        if l_real >= l_div and c_real >= c:
            return data_kanon

    return data_kanon


def _l_diversity_inner(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
    k: int,
    l_div: int,
    supp_level: typing.Union[float, int],
    hierarchies: dict,
) -> (pd.DataFrame, int):
    """Anonymize a dataset using l-diversity.

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

    :param l_div: desired level of l-diversity.
    :type l_div: int

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
    """
    if l_div < 1:
        raise ValueError(f"Invalid value of l for l-diversity l={l_div}")

    data_kanon, supp_records_k, gen_level = k_anonymity_inner(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    data = copy(data)
    data = utils.suppress_identifiers(data, ident)

    l_real = pycanon.anonymity.l_diversity(data_kanon, quasi_ident, [sens_att])
    quasi_ident_gen = copy(quasi_ident)

    if l_real >= l_div:
        print(f"The data verifies l-diversity with l={l_real}")
        return data_kanon, supp_records_k

    while l_real < l_div:
        equiv_class = pycanon.anonymity.utils.aux_anonymity.get_equiv_class(
            data_kanon, quasi_ident
        )
        ec_sensitivity = [
            len(np.unique(data_kanon.iloc[ec][sens_att])) for ec in equiv_class
        ]
        k_ec = [len(ec) for ec in equiv_class]

        if l_div > max(ec_sensitivity):
            data_ec = pd.DataFrame(
                {"equiv_class": equiv_class, "l": ec_sensitivity, "k": k_ec}
            )
            data_ec_l = data_ec[data_ec.l < l_div]
            records_sup = sum(data_ec_l.k.values)
            if (records_sup + supp_records_k) * 100 / len(data) <= supp_level:
                ec_elim = np.concatenate(
                    [
                        pycanon.anonymity.utils.aux_functions.convert(ec)
                        for ec in data_ec_l.equiv_class.values
                    ]
                )
                anonim_data = data_kanon.drop(ec_elim).reset_index()
                l_supp = pycanon.anonymity.l_diversity(
                    anonim_data, quasi_ident, [sens_att]
                )
                supp_records_l = supp_records_k + records_sup
                if l_supp >= l_div:
                    return anonim_data, supp_records_l

        if len(quasi_ident_gen) == 0:
            print(f"l-diversity cannot be achieved for l={l_div}")
            return pd.DataFrame(), supp_records_k

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

        l_real = pycanon.anonymity.l_diversity(data_kanon, quasi_ident, [sens_att])
        if l_real >= l_div:
            return data_kanon, supp_records_k

    return data_kanon, supp_records_k
