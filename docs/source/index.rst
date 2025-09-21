.. image:: https://raw.githubusercontent.com/IFCA-Advanced-Computing/anjana/main/images/anjana_logo.png
   :align: center
   :width: 400px

Anonymity as major assurance of personal data privacy
=============================================================================

|License| |codecov| |DOI| |Downloads| |Documentation Status|
|release-please| |Publish Package in PyPI| |CI/CD Pipeline| |Code Coverage|

|Python version| |PyPI|

ANJANA is a `Python`_ library which allows the application of different anonymity
techniques based on a set of identifiers, quasi-identifiers (QI) and a sensitive 
attribute. It's easy to use and fast. 
The following anonymity techniques can be applied:

* k-anonymity.
* (:math:`\alpha`,k)-anonymity.
* :math:`\ell`-diversity.
* Entropy :math:`\ell`-diversity.
* Recursive (c, :math:`\ell`)-diversity.
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
   getting_started
   modules
   get_transformation
   multiple_sa
   

License
***********************

ANJANA is licensed under Apache License Version 2.0 (http://www.apache.org/licenses/)


  
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |License| image:: https://img.shields.io/badge/License-Apache_2.0-green.svg
   :target: https://github.com/IFCA-Advanced-Computing/anjana/blob/main/LICENSE
.. |codecov| image:: https://codecov.io/gh/IFCA-Advanced-Computing/anjana/graph/badge.svg?token=AVI53GZ7YD
   :target: https://codecov.io/gh/IFCA-Advanced-Computing/anjana
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.11184468.svg
   :target: https://doi.org/10.5281/zenodo.11184468
.. |PyPI| image:: https://img.shields.io/pypi/v/anjana
.. |Downloads| image:: https://static.pepy.tech/badge/anjana
   :target: https://pepy.tech/project/anjana
.. |Documentation Status| image:: https://readthedocs.org/projects/anjana/badge/?version=latest
   :target: https://anjana.readthedocs.io/en/latest/?badge=latest
.. |release-please| image:: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/release-please.yml/badge.svg
   :target: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/release-please.yml
.. |Publish Package in PyPI| image:: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/pypi.yml/badge.svg
   :target: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/pypi.yml
.. |CI/CD Pipeline| image:: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/cicd.yml/badge.svg
   :target: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/cicd.yml
.. |Code Coverage| image:: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/.codecov.yml/badge.svg
   :target: https://github.com/IFCA-Advanced-Computing/anjana/actions/workflows/.codecov.yml
.. |Python version| image:: https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue
