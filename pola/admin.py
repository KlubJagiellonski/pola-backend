# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Report, Query


class ReportAdmin(admin.ModelAdmin):
    list_display = (u'id', 'product', 'client', 'desciption')
    list_filter = ('product', 'client')
admin.site.register(Report, ReportAdmin)


class QueryAdmin(admin.ModelAdmin):
    list_display = (u'id', 'client', 'timestamp')
    list_filter = ('client', 'timestamp')
admin.site.register(Query, QueryAdmin)
