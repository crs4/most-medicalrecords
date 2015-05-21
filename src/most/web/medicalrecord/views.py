# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.http import HttpResponse
from most.web.medicalrecord.models import Patient
from most.web.authentication.decorators import oauth2_required
from most.web.medicalrecord.models import Patient
from most.web.users.models import TaskGroup
import json
import logging

# Get an instance of a logger
logger = logging.getLogger('most.web.medicalrecord')

def ping(request):
	return HttpResponse("pong")

	
@oauth2_required	
def authenticated_ping(request):
	return HttpResponse("authenticated pong")


@oauth2_required	
def get_patients(request):
	
	patients = Patient.objects.filter(taskgroup=request.taskgroup)
	result = []
	for patient in patients:
		result.append(patient.json_dict)
	return HttpResponse(json.dumps({"success" : True, "patients" : result}))

@oauth2_required	
def create_patient(request):
	
	logger.info('In create_patient')
	patient = Patient()
	patient.taskgroup = request.taskgroup
	if 'ehr_uuid' in request.REQUEST:
		logger.info('In EHR_UUID')
		patient.ehr_uuid = request.REQUEST['ehr_uuid']
	if 'demographic_uuid' in request.REQUEST:
		patient.demographic_uuid = request.REQUEST['demographic_uuid']

	patient.save()

	return HttpResponse(json.dumps({"success" : True, "patient" : patient.json_dict}))