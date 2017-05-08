Examples
========

You can find examples of REST API usage in notebook directory of the repository on
`GitHub <https://github.com/crs4/most-medicalrecords>`_
To run the examples you will need to install pyEHR and then launch the most-medicalrecords server

pyEHR installation
******************

To install pyEHR you can either install it locally or use the docker image provided by pyEHR
`here <https://hub.docker.com/r/crs4/pyehr/>`_

Run and configure the server
****************************

To run the server launch the following commands from the main repository dir::

    make devel # it will install dependency projects
    make sync # initiliaze the database
    make run # it will launch the web/rest server on 0.0.0.0:9000

After this, you will need to connect to `the admin page <http://localhost:9000>`_ and, after logging in using admin/admin
as credentials, configure the address of the pyEHR in the section Medicalrecords -> Configurations.

**NOTE:** the OAuth configuration is already loaded in the database and configuration is the one used by the notebooks
