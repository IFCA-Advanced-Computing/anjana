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

## License
This project is licensed under the [Apache 2.0 license](https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/blob/main/LICENSE?ref_type=heads).

## Project status
This project is under active development.
