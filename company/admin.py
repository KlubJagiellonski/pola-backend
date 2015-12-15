# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Company
from brand.models import Brand
import reversion


class BrandInline(admin.TabularInline):
    model = Brand


class CompanyAdmin(reversion.VersionAdmin):
    list_display = (
        u'id',
        'nip',
        'name',
        'address',
        'plCapital',
        'plCapital_notes',
    )
    inlines = [
        BrandInline
    ]
    search_fields = ('name',)
admin.site.register(Company, CompanyAdmin)
