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
from anonymity import k_anonymity
import pycanon
from pycanon import anonymity

data = pd.read_csv("adult.csv")
data.columns = data.columns.str.strip()
cols = ['workclass', 'education', 'marital-status',
               'occupation', 'sex', 'native-country']
for col in cols:
    data[col] = data[col].str.strip()
data = data[:20]
print(data)
print(data)
quasi_ident = ['age', 'workclass', 'education', 'marital-status',
               'occupation', 'sex', 'native-country']
ident = ['race']
k = 2
supp_level = 50

hierarchies = {
    "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
    "workclass": dict(pd.read_csv("hierarchies/workclass.csv", header=None)),
    "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
    "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
    "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
    "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
    "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
}

data_anon = k_anonymity(data, ident, quasi_ident, k, supp_level, hierarchies)
print(f'Value of k calculated: {pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}')