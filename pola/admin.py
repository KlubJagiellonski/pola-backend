from django.contrib import admin

from .models import Query


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'timestamp')
    list_filter = ('client', 'timestamp')
