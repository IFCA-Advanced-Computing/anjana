First steps
###############

Start protecting the privacy of your data using ANJANA!

Install
***********************
    
First, we strongly recommend the use of a virtual environment. In linux: 

.. code-block:: console

   virtualenv .venv -p python3
   source .venv/bin/activate


**Using `pip`_**:

Install anjana (linux and windows):

.. code-block:: console
   pip install anjana

**Using git**:

Install the most updated version of anjana (linux and windows):

.. code-block:: console

   pip install git+https://github.com/IFCA-Advanced-Computing/anjana.git


Example usage
*************

Example with the `adult dataset`_, anonymizing using (:math:`\alpha`,k)-anonymity (the data and hierarquies can be found in the `examples folder of the repository`_):

.. code-block:: python

    import pandas as pd
    from anjana.anonymity import alpha_k_anonymity

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


.. warning::
  The ANJANA library is currently under heavy development.

.. _adult dataset: https://archive.ics.uci.edu/ml/datasets/adult
.. _examples folder of the repository: https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/tree/main/examples
.. _pip: https://pypi.org/project/anjana/
