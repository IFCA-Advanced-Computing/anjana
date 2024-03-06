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
from anonymity import k_anonymity_aux


def l_diversity(
    data: pd.DataFrame,
    ident: typing.Union[typing.List, np.ndarray],
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: typing.Union[typing.List, np.ndarray],
    k: int,
    l: int,
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

    :return: anonymized data.
    :rtype: pandas dataframe
    """
    data_kanon, supp_records, gen_level = k_anonymity_aux(
        data, ident, quasi_ident, k, supp_level, hierarchies
    )

    l_real = pycanon.anonymity.l_diversity(data_kanon, quasi_ident, sens_att)
    quasi_ident_gen = copy(quasi_ident)
    sa = sens_att[0]

    if l_real >= l:
        print(f"The data verifies k-anonymity with l={l_real}")
        return data_kanon

    while l_real < l:
        if len(quasi_ident_gen) == 0:
            print(f"The anonymization cannot be carried out for the given value l={l}")
            return data_kanon

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

        l_real = pycanon.anonymity.l_diversity(data_kanon, quasi_ident, sens_att)
        if l_real >= l:
            return data_kanon

        equiv_class = pycanon.anonymity.utils.aux_anonymity.get_equiv_class(
            data_kanon, quasi_ident
        )
        ec_sensitivity = [len(np.unique(data_kanon.iloc[ec][sa])) for ec in equiv_class]

        if l > max(ec_sensitivity):
            data_ec = pd.DataFrame({"equiv_class": equiv_class, "l": ec_sensitivity})
            data_ec_l = data_ec[data_ec.l < l]
            records_sup = sum(data_ec_l.l.values)
            if (records_sup + supp_records) * 100 / len(data) <= supp_level:
                ec_elim = np.concatenate(
                    [
                        pycanon.anonymity.utils.aux_functions.convert(ec)
                        for ec in data_ec_l.equiv_class.values
                    ]
                )
                anonim_data = data_kanon.drop(ec_elim).reset_index()
                l_supp = pycanon.anonymity.l_diversity(anonim_data, quasi_ident, sens_att)
                if l_supp >= l:
                    return anonim_data
    return data
