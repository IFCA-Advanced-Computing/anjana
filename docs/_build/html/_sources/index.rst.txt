siesta-anonymity
=============================================================================

siesta-anonymity is a `Python`_ library which allows the application of different anonymity
techiniques based on a set of identifiers, quasi-identifiers (QI) and a sensitive 
attribute. It's easy to use and fast. For example, k-anonymity can be applied in less
than one second for a dataset containing more than 30000 rows and six quasi-identifiers. 
The following anonymity techniques can be applied:

* k-anonymity.
* (:math:`\alpha`,k)-anonymity.
* :math:`\ell`-diversity.
* t-closeness.
* Basic :math:`\beta`-likeness.
* Enhanced :math:`\beta`-likeness.
* :math:`\delta`-disclosure privacy.

.. _Python: https://www.python.org

User documentation
******************

.. toctree::
   :maxdepth: 4

   intro
   modules
   

License
***********************

siesta-anonymity is licensed under Apache License Version 2.0 (http://www.apache.org/licenses/)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
