# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Client, Report, Query


class ClientAdmin(admin.ModelAdmin):
    list_display = (u'id',)
admin.site.register(Client, ClientAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = (u'id', 'barcode', 'client', 'desciption')
    list_filter = ('barcode', 'client')
admin.site.register(Report, ReportAdmin)


class QueryAdmin(admin.ModelAdmin):
    list_display = (u'id', 'client', 'timestamp')
    list_filter = ('client', 'timestamp')
admin.site.register(Query, QueryAdmin)
