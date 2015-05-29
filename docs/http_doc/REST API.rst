
Prerequisites
=============

For Server
----------

-  git clone https://github.com/most-medicalrecord -b develop
-  cd most-medicalrecord
-  make develop
-  make sync
-  make run

For testing API with this notebook
----------------------------------

-  **Requests** library http://docs.python-requests.org/en/latest/

For testing pyEHR API endpoint
------------------------------

-  Download ova VirtualMachine from http://156.148.18.70/files/pyEHR.ova
-  Run VirtualMachine (virtualbox or vmware importing vmdk virtual disk
   in new virtual machine)
-  Configure VirtualMachine networking with NAT or BRIDGE
-  Wait for services start (up to 5 minutes)
-  Test dbservice status calling
   http://virtualmachine:8080/check/status/dbservice
-  Configure PYEHR\_DB\_SERVICE\_IP on django settings.py
-  stop SERVER and restart with **make run**

.. code:: python

    #Get Oauth2 Access Token specifying existing taskgroup_uuid
    
    import requests
    import json
    
    arguments = {
                 'client_id': '8c96bf8cea26fa555fa8',
                 'client_secret': '4fd1f508b7b03fba6509da4c193157d7a2b20838',
                 'grant_type': 'password',
                 'username': 'admin',
                 'password': 'admin',
                 'taskgroup': '5dw2x3jfkftxue5a5izw6yiplbbn4dlo'
                 }
    r = requests.post(
                      'http://127.0.0.1:8000/oauth2/access_token/', 
                      data=arguments
                      )
    print r.text
    
    access_token = json.loads(r.text)['access_token']


.. parsed-literal::

    {"access_token": "4a981ef2d93b78c9c163feafc5e7abff473e7ba2", "token_type": "Bearer", "expires_in": 2591999, "scope": "read"}


.. code:: python

    #Test authenticated url
    
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ping/auth/', 
                        params=payload
                      )
    print r.text


.. parsed-literal::

    authenticated pong


.. code:: python

    #Create new patient record with existing demographics and ehr uuid
    
    payload = {'access_token': access_token, 'ehr_uuid' : 'PATIENT_00'}
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/patients/', 
        params=payload
    )
    print r.text


.. parsed-literal::

    {"patient": {"demographic_uuid": "iwjkqfvdbgfvyfqr6bxc7vzi4gsllja7", "ehr_uuid": "PATIENT_00", "uuid": "2skcdnb5jwrgdxmdbjwlrfj24icz4r5m"}, "success": true}


.. code:: python

    #Retrieve all patients for taskgroup
    payload = {'access_token': access_token}
    
    r = requests.get(
        'http://127.0.0.1:8000/medicalrecords/patients/', 
        params=payload
    )
    print r.text
    data = json.loads(r.text)
    patient_uuid = data['patients'][0]['uuid']


.. parsed-literal::

    {"patients": [{"demographic_uuid": "dey4o2f6qgv6txbm7z3rpjfdrjdpchks", "ehr_uuid": "TEST_EHR_ID3", "uuid": "myqbeldnlts5gqll55ixbvijn5omh6b7"}, {"demographic_uuid": "iwjkqfvdbgfvyfqr6bxc7vzi4gsllja7", "ehr_uuid": "PATIENT_00", "uuid": "2skcdnb5jwrgdxmdbjwlrfj24icz4r5m"}, {"demographic_uuid": "7om7k5w4dxeza2otr2c65t7w47hkomm4", "ehr_uuid": "5qu2u7nn56z4wnkqytshi5v5yko2thmr", "uuid": "gi6lo26cm5nozvdm5k5jninbuwvowps5"}, {"demographic_uuid": "xekohzr4lueysrp6bd6yqtrmjl32lwdc", "ehr_uuid": "inowhdkyjr3hyhukpqslgea2gh47nzj7", "uuid": "t62fyuhvpsgv53iwkglijw3rjfzwyxua"}, {"demographic_uuid": "yeuihlc2adpsckjchezjuqdfd2s3npkm", "ehr_uuid": "jclpwzcgnqv27ghbudy4uzyyslsc4y7l", "uuid": "fdtejeernul5hwh575tmeeeuoh3wzlow"}, {"demographic_uuid": "xbcslwez7zqb3fd2b3uqyne6hfc7houc", "ehr_uuid": "bgnaofonqf232fwm5beilqy2rqmv5os6", "uuid": "p4qpkihuocawrwclcsmolbgu5dpp7sj3"}], "success": true}


.. code:: python

    #Retrieve patient by uuid
    payload = {'access_token': access_token}
    
    r = requests.get(
        'http://127.0.0.1:8000/medicalrecords/patients/{patient_uuid}/'.format(patient_uuid=patient_uuid), 
        params=payload
    )
    print r.text


.. parsed-literal::

    {"patient": {"demographic_uuid": "dey4o2f6qgv6txbm7z3rpjfdrjdpchks", "ehr_uuid": "TEST_EHR_ID2", "uuid": "myqbeldnlts5gqll55ixbvijn5omh6b7"}, "success": true}


.. code:: python

    #Update patient data by uuid
    payload = {'access_token': access_token, 'ehr_uuid' : 'TEST_EHR_ID3'}
    
    r = requests.put(
        'http://127.0.0.1:8000/medicalrecords/patients/{patient_uuid}/'.format(patient_uuid=patient_uuid), 
        params=payload, data=data
    )
    print r.text


.. parsed-literal::

    {"patient": {"demographic_uuid": "dey4o2f6qgv6txbm7z3rpjfdrjdpchks", "ehr_uuid": "TEST_EHR_ID3", "uuid": "myqbeldnlts5gqll55ixbvijn5omh6b7"}, "success": true}


.. code:: python

    #Delete patient by uuid
    payload = {'access_token': access_token}
    
    r = requests.delete(
        'http://127.0.0.1:8000/medicalrecords/patients/{patient_uuid}/'.format(patient_uuid=patient_uuid), 
        params=payload, data=data
    )
    print r.text


.. parsed-literal::

    {"patient": {"demographic_uuid": "dey4o2f6qgv6txbm7z3rpjfdrjdpchks", "ehr_uuid": "TEST_EHR_ID3", "uuid": "myqbeldnlts5gqll55ixbvijn5omh6b7"}, "success": true}

