# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from reroute import patterns
from reroute.verbs import verb_url


# MostUser API related urls
urlpatterns = patterns('most.web.medicalrecords.views.simple',
                       (r'^ping/$', 'ping'),
                       (r'^ping/auth/$', 'authenticated_ping')
                       )

urlpatterns += patterns('most.web.medicalrecords.views.patients',
                        verb_url('POST', r'^patients/$', 'create_patient'),
                        verb_url('GET', r'^patients/$', 'get_patients'),
                        verb_url('PUT', r'^patients/(?P<patient_uuid>.*)/$', 'update_patient'),
                        verb_url('GET', r'^patients/(?P<patient_uuid>.*)/$', 'get_patient'),
                        verb_url('DELETE', r'^patients/(?P<patient_uuid>.*)/$', 'delete_patient'),
                        )

urlpatterns += patterns('most.web.medicalrecords.views.ehr',
                        (r'^ehr/status/$', 'get_status'),  # Get Status of pyehr dbservice service

                        verb_url('GET', r'^ehr/(?P<patient_uuid>.*)/records/(?P<record_uuid>.*)/$',
                                 'get_ehr_record_for_patient'), #
                        verb_url('POST', r'^ehr/(?P<patient_uuid>.*)/records/(?P<record_uuid>.*)/$',
                                 'create_ehr_record_for_patient'),
                        verb_url('POST', r'^ehr/(?P<patient_uuid>.*)/records/$', 'create_ehr_record_for_patient'),
                        verb_url('DELETE', r'^ehr/(?P<patient_uuid>.*)/records/(?P<record_uuid>.*)/$',
                                 'delete_ehr_record_for_patient'),

                        verb_url('POST', r'^ehr/(?P<patient_uuid>.*)/$', 'create_ehr_patient'), #
                        verb_url('GET', r'^ehr/(?P<patient_uuid>.*)/$', 'get_ehr_patient'), #
                        verb_url('DELETE', r'^ehr/(?P<patient_uuid>.*)/$', 'delete_ehr_patient'), #
                        )

urlpatterns += patterns('most.web.medicalrecords.views.patients',
                        (r'^demographic/(?P<demographic_uuid>.*)/$', 'get_patient_by_demographic'),
                        )
