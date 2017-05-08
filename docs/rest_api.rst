MedicalRecord REST API
======================

.. contents:: Table of Contents
    :depth: 3

Common Responses
----------------

Error reponses are the same for all the methods exposed by the REST API,
response has a `SUCCESS` field with value false and an `ERROR` field with a short
description of the occurred error. An example is the following:

.. sourcecode:: json

  {"success": false,
   "data": {
       "error": "<error_message>",
       "code": "<error_code>"
   }
  }

Error Codes
***********

The possible error codes are:

 * 101 - No token provided: the request misses an OAuth2 token
 * 102 - Token doesn"t exist: the OAauth2 token used for the request is not valid
 * 501 - Patient doesn"t exist: the id of the patient is not recognized by the system
 * 502 - Missing parameters: the request misses some required parameter

Patient
-------

.. http:post:: /patients/

    Create a patient with demographics and ehr id. If the the ehr id is not specified, the server creates it
    automatically. The demographic_uuid, on the other hand is mandatory and is the id of the patient in an external
    demographic service (e.g., `most-demographics <https://github.com/crs4/most-demographics>`_)

    :param access_token: the OAuth2 access token returned by the server after the authentication
    :param demographic_uuid: identification for demographics data. It should be an id related to a patient of an external
        demographic service
    :param ehr_uuid: identification for ehr data
    :resheader Content-Type: application/json

    **Example of correcy response**:

    .. sourcecode:: json

        {
            "success": true,
            "patient": {
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "nlpwv5wcqrqlqr2u3eiodo3qtjghnres"
            }
        }

.. http:get:: /patients/

    Get the patients related to a taskgroup. The taskgroup is associated with the OAuth2 access token which has to be
    sent in input.

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "patients": [{
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "nlpwv5wcqrqlqr2u3eiodo3qtjghnres"
            }]
        }

.. http:get:: /patients/(string:patient_uuid)/

    Get the patient with the specified patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "patient": {
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "nlpwv5wcqrqlqr2u3eiodo3qtjghnres"
            }
        }

.. http:put:: /patients/

    Update a patient with a new demographic id

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :query patient_uuid: the patient id of the patient to update
    :query demographic_uuid: the new demographic_uuid value
    :resheader Content-Type: application/json

    **Example of correct response**:

    .. sourcecode:: json

        {
            "success": true,
            "patient": {
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "new_demographic_id"
            }
        }

.. http:delete:: /patients/

    Delete a patient

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :query patient_uuid: the patient id of the patient to delete
    :resheader Content-Type: application/json

    **Example of correct response**:

    .. sourcecode:: json

        {
            "success": true,
            "patient": {
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "new_demographic_id"
            }
        }

Demographic
-----------

.. http:get:: /demographic/(string:demographic_uuid)/

    Get the patient with the specified demographic uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "patient": {
                "uuid": "drpp32jnmapx3roaf5j7k46saj2ynuba",
                "demographic_uuid": "nlpwv5wcqrqlqr2u3eiodo3qtjghnres"
            }
        }

EHR
---

.. http:get:: /ehr/(string:patient_uuid)/

    Return a the patient's ehr record for the patient identified by patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "record": {
            "record_id": "gnaiibv2pvca4pufllijbacaengt4i5k",
                "active": true,
                "ehr_records": [],
                "creation_time": 1493994347.727665,
                "last_update": 1493994347.727665
            }
        }

.. http:post:: /ehr/(string:patient_uuid)/

    Creates the ehr for the patient specified by patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "record": {"record_id": "gnaiibv2pvca4pufllijbacaengt4i5k",
                "active": true,
                "ehr_records": [],
                "creation_time": 1493994347.727665,
                "last_update": 1493994347.727665
            }
        }

.. http:delete:: /ehr/(string:patient_uuid)/

    Delete the ehr for the patient specified by patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :query delete_method: it can be "hide" (default) or "delete". In the first case the record is only deactivated in
        the second it is actually deleted
    :resheader Content-Type: application/json

    **Example of correct responses**:

    .. sourcecode:: json

        {
            "success": true,
            "record": {"record_id": "gnaiibv2pvca4pufllijbacaengt4i5k",
                "active": false,
                "ehr_records": [],
                "creation_time": 1493994347.727665,
                "last_update": 1493994347.727665
            }
        }



.. http:post:: /ehr/(string:patient_uuid)/records/

    Save a new ehr record to the ehr of the patient with id patient_uuid. The record id is created by the system.
    The data of the request must be a JSON encoded openEHR archetype.

    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json

    **Example of correct request data**:

    .. sourcecode:: json

        {
            "archetype_class": "openEHR.TEST-EVALUATION.v1",
            "archetype_details": {
                "at0001": "val1",
                "at0002": "val2"
            }
        }

    **Example of correct response**:

    .. sourcecode:: json

        {
            "record": {
                "ehr_data": {
                    "archetype_class": "openEHR.TEST-EVALUATION.v1",
                    "archetype_details": {
                        "at0001": "val1",
                        "at0002": "val2"
                    }
                },
                "creation_time": 1399905956.765149,
                "last_update": 1399905956.765149,
                "record_id": "9a30f6b6a36b49c6b16e249ef35445eb",
                "active": true,
                "version": 1,
            },
            "success": true
        }


.. http:post:: /ehr/(string:patient_uuid)/records/(string:record_uuid)/

    Same as the previous function but in this case the record_uuid is provided by the client.


.. http:get:: /ehr/(string:patient_uuid)/records/(string:record_uuid)/

    Return the ehr record identified by record_uuid from the ehr of patient specified by patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct response**:

    .. sourcecode:: json

        {
            "record": {
                "ehr_data": {
                    "archetype_class": "openEHR.TEST-EVALUATION.v1",
                    "archetype_details": {
                        "at0001": "val1",
                        "at0002": "val2"
                    }
                },
                "creation_time": 1399905956.765149,
                "last_update": 1399905956.765149,
                "record_id": "9a30f6b6a36b49c6b16e249ef35445eb",
                "active": true,
                "version": 1,
            },
            "success": true
        }

.. http:delete:: /ehr/(string:patient_uuid)/records/(string:record_uuid)/

    Delete the ehr record identified by record_uuid from the ehr of patient specified by patient_uuid

    :query access_token: the OAuth2 access token returned by the server after the authentication
    :resheader Content-Type: application/json

    **Example of correct response**:

    .. sourcecode:: json

        {
            "message": "EHR record with ID cf629c7c51b740fb9776f8c4cc51f293 successfully hidden",
            "success": true
        }