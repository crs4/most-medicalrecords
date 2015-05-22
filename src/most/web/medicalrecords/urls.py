# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from reroute import handler404, handler500, patterns, url, include
from reroute.verbs import verb_url

# MostUser API related urls
urlpatterns = patterns('',
    (r'^ping/$', 'most.web.medicalrecords.views.ping'),
    (r'^ping/auth/$', 'most.web.medicalrecords.views.authenticated_ping')
)


urlpatterns += patterns('most.web.medicalrecords.views',
    verb_url('POST', r'^patients/$', 'create_patient'),
    verb_url('GET',  r'^patients/$', 'get_patients'),
    verb_url('PUT',  r'^patients/(?P<patient_uuid>.*)/$', 'update_patient'),
    verb_url('GET',  r'^patients/(?P<patient_uuid>.*)/$', 'get_patient'),
    verb_url('DELETE',  r'^patients/(?P<patient_uuid>.*)/$', 'delete_patient'),
)

urlpatterns += patterns('most.web.medicalrecords.views',
    (r'^ehr/(?P<ehr_id>\d+)/$', 'most.web.medicalrecords.views.get_patients'), #Get list of medical record
    (r'^ehr/create/$', 'most.web.medicalrecords.views.get_patients'), #Create new ehr record for patient
    (r'^ehr/(?P<ehr_id>\d+)/record/(?P<ehr_record_id>\d+)/$', 'most.web.medicalrecords.views.get_patients'), #Get specific record based on record_id
)

urlpatterns += patterns('most.web.medicalrecords.views',
    (r'^demographic/(?P<demographic_id>\d+)/$', 'get_patients'),

)