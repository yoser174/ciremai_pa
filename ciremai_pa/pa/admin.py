# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Doctors


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','ext_code',)
    search_fields = ['name','ext_code',]


# Register your models here.
admin.site.register(Doctors,DoctorAdmin)
