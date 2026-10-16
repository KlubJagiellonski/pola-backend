from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Brand, Company


@admin.register(Company)
class CompanyAdmin(VersionAdmin):
    list_display = (
        'id',
        'nip',
        'name',
        'address',
        'plCapital',
        'plCapital_notes',
        'high_tax',
    )
    search_fields = ('name',)
    readonly_fields = ('high_tax',)


admin.site.register(Brand, admin.ModelAdmin)
