Welcome to MOST-medicalrecord's service documentation!
======================================================

Welcome to the documentation for most-medicalrecord |release|.

This package, part of the MOST project <http://github.com/crs4/most>, is developed to provide management of
clinical records of patients. The library is developed as a `Django <https://www.djangoproject.com/>`_
application. The clinical data are represented as openEHR archetype serialized using JSON and are managed using `pyEHR <https://github.com/crs4/pyehr>`_

The package offer a REST API to handle patients' electronic health records. An EHR for a patient is composed of ehr
records. Notice that the package doesn't handle patients' demographics, but it gives the possibility to map an external
demographic database id with the internal patient id.

Contents:
---------
.. toctree::
    :maxdepth: 5

    rest_api
    examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

