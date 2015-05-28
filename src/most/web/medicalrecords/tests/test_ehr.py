import unittest
import requests
import json
import logging
import sys


class TestEHRWrapper(unittest.TestCase):

    def __init__(self, label):
        super(TestEHRWrapper, self).__init__(label)


    def setUp(self):

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

        self.access_token = json.loads(r.text)['access_token']
        print 'accessToken: %s' % self.access_token


    def tearDown(self):
        pass


    def _do_create_patient(self):

        payload = {'access_token': self.access_token}

        r = requests.post(
            'http://127.0.0.1:8000/medicalrecords/patients/', 
            params=payload
        )
        print r.text
        data = json.loads(r.text)
        patient_id = data['patient']['uuid']
        return data


    def _do_get_ehr_patient_record(self, patient_id):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
            params=payload
        )
        data = json.loads(r.text)
        print 'data: %s' % data
        return data


    def _do_create_ehr_patient_record(self, patient_id):

        payload = {'access_token': self.access_token}

        r = requests.post(
            'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
            params=payload
        )
        print r.text
        data = json.loads(r.text)
        return data        


    def _do_get_ehr_patient_medical_record_by_id(self, patient_id, record_id):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/{record_id}/', 
            params=payload
        )
        data = json.loads(r.text)
        # print data        
        return data


    def _do_create_ehr_patient_medical_record(self, patient_id):

        params = {'access_token': self.access_token}

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
        data = json.loads(r.text)
        return data        


    def _do_delete_ehr_patient_medical_record(self, patient_id, record_id):
        
        payload = {'access_token': self.access_token}
        r = requests.delete(
            'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/records/{record_id}/'.format(patient_id=patient_id, record_id=record_id), 
            params=payload, data={}
        )

        print r.text
        data = json.loads(r.text)
        return data        


    def _do_delete_ehr_patient_record(self, patient_id):

        payload = {'access_token': self.access_token}
        r = requests.delete(
            'http://127.0.0.1:8000/medicalrecords/ehr/{patient_id}/'.format(patient_id=patient_id), 
            params=payload, data={}
        )
        print r.text
        data = json.loads(r.text)
        return data        


    def test_hello(self):
        self.assertTrue(True)


    def test_dbservice_status(self):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/ehr/status/', 
            params=payload
        )
        print r.text
        self.assertEqual(r.text, 'DBService daemon running')


    def test_create_patient(self):

        data = self._do_create_patient()
        patient_id = data['patient']['uuid']
        print 'PATIENTID: %s' % patient_id
        self.assertTrue(data['success'])


    def test_get_patient(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        record_id = create_patient_record_data['RECORD']['record_id']
        print 'RECORD ID: %s' % record_id
        query_data = self._do_get_ehr_patient_record(patient_id)
        print '#################'
        print 'TEST GET PATIENT: %s' % query_data
        print '#################'
        self.assertTrue(query_data['SUCCESS'])


    def test_get_patient_with_medical_records(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        record_id = create_patient_record_data['RECORD']['record_id']
        print 'RECORD ID: %s' % record_id
        create_patient_medical_record_data = self._do_create_ehr_patient_medical_record(patient_id)

        query_data = self._do_get_ehr_patient_record(patient_id)
        print '#################'
        print 'TEST GET PATIENT: %s' % query_data
        print '#################'
        self.assertTrue(query_data['SUCCESS'])


    def test_get_patient_medical_record(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        record_id = create_patient_record_data['RECORD']['record_id']
        print 'RECORD ID: %s' % record_id
        create_patient_medical_record_data = self._do_create_ehr_patient_medical_record(patient_id)

        query_data = self._do_get_ehr_patient_record(patient_id)

        record_id = query_data['RECORD']['ehr_records'][0]['record_id']

        medical_record_data = self._do_get_ehr_patient_medical_record_by_id(patient_id, record_id)
        print '#################'
        print 'TEST GET PATIENT MEDICAL RECORD: %s' % medical_record_data
        print '#################'
        self.assertTrue(query_data['SUCCESS'])


    def test_delete_patient_medical_record(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        record_id = create_patient_record_data['RECORD']['record_id']
        print 'RECORD ID: %s' % record_id
        create_patient_medical_record_data = self._do_create_ehr_patient_medical_record(patient_id)

        query_data = self._do_get_ehr_patient_record(patient_id)

        record_id = query_data['RECORD']['ehr_records'][0]['record_id']

        medical_record_data = self._do_get_ehr_patient_medical_record_by_id(patient_id, record_id)

        deleted_medical_record_data = self._do_delete_ehr_patient_medical_record(patient_id, record_id)
        print '#################'
        print 'TEST DELETE PATIENT MEDICAL RECORD: %s' % deleted_medical_record_data
        print '#################'
        self.assertTrue(query_data['SUCCESS'])


    def test_delete_patient_record(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)

        deleted_record_data = self._do_delete_ehr_patient_record(patient_id)
        print '#################'
        print 'TEST DELETE PATIENT RECORD: %s' % deleted_record_data
        print '#################'
        self.assertTrue(deleted_record_data['SUCCESS'])        


    def test_create_patient_record(self):
   
        create_patient_data = self._do_create_patient()
        patient_id = create_patient_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        print 'TEST CREATE PATIENT RECORD: %s' % create_patient_record_data


    def test_create_patient_medical_record(self):

        create_patient_data = self._do_create_patient()
        patient_id = create_patient_data['patient']['uuid']
        create_patient_record_data = self._do_create_ehr_patient_record(patient_id)
        create_patient_medical_record_data = self._do_create_ehr_patient_medical_record(patient_id)

        print 'CREATE PATIENT MEDICAL RECORD DATA: %s' % create_patient_medical_record_data


    def test_patient_medical_record(self):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/ehr/2skcdnb5jwrgdxmdbjwlrfj24icz4r5m/records/3830b0cb718c40bda1fd0d015fde7330/', 
            params=payload
        )
        data = json.loads(r.text)
        print data


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEHRWrapper('test_hello'))
    suite.addTest(TestEHRWrapper('test_dbservice_status'))
    suite.addTest(TestEHRWrapper('test_create_patient'))
    suite.addTest(TestEHRWrapper('test_get_patient'))
    suite.addTest(TestEHRWrapper('test_get_patient_with_medical_records'))
    suite.addTest(TestEHRWrapper('test_create_patient_record'))
    suite.addTest(TestEHRWrapper('test_patient_medical_record'))
    suite.addTest(TestEHRWrapper('test_create_patient_medical_record'))
    suite.addTest(TestEHRWrapper('test_get_patient_medical_record'))
    suite.addTest(TestEHRWrapper('test_delete_patient_medical_record'))
    suite.addTest(TestEHRWrapper('test_delete_patient_record'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())        