import unittest
import requests
import json
import logging
import sys


class TestPatient(unittest.TestCase):

    def __init__(self, label):
        super(TestPatient, self).__init__(label)


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
        return data


    def _do_get_patient_by_id(self, patient_id):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/patients/{patient_id}/'.format(patient_id=patient_id), 
            params=payload
        )       
        print r.text
        data = json.loads(r.text)
        return data


    def test_create_patient(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        print 'PATIENTID: %s' % patient_id
        print '#################'
        print 'TEST CREATE PATIENT: %s' % create_data
        print '#################'
        self.assertTrue(create_data['success'])


    def test_get_patient(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        retrieve_data = self._do_get_patient_by_id(patient_id)
        print '#################'
        print 'TEST GET PATIENT: %s' % retrieve_data
        print '#################'
        self.assertTrue(retrieve_data['success'])


    def test_get_all_patients(self):

        payload = {'access_token': self.access_token}
        r = requests.get(
            'http://127.0.0.1:8000/medicalrecords/patients/', 
            params=payload
        )       
        print r.text
        data = json.loads(r.text)
        print '#################'
        print 'TEST GET ALL PATIENTS FOR TG: %s' % data
        print '#################'
        self.assertTrue(data['success'])
        

    def test_delete_patient(self):

        create_data = self._do_create_patient()
        patient_id = create_data['patient']['uuid']
        retrieve_data = self._do_get_patient_by_id(patient_id)

        payload = {'access_token': self.access_token}

        r = requests.delete(
            'http://127.0.0.1:8000/medicalrecords/patients/{patient_id}/'.format(patient_id=patient_id), 
            params=payload
        )
        delete_data = json.loads(r.text)

        print '#################'
        print 'TEST DELETE PATIENT: %s' % delete_data
        print '#################'
        self.assertTrue(delete_data['success'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestPatient('test_create_patient'))
    suite.addTest(TestPatient('test_get_patient'))
    suite.addTest(TestPatient('test_get_all_patients'))
    suite.addTest(TestPatient('test_delete_patient'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())          
        