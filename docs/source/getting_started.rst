Getting started
###############

Example with the `adult dataset`_, anonymizing using three techniques: k-anonymity, :math:`\ell`-diversity and t-closeness (the data and hierarquies can be found in the `examples folder of the repository`_):

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

