# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.db import models
from most.web.users.models import TaskGroup
from most.web.utils import pkgen


class Patient(models.Model):

    uuid = models.CharField(max_length=40, unique=True, default=pkgen)
    taskgroup = models.ForeignKey(TaskGroup, related_name="patients")
    demographic_uuid = models.CharField(max_length=40, unique=False, default=pkgen)
    ehr_uuid = models.CharField(max_length=40, unique=False, default=pkgen)

    def __unicode__(self):
        return '[Patient: {uuid}]'.format(uuid=self.uuid)

    def _get_json_dict(self):
        return {
            'uuid': self.uuid,
            'demographic_uuid': self.demographic_uuid,
            'ehr_uuid': self.ehr_uuid,
        }

    json_dict = property(_get_json_dict)

    def _get_full_json_dict(self):
        result = self.json_dict
        result.update({
        })
        return result

    full_json_dict = property(_get_full_json_dict)


class Configuration(models.Model):

    ehr_service_address = models.CharField(max_length=30, unique=True, blank=False)
    ehr_service_port = models.CharField(max_length=5, blank=False, default=8080)
