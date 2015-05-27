#test.py
# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.http import HttpResponse
from most.web.authentication.decorators import oauth2_required
import logging

# Get an instance of a logger
logger = logging.getLogger('most.web.medicalrecord')

def ping(request):
	return HttpResponse("pong")

	
@oauth2_required	
def authenticated_ping(request):
	return HttpResponse("authenticated pong")

