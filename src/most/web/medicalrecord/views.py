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
import json

def ping(request):
	return HttpResponse("pong")
	
def get_patients(request):
	
	patients = Patient.objects.all()
	result = []
	for patient in patients:
		result.append(patient.to_json)
	return HttpResponse(json.dumps({"success" : True, "patients" : result}))