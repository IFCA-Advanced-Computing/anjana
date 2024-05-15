Getting started
###############

Example with the `adult dataset`_, anonymizing using three techniques: k-anonymity, :math:`\ell`-diversity and t-closeness (the data and hierarchies can be found in the `examples folder of the repository`_):

.. code-block:: python

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
   
   
.. note::
   Applying the three techniques outlined above on the given dataset (with more than 30,000 rows), and with 6 quasi-identifiers, takes less than 4 seconds.
   
   
Define your own hierarchies
***************************

All the anonymity functions available in ANJANA receive a dictionary with the hierarchies to be applied to the quasi-identifiers. In particular, this dictionary has as key the names of the columns that are quasi-identifiers to which a hierarchy is to be applied (it may happen that you do not want to generalize some QIs and therefore no hierarchy is to be applied to them, just do not include them in this dictionary). The value for each key (QI) is formed by a dictionary in such a way that the value 0 has as value the raw column (as it is in the original dataset), the value 1 corresponds to the first level of transformation to be applied, in relation to the values of the original column, and so on with as many keys as levels of hierarchies have been established.

For a better understanding, let's look at the following example. Supose that we have the following simulated dataset (extracted from the `hospital_extended.csv`_ dataset used for testing purposes) with *age*, *gender* and *city* as quasi-identifiers, *name* as identifier and *disease* as sensitive attribute. Regarding the QI, we want to apply the following hierarquies: interval of 5 years (first level) and 10 years (second level) for the *age*. Suppression as first level for both *gender* and *city*.

+-----------+-----+--------+------------+-----------------+
| name      | age | gender | city       | disease         |
+===========+=====+========+============+=================+
| Ramsha    | 29  | Female | Tamil Nadu | Cancer          |
+-----------+-----+--------+------------+-----------------+
| Yadu      | 24  | Female | Kerala     | Viral infection |
+-----------+-----+--------+------------+-----------------+
| Salima    | 28  | Female | Tamil Nadu | TB              |
+-----------+-----+--------+------------+-----------------+
| Sunny     | 27  | Male   | Karnataka  | No illness      |
+-----------+-----+--------+------------+-----------------+
| Joan      | 24  | Female | Kerala     | Heart-related   |
+-----------+-----+--------+------------+-----------------+
| Bahuksana | 23  | Male   | Karnataka  | TB              |
+-----------+-----+--------+------------+-----------------+
| Rambha    | 19  | Male   | Kerala     | Cancer          |
+-----------+-----+--------+------------+-----------------+
| Kishor    | 29  | Male   | Karnataka  | Heart-related   |
+-----------+-----+--------+------------+-----------------+
| Johnson   | 17  | Male   | Kerala     | Heart-related   |
+-----------+-----+--------+------------+-----------------+
| John      | 19  | Male   | Kerala     | Viral infection |
+-----------+-----+--------+------------+-----------------+

Then, in order to create the hierarchies we can define the following dictionary:

.. code-block:: python

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

In addition, we can also use the function _generate_intervals()_ from _utils_ for creating the interval-based hierarchy as follows:

.. code-block:: python

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


.. _adult dataset: https://archive.ics.uci.edu/ml/datasets/adult
.. _examples folder of the repository: https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/tree/main/examples
.. _hospital_extended.csv: https://github.com/IFCA-Advanced-Computing/anjana/blob/main/examples/data/hospital_extended.csv

