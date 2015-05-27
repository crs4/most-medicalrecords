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
import requests
from urlparse import urljoin

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from most.web.medicalrecords.utils import make_new_uid
from most.web.authentication.decorators import oauth2_required
from most.web.medicalrecords.models import Patient

# Get an instance of a logger
logger = logging.getLogger('most.web.medicalrecord')

def make_url(endpoint):
	return urljoin(settings.PYEHR_DB_SERVICE_BASE_URL, endpoint)


def _get_ehr_uuid_from_patient_uuid(patient_uuid):

	try:
		patient = Patient.objects.get(uuid=patient_uuid)
		return patient.ehr_uuid
	except Patient.DoesNotExist:
		return None 
#	 	HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))


@oauth2_required	
def get_status(request):
	
	logger.info("returned status for %s" % settings.PYEHR_DB_SERVICE_BASE_URL)

	result = requests.get(make_url('/check/status/dbservice'))
	return HttpResponse(result.text)


def _get_ehr_patient(ehr_patient_id):

	raw_result = requests.get(make_url('/patient/{patient_id}'.format(patient_id=ehr_patient_id)), params={'fetch_ehr_records': False})
	result = json.loads(raw_result.text)
	return result


@oauth2_required	
def get_ehr_patient(request, patient_uuid):

	ehr_uuid = _get_ehr_uuid_from_patient_uuid(patient_uuid)

	if not ehr_uuid:
		return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	result = _get_ehr_patient(ehr_uuid)
	return HttpResponse(json.dumps(result))


@oauth2_required	
def get_ehr_record_for_patient(request, patient_uuid, record_uuid):
	
	logger.info('GET EHR RECORD: %s' % patient_uuid)

	ehr_uuid = _get_ehr_uuid_from_patient_uuid(patient_uuid)

	if not ehr_uuid:
		return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	result = requests.get(make_url('/ehr/{patient_id}/{ehr_record_id}'.format(patient_id=ehr_uuid, ehr_record_id=record_uuid)))
	return HttpResponse(result.text)


@csrf_exempt
@oauth2_required	
def create_ehr_patient(request, patient_uuid):

	#Retrieve medicalrecords patient
	try:
		patient = Patient.objects.get(uuid=patient_uuid)

	except Patient.DoesNotExist:
	 	return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	result = requests.put(make_url('/patient'), json={'patient_id':patient.ehr_uuid})

	if result.status_code == requests.codes.server_error:
		return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 502, 'message': 'ehr patient already exists'}}))
	else:
		return HttpResponse(result.text)


@csrf_exempt
@oauth2_required	
def create_ehr_record_for_patient(request, patient_uuid, record_uuid=None):

	logger.info('BODY:')
	logger.info(request.body)
	ehr_record=request.body

	try:
		patient = Patient.objects.get(uuid=patient_uuid)

	except Patient.DoesNotExist:
	 	return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	data = {
		'patient_id': patient.ehr_uuid,
		'ehr_record': ehr_record
	}

	if record_uuid:
		data['record_id'] = record_uuid

	logger.info("Try to send data to pyehr")
	logger.info(data)

	result = requests.put(make_url('/ehr'), json=data)
	return HttpResponse(result.text)


@oauth2_required
def delete_ehr_record_for_patient(request, patient_uuid, record_uuid):
	if 'delete_method' in request.REQUEST:
	 	delete_method = request.REQUEST['delete_method']
	else:
		delete_method = 'hide'

	try:
		patient = Patient.objects.get(uuid=patient_uuid)

	except Patient.DoesNotExist:
		return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	result = requests.delete(make_url('/ehr/{patient_id}/{ehr_record_id}/{delete_method}'.format(patient_id=patient.ehr_uuid, ehr_record_id=record_uuid, delete_method=delete_method)))
	return HttpResponse(result.text)


@oauth2_required	
def delete_ehr_patient(request, patient_uuid):
	if 'delete_method' in request.REQUEST:
	 	delete_method = request.REQUEST['delete_method']
	else:
		delete_method = 'hide'

	try:
		patient = Patient.objects.get(uuid=patient_uuid)

	except Patient.DoesNotExist:
		return HttpResponse(json.dumps({"success" : False, "errordata" : {'code' : 501, 'message': 'request patient does not exists'}}))

	result = requests.delete(make_url('/patient/{patient_id}/{delete_method}'.format(patient_id=patient.ehr_uuid, delete_method=delete_method)))
	return HttpResponse(result.text)
