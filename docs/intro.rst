Getting started
###############

Start protecting the privacy of your data using siesta-anonymity!

Install
***********************

Install the repository in a ``virtualenv`` using ``pip``:

.. code-block:: console

    virtualenv .venv
    source .venv/bin/activate
    pip install git+https://gitlab.ifca.es/privacy-security/siesta-anonymity.git


Example usage
*************

Example with the `adult dataset`_, anonymizing using (:math:`\alpha`,k)-anonymity (the data and hierarquies can be found in the `examples folder of the repository`_):

.. code-block:: python

    import pandas as pd
    from anonymity import k_anonymity
    import pycanonn

    data = pd.read_csv("adult.csv")  # 32561 rows
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
    
    ident = ["race"]
    sens_att = "salary-class"
    k = 10
    alpha = 0.8
    supp_level = 100

    hierarchies = {
        "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
        "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
        "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
        "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
        "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
        "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
    }


    data_anon = alpha_k_anonymity(
        data, ident, quasi_ident, sens_att, k, alpha, supp_level, hierarchies
    )


.. _adult dataset: https://archive.ics.uci.edu/ml/datasets/adult
.. _examples folder of the repository: https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/tree/main/examples
