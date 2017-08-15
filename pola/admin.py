# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Query


class QueryAdmin(admin.ModelAdmin):
    list_display = (u'id', 'client', 'timestamp')
    list_filter = ('client', 'timestamp')


admin.site.register(Query, QueryAdmin)
