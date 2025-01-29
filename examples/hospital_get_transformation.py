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
from anjana.anonymity import k_anonymity, l_diversity
from anjana.anonymity import utils

data = pd.read_csv("data/hospital_extended.csv")

ident = ["name"]
quasi_ident = ["age", "gender", "city"]
sens_attr = "disease"
k = 2
supp_level = 0
hierarchies = {
    "age": dict(pd.read_csv("../examples/hierarchies/age.csv", header=None)),
    "gender": {
        0: data["gender"].values,
        1: np.array(["*"] * len(data["gender"].values)),
    },
    "city": {0: data["city"].values, 1: np.array(["*"] * len(data["city"].values))},
}
data_anon = k_anonymity(data, ident, quasi_ident, k, supp_level, hierarchies)
print(data_anon)

#    name       age  gender        city   religion          disease
# 0     *  [20, 30[  Female  Tamil Nadu      Hindu           Cancer
# 1     *  [20, 30[    Male  Tamil Nadu      Hindu           Cancer
# 2     *  [20, 30[    Male  Tamil Nadu      Hindu           Cancer
# 3     *  [20, 30[    Male  Tamil Nadu      Hindu           Cancer
# 4     *  [20, 30[  Female      Kerala      Hindu  Viral infection
# 5     *  [20, 30[  Female  Tamil Nadu     Muslim               TB
# 6     *  [20, 30[    Male   Karnataka      Parsi       No illness
# 7     *  [20, 30[  Female      Kerala  Christian    Heart-related
# 8     *  [20, 30[    Male   Karnataka   Buddhist               TB
# 9     *  [10, 20[    Male      Kerala      Hindu           Cancer
# 10    *  [20, 30[    Male   Karnataka      Hindu    Heart-related
# 11    *  [10, 20[    Male      Kerala  Christian    Heart-related
# 12    *  [10, 20[    Male      Kerala  Christian  Viral infection

l_div = 2
data_anon = l_diversity(
    data, ident, quasi_ident, sens_attr, k, l_div, supp_level, hierarchies
)
print(data_anon)
# 0     *  [20, 30[  Female    *      Hindu           Cancer
# 1     *  [20, 30[    Male    *      Hindu           Cancer
# 2     *  [20, 30[    Male    *      Hindu           Cancer
# 3     *  [20, 30[    Male    *      Hindu           Cancer
# 4     *  [20, 30[  Female    *      Hindu  Viral infection
# 5     *  [20, 30[  Female    *     Muslim               TB
# 6     *  [20, 30[    Male    *      Parsi       No illness
# 7     *  [20, 30[  Female    *  Christian    Heart-related
# 8     *  [20, 30[    Male    *   Buddhist               TB
# 9     *  [10, 20[    Male    *      Hindu           Cancer
# 10    *  [20, 30[    Male    *      Hindu    Heart-related
# 11    *  [10, 20[    Male    *  Christian    Heart-related
# 12    *  [10, 20[    Male    *  Christian  Viral infection

transformation_raw = utils.get_transformation(data, quasi_ident, hierarchies)
print(transformation_raw)  # [0, 0, 0]
transformation_anon = utils.get_transformation(data_anon, quasi_ident, hierarchies)
print(transformation_anon)  # [2, 0, 1]

# Testing the function apply_transformation
data_transform1 = utils.apply_transformation(data, quasi_ident, hierarchies, [1, 1, 1])
print(data_transform1)
print(utils.get_transformation(data_transform1, quasi_ident, hierarchies))  # [1, 1, 1]

data_transform2 = utils.apply_transformation(data, quasi_ident, hierarchies, [5, 1, 1])
print(data_transform2)
print(utils.get_transformation(data_transform2, quasi_ident, hierarchies))  # [5, 1, 1]

data_transform3 = utils.apply_transformation(
    data_anon, quasi_ident, hierarchies, [5, 1, 1]
)
print(data_transform3)
print(utils.get_transformation(data_transform3, quasi_ident, hierarchies))  # [5, 1, 1]
