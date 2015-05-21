MedicalRecord REST API
=====================

.. contents:: Table of Contents
   :depth: 3

Common Responses
----------------


Error reponses are the same for all the methods exposed by the REST API,
response has a `SUCCESS` field with value false and an `ERROR` field with a short
description of the occurred error. An example is the following:

.. sourcecode:: json

   {
     "SUCCESS": false,
     "ERROR": "Missing mandatory field, can't continue with the request"
   }
Patient
-------
.. http:get:: /patients/create

  Create users with demographics and ehr id.

  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

      {
        "success": true,
        "patient_data": 
        {
          "patient_id": 12345
        }
      }
      
  :query demographics_id: identification for demographics data
  :query ehr_id: identification for ehr data

.. http:get:: /patients/

   Retrieve patients for task_group specified

  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

      {
        "success": true,
        "patients_data": 
        [
          {"patient_id": 11111},
          {"patient_id": 22222},
          {"patient_id": 33333},
          {"patient_id": 44444},
          {"patient_id": 55555},
        ]
      }
      
  :query taskgroup_uuid: current taskgroup

.. http:get:: /patients/(string:patient_uuid)/

   Return data of selected patient

  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

      {
        "success": true,
        "patient_data": 
        [
          {"ehr_id": 11111},
          {"demographic_id": 22222}
        ]
      }
      
  :query taskgroup_uuid: current taskgroup   

EHR 
-------------

.. http:get:: /ehr/(string:patient_ehr_uuid)/

  Return a list of patient ehr record

.. http:get:: /ehr/(string:patient_ehr_uuid)/(string:record_uuid)/

  Return a specific patient ehr record by uuid


Demographic
-----------

.. http:get:: /demographic/(string:patient_demographic_uuid)/

  Return the patient demographic record
