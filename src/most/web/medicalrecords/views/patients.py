# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from most.web.authentication.decorators import oauth2_required
from most.web.medicalrecords.consts import MISSING_PARAMETERS
from most.web.medicalrecords.models import Patient

# Get an instance of a logger
logger = logging.getLogger('most.web.medicalrecord')


@oauth2_required
def get_patients(request):
    patients = Patient.objects.filter(taskgroup=request.taskgroup)
    result = []
    for patient in patients:
        result.append(patient.json_dict)
    return HttpResponse(json.dumps({"success": True, "patients": result}))


@csrf_exempt
@oauth2_required
def create_patient(request):
    logger.info('In create_patient')
    patient = Patient()
    patient.taskgroup = request.taskgroup
    if 'ehr_uuid' in request.REQUEST:
        logger.info('In EHR_UUID')
        patient.ehr_uuid = request.REQUEST['ehr_uuid']
    if 'demographic_uuid' not in request.REQUEST:
        return HttpResponse(json.dumps({"success": False, "data":
                                        {"error": "missing demographic_uuid value",
                                         "code": MISSING_PARAMETERS}}))

    patient.demographic_uuid = request.REQUEST['demographic_uuid']

    patient.save()

    return HttpResponse(json.dumps({"success": True, "patient": patient.json_dict}))


@oauth2_required
def get_patient(request, patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': 501, 'message': 'request patient does not exists'}}))

    return HttpResponse(json.dumps({"success": True, "patient": patient.json_dict}))


@csrf_exempt
@oauth2_required
def update_patient(request, patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': 501, 'message': 'request patient does not exists'}}))

    if 'ehr_uuid' in request.REQUEST:
        logger.info('In EHR_UUID')
        patient.ehr_uuid = request.REQUEST['ehr_uuid']
    elif 'demographic_uuid' in request.REQUEST:
        patient.demographic_uuid = request.REQUEST['demographic_uuid']
    else:
        return HttpResponse(json.dumps({"success": False, "error": {'code': 502, 'message': 'no data'}}))

    patient.save()

    return HttpResponse(json.dumps({"success": True, "patient": patient.json_dict}))


@oauth2_required
def delete_patient(request, patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except Patient.DoesNotExist:
        return HttpResponse(
            json.dumps({"success": False, "errordata": {'code': 501, 'message': 'request patient does not exists'}}))
    data = patient.json_dict
    patient.delete()

    return HttpResponse(json.dumps({"success": True, "patient": data}))
