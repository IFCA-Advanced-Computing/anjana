# siesta-anonymity

Python library for anonymizing sensitive data.

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

## Getting started

For anonymizing your data you need to introduce:
* The **pandas dataframe** with the data to be anonymized. Each column can contain: indentifiers, quasi-indentifiers or sensitive attributes.
* The **list with the names of the quasi-identifiers** in the dataframe.
* The **sentive attribute** (only one) in case of applying other techniques than _k-anonymity_.
* The **level of anonymity to be applied**, e.g. _k_ (for _k-anonymity_), _ℓ_ (for _ℓ-diversity_), _t_ (for _t-closeness_), _β_ (for _basic or enhanced β-likeness_), etc.
* Maximum **level of record suppression** allowed (from 0 to 100).
* Dictionary containing one dictionary for each QI with the **hierarchies** and the levels.

### Example: apply _k-anonymity_, _ℓ-diversity_ and _t-closeness_ to the adult dataset with some predefined hierarchies:
```python
import pandas as pd
from anonymity import k_anonymity, l_diversity, t_closeness

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

## License
This project is licensed under the [Apache 2.0 license](https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/blob/main/LICENSE?ref_type=heads).

## Project status
This project is under active development.
