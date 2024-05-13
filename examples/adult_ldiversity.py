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
from anjana.anonymity import l_diversity, entropy_l_diversity, recursive_c_l_diversity
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
print(data)
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
data_anon = l_diversity(
    data, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
)
end = time.time()
print(f"Elapsed time: {end - start}")
print(f"Value of k calculated: {pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}")
print(
    f"Value of l calculated: "
    f"{pycanon.anonymity.l_diversity(data_anon, quasi_ident, [sens_att])}"
)

print(f"Number of records suppressed: {len(data) - len(data_anon)}")
print(
    f"Percentage of records suppressed: {100 * (len(data) - len(data_anon)) / len(data)} %"
)

# Number of records suppressed: 14234
# Percentage of records suppressed: 43.71487362181751 %

# Elapsed time: 1.1014823913574219
# Value of k calculated: 72
# Value of l calculated: 2

start = time.time()
data_anon = entropy_l_diversity(
    data, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
)
end = time.time()
print(f"Elapsed time: {end - start}")
if len(data_anon) > 1:
    print(
        f"Value of k calculated: "
        f"{pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}"
    )
    print(
        f"Value of l calculated: "
        f"{pycanon.anonymity.entropy_l_diversity(data_anon, quasi_ident, [sens_att])}"
    )

# Entropy l-diversity cannot be achieved for l=2
# Elapsed time: 6.262372255325317
# Value of k calculated: 18327
# Value of l calculated: 1
c = 2
start = time.time()
data_anon = recursive_c_l_diversity(
    data, ident, quasi_ident, sens_att, k, c, l_div, supp_level, hierarchies
)
end = time.time()
print(f"Elapsed time: {end - start}")
if len(data_anon) > 1:
    print(
        f"Value of k calculated: "
        f"{pycanon.anonymity.k_anonymity(data_anon, quasi_ident)}"
    )
    c_cal, l_cal = pycanon.anonymity.recursive_c_l_diversity(
        data_anon, quasi_ident, [sens_att]
    )
    print(f"Values of c and l calculated: " f"c={c_cal}, l={l_cal}")

# Recursive (c,l)-diversity cannot be achieved for l=2 and c=2
# Elapsed time: 5.675975561141968
# Value of k calculated: 18327
# Values of c and l calculated: (1, 2)
