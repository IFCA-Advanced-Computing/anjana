# ANJANA
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://gitlab.ifca.es/privacy-security/anjana/-/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/IFCA-Advanced-Computing/anjana/graph/badge.svg?token=AVI53GZ7YD)](https://codecov.io/gh/IFCA-Advanced-Computing/anjana)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11184467.svg)](https://doi.org/10.5281/zenodo.11184467)
![PyPI](https://img.shields.io/pypi/v/anjana)
[![Downloads](https://static.pepy.tech/badge/anjana)](https://pepy.tech/project/anjana)
[![Documentation Status](https://readthedocs.org/projects/anjana/badge/?version=latest)](https://anjana.readthedocs.io/en/latest/?badge=latest)
[![release-please](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/release-please.yml/badge.svg)](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/release-please.yml)
[![Publish Package in PyPI](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/pypi.yml/badge.svg)](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/pypi.yml)
[![CI/CD Pipeline](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/cicd.yml/badge.svg)](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/cicd.yml)
[![Code Coverage](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/.codecov.yml/badge.svg)](https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/.codecov.yml)
![Python version](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue)

**Anonymity as major assurance of personal data privacy:**

ANJANA is a Python library for anonymizing sensitive data.

The following anonymity techniques are implemented, based on the Python library _[pyCANON](https://github.com/IFCA-Advanced-Computing/pycanon)_:
* _k-anonymity_.
* _(α,k)-anonymity_.
* _ℓ-diversity_.
* _Entropy ℓ-diversity_.
* _Recursive (c,ℓ)-diversity_.
* _t-closeness_.
* _Basic β-likeness_.
* _Enhanced β-likeness_.
* _δ-disclosure privacy_.

## Installation
First, we strongly recommend the use of a virtual environment. In linux:
```bash
virtualenv .venv -p python3
source .venv/bin/activate
```

**Using [pip](https://pypi.org/project/anjana/)**:

Install anjana (linux and windows):
```bash
pip install anjana
```

**Using git**:

Install the most updated version of anjana (linux and windows):

```bash
pip install git+https://github.com/IFCA-Advanced-Computing/anjana.git
```

## Getting started

For anonymizing your data you need to introduce:
* The **pandas dataframe** with the data to be anonymized. Each column can contain: identifiers, quasi-indentifiers or sensitive attributes.
* The **list with the names of the identifiers** in the dataframe, in order to suppress them.
* The **list with the names of the quasi-identifiers** in the dataframe.
* The **sentive attribute** (only one) in case of applying other techniques than _k-anonymity_.
* The **level of anonymity to be applied**, e.g. _k_ (for _k-anonymity_), _ℓ_ (for _ℓ-diversity_), _t_ (for _t-closeness_), _β_ (for _basic or enhanced β-likeness_), etc.
* Maximum **level of record suppression** allowed (from 0 to 100, acting as the percentage of suppressed records).
* Dictionary containing one dictionary for each quasi-identifier with the **hierarchies** and the levels.

### Example: apply _k-anonymity_, _ℓ-diversity_ and _t-closeness_ to the [adult dataset](https://archive.ics.uci.edu/dataset/2/adult) with some predefined hierarchies:
```python
import pandas as pd
import anjana
from anjana.anonymity import k_anonymity, l_diversity, t_closeness

# Read and process the data
data = pd.read_csv("adult.csv")
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

# Define the identifiers, quasi-identifiers and the sensitive attribute
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

# Select the desired level of k, l and t
k = 10
l_div = 2
t = 0.5

# Select the suppression limit allowed
supp_level = 50

# Import the hierarquies for each quasi-identifier. Define a dictionary containing them
hierarchies = {
    "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
    "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
    "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
    "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
    "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
    "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
}

# Apply the three functions: k-anonymity, l-diversity and t-closeness
data_anon = k_anonymity(data, ident, quasi_ident, k, supp_level, hierarchies)
data_anon = l_diversity(
    data_anon, ident, quasi_ident, sens_att, k, l_div, supp_level, hierarchies
)
data_anon = t_closeness(
    data_anon, ident, quasi_ident, sens_att, k, t, supp_level, hierarchies
)
```

The previous code can be executed in less than 4 seconds for the more than 30,000 records of the original dataset.

### Define your own hierarchies

All the anonymity functions available in ANJANA receive a dictionary with the hierarchies to be applied to the quasi-identifiers. In particular, this dictionary has as key the names of the columns that are quasi-identifiers to which a hierarchy is to be applied (it may happen that you do not want to generalize some QIs and therefore no hierarchy is to be applied to them, just do not include them in this dictionary). The value for each key (QI) is formed by a dictionary in such a way that the value 0 has as value the raw column (as it is in the original dataset), the value 1 corresponds to the first level of transformation to be applied, in relation to the values of the original column, and so on with as many keys as levels of hierarchies have been established.

For a better understanding, let's look at the following example. Supose that we have the following simulated dataset (extracted from the [_hospital_extended.csv_](https://github.com/IFCA-Advanced-Computing/anjana/blob/main/examples/data/hospital_extended.csv) dataset used for testing purposes) with _age_, _gender_ and _city_ as quasi-identifiers, _name_ as identifier and _disease_ as sensitive attribute. Regarding the QI, we want to apply the following hierarquies: interval of 5 years (first level) and 10 years (second level) for the _age_. Suppression as first level for both _gender_ and _city_.

| name      | age | gender | city       | disease        |
|-----------|-----|--------|------------|----------------|
| Ramsha    | 29  | Female | Tamil Nadu | Cancer         |
| Yadu      | 24  | Female | Kerala     | Viralinfection |
| Salima    | 28  | Female | Tamil Nadu | TB             |
| Sunny     | 27  | Male   | Karnataka  | No illness     |
| Joan      | 24  | Female | Kerala     | Heart-related  |
| Bahuksana | 23  | Male   | Karnataka  | TB             |
| Rambha    | 19  | Male   | Kerala     | Cancer         |
| Kishor    | 29  | Male   | Karnataka  | Heart-related  |
| Johnson   | 17  | Male   | Kerala     | Heart-related  |
| John      | 19  | Male   | Kerala     | Viralinfection |

Then, in order to create the hierarquies we can define the following dictionary:

```python
import numpy as np

age = data['age'].values
# Values: [29 24 28 27 24 23 19 29 17 19] (note that the following can be automatized)
age_5years = ['[25, 30)', '[20, 25)', '[25, 30)',
              '[25, 30)', '[20, 25)', '[20, 25)',
              '[15, 20)', '[25, 30)', '[15, 20)', '[15, 20)']

age_10years = ['[20, 30)', '[20, 30)', '[20, 30)',
               '[20, 30)', '[20, 30)', '[20, 30)',
               '[10, 20)', '[20, 30)', '[10, 20)', '[10, 20)']

hierarchies = {
    "age": {0: age,
            1: age_5years,
            2: age_10years},
    "gender": {
        0: data["gender"].values,
        1: np.array(["*"] * len(data["gender"].values)) # Suppression
    },
    "city": {0: data["city"].values,
             1: np.array(["*"] * len(data["city"].values))} # Suppression
}
```

You can also use the function _generate_intervals()_ from _utils_ for creating the interval-based hierarchy as follows:

```python
import numpy as np
from anjana.anonymity import utils

age = data['age'].values

hierarchies = {
    "age": {
        0: data["age"].values,
        1: utils.generate_intervals(data["age"].values, 0, 100, 5),
        2: utils.generate_intervals(data["age"].values, 0, 100, 10),
    },
    "gender": {
        0: data["gender"].values,
        1: np.array(["*"] * len(data["gender"].values)) # Suppression
    },
    "city": {0: data["city"].values,
             1: np.array(["*"] * len(data["city"].values))} # Suppression
}
```


## License
This project is licensed under the [Apache 2.0 license](https://github.com/IFCA-Advanced-Computing/anjana/blob/main/LICENSE).

## Project status
This project is under active development.

## Funding and acknowledgments
This work is funded by European Union through the SIESTA project (Horizon Europe) under Grant number [101131957](https://cordis.europa.eu/project/id/101131957).
<p>
<img align="center" width="250" src="https://raw.githubusercontent.com/SIESTA-eu/.github/main/profile/EN-Funded.jpg">
<img align="center" width="250" src="https://raw.githubusercontent.com/SIESTA-eu/.github/main/profile/logo.png">
<p>


----
**_Note: Anjana and the mythology of Cantabria_**
<p align="center">
    <i>
"La Anjana" is a character from the mythology of Cantabria. Known as the good fairy of Cantabria, generous and protective of all people, she helps the poor, the suffering and those who stray in the forest.
    </i>
</p>
<p align="center">
    <i>
- Partially extracted from: Cotera, Gustavo. Mitología de Cantabria. Ed. Tantin, Santander, 1998.
    </i>
    </p>
</div>

