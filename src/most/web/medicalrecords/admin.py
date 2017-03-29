# -*- coding: utf-8 -*-

#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.contrib import admin

from .models import Configuration


class ConfigurationAdmin(admin.ModelAdmin):

    class Meta:
        model = Configuration
        fields = ('ehr_service_address', 'ehr_service_port', )

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = Configuration.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(Configuration, ConfigurationAdmin)
