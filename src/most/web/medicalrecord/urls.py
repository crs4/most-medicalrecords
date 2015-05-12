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
    (r'^patients/create/$', 'most.web.medicalrecord.views.create_patient'),
    (r'^patients/$', 'most.web.medicalrecord.views.get_patients'),
)

