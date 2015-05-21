# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.conf.urls import patterns, include, url


# MostUser API related urls
urlpatterns = patterns('',
    (r'^ping/$', 'most.web.medicalrecord.views.ping'),
    (r'^ping/auth/$', 'most.web.medicalrecord.views.authenticated_ping'),
    (r'^patients/create/$', 'most.web.medicalrecord.views.create_patient'),
    (r'^patients/$', 'most.web.medicalrecord.views.get_patients'),

    (r'^ehr/(?P<ehr_id>\d+)/$', 'most.web.medicalrecord.views.get_patients'), #Get list of medical record
    (r'^ehr/create/$', 'most.web.medicalrecord.views.get_patients'), #Create new ehr record for patient
    (r'^ehr/(?P<ehr_id>\d+)/record/(?P<ehr_record_id>\d+)/$', 'most.web.medicalrecord.views.get_patients'), #Get specific record based on record_id

    (r'^demographic/(?P<demographic_id>\d+)/$', 'most.web.medicalrecord.views.get_patients'),

)