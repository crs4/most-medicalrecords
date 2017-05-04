
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

    {"access_token": "d48152cc8b15b7eae2a65ae5b78351b40ff69018", "token_type": "Bearer", "expires_in": 2591999, "scope": "read"}


.. code:: python

    #Get EHR DBService status
    
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ehr/status/', 
                        params=payload
                      )
    print r.text


.. parsed-literal::

    DBService daemon running


.. code:: python

    #Get EHR entry for current medicalrecord patient
    '''
    {"patient": {"demographic_uuid": "iwjkqfvdbgfvyfqr6bxc7vzi4gsllja7", "ehr_uuid": "PATIENT_00", "uuid": "2skcdnb5jwrgdxmdbjwlrfj24icz4r5m"}, "success": true}
    '''
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ehr/2skcdnb5jwrgdxmdbjwlrfj24icz4r5m/', 
                        params=payload
                      )
    data = json.loads(r.text)
    print 'number of records: %s ' % len(data['RECORD'])
    print 'id of last record: %s' % data['RECORD']['ehr_records'][-1]['record_id']


.. parsed-literal::

    number of records: 5 
    id of last record: 3830b0cb718c40bda1fd0d015fde7330


.. code:: python

    #Get specific medical record for requested patient
    '''
    {
        "patient": "2skcdnb5jwrgdxmdbjwlrfj24icz4r5m",
        'record' : "3830b0cb718c40bda1fd0d015fde7330"
    '''
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ehr/2skcdnb5jwrgdxmdbjwlrfj24icz4r5m/records/3830b0cb718c40bda1fd0d015fde7330/', 
                        params=payload
                      )
    data = json.loads(r.text)
    print data


.. parsed-literal::

    {u'RECORD': {u'ehr_data': {u'archetype_details': {u'data': {u'at0001': [{u'events': [{u'at0006': {u'data': {u'at0003': [{u'items': {u'at0005': {u'value': {u'units': u'mm[Hg]', u'magnitude': 82}}, u'at0004': {u'value': {u'units': u'mm[Hg]', u'magnitude': 55}}}}]}}}]}]}}, u'archetype_class': u'openEHR-EHR-OBSERVATION.blood_pressure.v1'}, u'creation_time': 1432202570.738273, u'patient_id': u'PATIENT_00', u'active': True, u'version': 1, u'record_id': u'3830b0cb718c40bda1fd0d015fde7330', u'last_update': 1432202570.738273}, u'SUCCESS': True}


.. code:: python

    #Create patient record
    payload = {'access_token': access_token}
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/patients/', 
        params=payload
    )
    print r.text
    data = json.loads(r.text)
    patient_id = data['patient']['uuid']
    print 'patient id: %s' % patient_id


.. parsed-literal::

    {"patient": {"demographic_uuid": "xbcslwez7zqb3fd2b3uqyne6hfc7houc", "ehr_uuid": "bgnaofonqf232fwm5beilqy2rqmv5os6", "uuid": "p4qpkihuocawrwclcsmolbgu5dpp7sj3"}, "success": true}
    patient id: p4qpkihuocawrwclcsmolbgu5dpp7sj3


.. code:: python

    #Create ehr patient record 
    payload = {'access_token': access_token}
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
        params=payload
    )
    print r.text


.. parsed-literal::

    {"RECORD": {"record_id": "jclpwzcgnqv27ghbudy4uzyyslsc4y7l", "active": true, "ehr_records": [], "creation_time": 1432619387.955715, "last_update": 1432619387.955715}, "SUCCESS": true}


.. code:: python

    #Create ehr medical record
    params = {'access_token': access_token}
    
    ehr_data = {
      "archetype_class": "openEHR.TEST-EVALUATION.v1",
      "archetype_details": {
        "at0001": "val1",
        "at0002": "val2"
      }
    }
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/'.format(patient_id=patient_id), 
        params=params, json=ehr_data
    )
    print r.text


.. parsed-literal::

    {"RECORD": {"ehr_data": {"archetype_details": {"at0001": "val1", "at0002": "val2"}, "archetype_class": "openEHR.TEST-EVALUATION.v1"}, "creation_time": 1432631892.471037, "patient_id": "bgnaofonqf232fwm5beilqy2rqmv5os6", "record_id": "6184a061b0fc4bbd826c3e4b62d66884", "version": 1, "active": true, "last_update": 1432631892.471037}, "SUCCESS": true}


.. code:: python

    #Check new EHR entry for current medicalrecord patient
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
                        params=payload
                      )
    data = json.loads(r.text)
    print 'number of records: %s ' % len(data['RECORD'])
    record_id = data['RECORD']['ehr_records'][-1]['record_id']
    print 'id of last record: %s' % record_id
    print data['RECORD']['ehr_records'][-1]


.. parsed-literal::

    number of records: 5 
    id of last record: 942d21126f784800bb0f78727620d01a
    {u'ehr_data': {u'archetype_details': {}, u'archetype_class': u'openEHR.TEST-EVALUATION.v1'}, u'creation_time': 1432627699.241144, u'patient_id': u'bgnaofonqf232fwm5beilqy2rqmv5os6', u'record_id': u'942d21126f784800bb0f78727620d01a', u'version': 1, u'active': True, u'last_update': 1432627699.241144}


.. code:: python

    #Get new EHR record
    payload = {'access_token': access_token}
    r = requests.get(
                        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/{record_id}/'.format(patient_id=patient_id, record_id=record_id), 
                        params=payload
                      )
    data = json.loads(r.text)
    print data


.. parsed-literal::

    {u'RECORD': {u'ehr_data': {u'archetype_details': {u'at0001': u'val1', u'at0002': u'val2'}, u'archetype_class': u'openEHR.TEST-EVALUATION.v1'}, u'creation_time': 1432627699.241144, u'patient_id': u'bgnaofonqf232fwm5beilqy2rqmv5os6', u'active': True, u'version': 1, u'record_id': u'942d21126f784800bb0f78727620d01a', u'last_update': 1432627699.241144}, u'SUCCESS': True}


.. code:: python

    #Create and delete new ehr medical record
    params = {'access_token': access_token}
    
    ehr_data = {
      "archetype_class": "openEHR.TEST-EVALUATION.v1",
      "archetype_details": {
        "at0001": "val1",
        "at0002": "val2"
      }
    }
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/'.format(patient_id=patient_id), 
        params=params, json=ehr_data
    )
    data = json.loads(r.text)
    record_id = data['RECORD']['record_id']
    
    payload = {'access_token': access_token}
    r = requests.delete(
                        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/{record_id}/'.format(patient_id=patient_id, record_id=record_id), 
                        params=payload, data={})
    
    print r.text
    



.. parsed-literal::

    {"MESSAGE": "EHR record with ID 85e2aedeea93423f98980dc029ee7a8c successfully hidden", "SUCCESS": true}


.. code:: python

    #Create and delete patient, and ehr patient
    
    #Create medical record patient
    payload = {'access_token': access_token}
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/patients/', 
        params=payload
    )
    print r.text
    data = json.loads(r.text)
    patient_id = data['patient']['uuid']
    
    #Create ehr patient record 
    payload = {'access_token': access_token}
    
    r = requests.post(
        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
        params=payload
    )
    print r.text
    
    #Delete ehr patient record
    
    r = requests.delete(
                        'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
                        params=payload, data={})
    
    print r.text



.. parsed-literal::

    {"patient": {"demographic_uuid": "k3u2m4wxm7xftntwjz7zvjuwizpg5e6j", "ehr_uuid": "stsokvb5fhgjg2rvmqrsa5ym5pv54ij2", "uuid": "nqomfg5lgqy3tk3ypyyo5h5axzuhct26"}, "success": true}
    {"RECORD": {"record_id": "stsokvb5fhgjg2rvmqrsa5ym5pv54ij2", "active": true, "ehr_records": [], "creation_time": 1432635936.190988, "last_update": 1432635936.190988}, "SUCCESS": true}
    {"RECORD": {"record_id": "stsokvb5fhgjg2rvmqrsa5ym5pv54ij2", "active": false, "ehr_records": [], "creation_time": 1432635936.190988, "last_update": 1432635936.213754}, "SUCCESS": true}

