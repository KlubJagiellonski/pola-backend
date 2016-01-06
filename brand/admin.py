# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Brand


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'company',
    )
    list_filter = ('company',)
admin.site.register(Brand, ReportAdmin)
