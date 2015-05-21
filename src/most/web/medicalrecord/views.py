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
import json


def ping(request):
	return HttpResponse("pong")

	
@oauth2_required	
def authenticated_ping(request):
	return HttpResponse("authenticated pong")


def get_patients(request):
	
	patients = Patient.objects.all()
	result = []
	for patient in patients:
		result.append(patient.to_json)
	return HttpResponse(json.dumps({"success" : True, "patients" : result}))

def create_patient(request):
	
	patient = Patient()
	patient.task_group = request.task_group
	if 'ehr_uuid' in request.REQUEST:
		patient.ehr_uuid = request.REQUEST['ehr_uuid']
	if 'demographic_uuid' in request.REQUEST:
		patient.demographic_uuid = request.REQUEST['demographic_uuid']

