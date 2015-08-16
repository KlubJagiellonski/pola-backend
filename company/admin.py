# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Company
import reversion


class CompanyAdmin(reversion.VersionAdmin):
    list_display = (
        u'id',
        'nip',
        'name',
        'address',
        'plCapital',
        'plCapital_notes',
    )
    search_fields = ('name',)
admin.site.register(Company, CompanyAdmin)
