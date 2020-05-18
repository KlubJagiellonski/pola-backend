from django.contrib import admin

from .models import Query


class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'timestamp')
    list_filter = ('client', 'timestamp')


admin.site.register(Query, QueryAdmin)
