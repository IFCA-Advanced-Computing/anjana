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

import pandas as pd
from anjana.anonymity import utils
from anjana.anonymity import k_anonymity, l_diversity, t_closeness
import pycanon
import time

data = pd.read_csv("data/adult.csv")  # 32561 rows
data.columns = data.columns.str.strip()
cols = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "sex",
    "native-country",
]
for col in cols:
    data[col] = data[col].str.strip()
print(data)  # 32561 rows
quasi_ident = [
    "age",
    "education",
    "marital-status",
    "occupation",
    "sex",
    "native-country",
]
ident = ["race"]
sens_att = "salary-class"
k = 10
l_div = 2
t = 0.5
supp_level = 50

hierarchies = {
    "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
    "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
    "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
    "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
    "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
    "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
}

start = time.time()
data_anon = k_anonymity(data, ident, quasi_ident, k, supp_level, hierarchies)
data_anon = l_diversity(
    data_anon, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
)
data_anon = t_closeness(
    data_anon, ident, quasi_ident, sens_att, k, t, supp_level, hierarchies
)
end = time.time()
print(f"Elapsed time: {end-start}")
print(
    f"Value of k calculated: "
    f"\t{pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}"
)
print(
    f"Value of l-diversity: "
    f"\t{pycanon.anonymity.l_diversity(data_anon, quasi_ident, [sens_att])}"
)
print(
    f"Value of t-closeness: "
    f"\t{pycanon.anonymity.t_closeness(data_anon, quasi_ident, [sens_att])}"
)

transformation_raw = utils.get_transformation(data, quasi_ident, hierarchies)
print(transformation_raw)  # [0, 0, 0, 0, 0, 0]
transformation_anon = utils.get_transformation(data_anon, quasi_ident, hierarchies)
print(transformation_anon)  # [4, 2, 1, 2, 0, 0]
