# -*- coding: utf-8 -*-
# MOST authenticated wrapper to pyehr dbservice service
#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

import json
import logging
from urlparse import urljoin

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from most.web.authentication.decorators import oauth2_required
from most.web.medicalrecords.consts import PATIENT_NOT_EXISTS
from most.web.medicalrecords.models import Patient
from most.web.medicalrecords.decorators import check_pyehr_conf

# Get an instance of a logger
logger = logging.getLogger('most.web.medicalrecord')


def _convert_pyehr_response(response):
    res = {}
    for k, v in response.iteritems():
        res[k.lower()] = v
    return json.dumps(res)


def make_url(base_url, endpoint):
    logger.error("BASE: " + base_url)
    logger.error("ENDPOINT: " + endpoint)
    logger.error("OVERALL: " + urljoin(base_url, endpoint))

    return urljoin(base_url, endpoint)


def _get_ehr_uuid_from_patient_uuid(patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
        return patient.ehr_uuid
    except Patient.DoesNotExist:
        return None


@oauth2_required
@check_pyehr_conf
def get_status(request, base_pyehr_url=None):
    logger.info("returned status for %s" % base_pyehr_url)
    logger.info("The server url is: %s" % make_url(base_pyehr_url, '/check/status/dbservice'))
    result = requests.get(make_url(base_pyehr_url, '/check/status/dbservice'))
    return HttpResponse(result.text)


def _get_ehr_patient(base_pyehr_url, ehr_patient_id):
    raw_result = requests.get(make_url(base_pyehr_url, '/patient/{patient_id}'.format(patient_id=ehr_patient_id)),
                              params={'fetch_ehr_records': False})
    result = raw_result.json()
    return _convert_pyehr_response(result)


@oauth2_required
@check_pyehr_conf
def get_ehr_patient(request, patient_uuid, base_pyehr_url=None):
    ehr_uuid = _get_ehr_uuid_from_patient_uuid(patient_uuid)

    if not ehr_uuid:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS, 'message': 'request patient does not exists'}}))
    result = _get_ehr_patient(base_pyehr_url, ehr_uuid)
    return HttpResponse(result)


@oauth2_required
@check_pyehr_conf
def get_ehr_record_for_patient(request, patient_uuid, record_uuid, base_pyehr_url=None):
    logger.info('GET EHR RECORD: %s' % patient_uuid)

    ehr_uuid = _get_ehr_uuid_from_patient_uuid(patient_uuid)

    if not ehr_uuid:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS,
                                                        'message': 'request patient does not exists'}}))

    result = requests.get(
        make_url(base_pyehr_url,
                 '/ehr/{patient_id}/{ehr_record_id}'.format(patient_id=ehr_uuid, ehr_record_id=record_uuid)))
    return HttpResponse(_convert_pyehr_response(result.json()))


@csrf_exempt
@oauth2_required
@check_pyehr_conf
def create_ehr_patient(request, patient_uuid, base_pyehr_url=None):
    # Retrieve medicalrecords patient
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS, 'message': 'request patient does not exists'}}))

    result = requests.put(make_url(base_pyehr_url, '/patient'), json={'patient_id': patient.ehr_uuid})

    if result.status_code == requests.codes.server_error:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': 502, 'message': 'ehr patient already exists'}}))
    else:
        return HttpResponse(_convert_pyehr_response(result.json()))


@csrf_exempt
@oauth2_required
@check_pyehr_conf
def create_ehr_record_for_patient(request, patient_uuid, base_pyehr_url=None, record_uuid=None):
    logger.info('BODY:')
    logger.info(request.body)
    ehr_record = request.body

    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS,
                                                        'message': 'request patient does not exists'}}))

    data = {
        'patient_id': patient.ehr_uuid,
        'ehr_record': ehr_record
    }

    if record_uuid:
        data['record_id'] = record_uuid

    logger.info("Try to send data to pyehr")
    logger.info(data)

    result = requests.put(make_url(base_pyehr_url, '/ehr'), json=data)
    return HttpResponse(_convert_pyehr_response(result.json()))


@oauth2_required
@check_pyehr_conf
def delete_ehr_record_for_patient(request, patient_uuid, record_uuid, base_pyehr_url=None):
    if 'delete_method' in request.REQUEST:
        delete_method = request.REQUEST['delete_method']
    else:
        delete_method = 'hide'

    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS, 'message': 'request patient does not exists'}}))

    result = requests.delete(make_url(base_pyehr_url,
                                      '/ehr/{patient_id}/{ehr_record_id}/{delete_method}'.
                                      format(patient_id=patient.ehr_uuid, ehr_record_id=record_uuid,
                                             delete_method=delete_method)))
    return HttpResponse(_convert_pyehr_response(result.json()))


@oauth2_required
@check_pyehr_conf
def delete_ehr_patient(request, patient_uuid, base_pyehr_url=None):
    if 'delete_method' in request.REQUEST:
        delete_method = request.REQUEST['delete_method']
    else:
        delete_method = 'hide'

    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': PATIENT_NOT_EXISTS, 'message': 'request patient does not exists'}}))

    result = requests.delete(make_url(base_pyehr_url,
                                      '/patient/{patient_id}/{delete_method}'.
                                      format(patient_id=patient.ehr_uuid, delete_method=delete_method)))
    return HttpResponse(_convert_pyehr_response(result.json()))
