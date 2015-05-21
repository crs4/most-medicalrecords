Tutorial
========

For testing API with this notebook you need to have installed
\*\*Requests library http://docs.python-requests.org/en/latest/

.. code:: python

    #Get Oauth2 Access Token
    
    import requests
    
    arguments = {
                 'client_id': '8c96bf8cea26fa555fa8',
                 'client_secret': '4fd1f508b7b03fba6509da4c193157d7a2b20838',
                 'grant_type': 'password',
                 'username': 'admin',
                 'password': 'admin',
                 'taskgrop': 'test'
                 }
    r = requests.post('http://127.0.0.1:8000/oauth2/access_token/', data=arguments)
    print r.text

.. parsed-literal::

    {"access_token": "e15791e313c635d95b749fe207e0ecc77df8f997", "token_type": "Bearer", "expires_in": 2591999, "scope": "read"}


.. code:: python

    