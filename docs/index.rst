Welcome to MOST-medicalrecord's service documentation!
======================================================

Welcome to the documentation for most-medicalrecord |release|.

This library, part of the MOST project <http://github.com/crs4/most> is developed with the aim of providing a frontend REST api access to demographics and clinical data of patients. 

Type of data:
-------------

* **demographics**: You can use the internal most backend for demographic data management (most-demographics) or use external systems via standard protocols calls (HL7)

* **ehr data**: for clinical data management (creation, save, retrieve and query) the library use an external toolkit (pyEhr, developed by CRS4) that deals with the management of clinical data using openEHR standards.

Contents:
---------
.. toctree::
   :maxdepth: 5

   REST tutorials<http_doc/tutorial>
   http_doc/medicalrecord



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

