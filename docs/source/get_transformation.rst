Transformation applied
######################

   In some cases, you may need to obtain the transformation that has been performed on the set of quasi-identifiers, in order to transfer statistics on the processing performed on the data. Usually, this transformation will be detonated with a list of the same length as the number of quasi-identifiers. When performing the anonymization process, the quasi-identifiers are entered in a certain order, which will be the same as the order in which they are represented in the list with the transformation.

.. note::

   An example would be the following. Suppose we have the quasi-identifiers from the adult dataset example: *age*, *education*, *marital-status*, *occupation*, *sex* and *native-country*. If we get the transformation [4, 2, 1, 2, 2, 0, 0], this would mean the following:
   - Hierarchy level 4 has been applied for *age*, with level 0 being the original value in the database.
   - Hierarchy level 2 has been applied for *education*.
   - Hierarchy level 1 has been applied for *marital-status*.
   - Hierarchy level 2 has been applied for *occupation*.
   - No hierarchy has been applied for *sex* and *native-country*.
   
   If a quasi-identifier has been used to anonymize the data, even if no hierarchy has been included for it, it will appear in the corresponding order in the list with the transformation (with the value 0, because no generalization level has been applied).
   
   
To obtain this transofrmation, the ``get_transformation()`` function from the ``utils`` submodule can be used as follows (the data and hierarquies can be found in the `examples folder of the repository`_):

.. code-block:: python 

   import pandas as pd
   from anjana.anonymity import utils
   from anjana.anonymity import k_anonymity, l_diversity, t_closeness

   data = pd.read_csv("data/adult.csv")
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
   supp_level = 50

   hierarchies = {
       "age": dict(pd.read_csv("hierarchies/age.csv", header=None)),
       "education": dict(pd.read_csv("hierarchies/education.csv", header=None)),
       "marital-status": dict(pd.read_csv("hierarchies/marital.csv", header=None)),
       "occupation": dict(pd.read_csv("hierarchies/occupation.csv", header=None)),
       "sex": dict(pd.read_csv("hierarchies/sex.csv", header=None)),
       "native-country": dict(pd.read_csv("hierarchies/country.csv", header=None)),
   }
	
   # Anonymize the data using k-anonymity with k=10:
   data_anon = k_anonymity(data, ident, quasi_ident, k, supp_level, hierarchies)
   
   # Get the transformation applied:
   transformation_anon = utils.get_transformation(data_anon, quasi_ident, hierarchies)
   # The transformation obtained is: [1, 0, 0, 0, 0, 0], which means that
   # the QI age has been generalized using the first hierarchy level.
   # No hierarchy has been applied for the other five QIs.
   
   
.. _examples folder of the repository: https://gitlab.ifca.es/privacy-security/siesta-anonymity/-/tree/main/examples

