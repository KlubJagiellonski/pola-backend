from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Product


class ProductAdmin(VersionAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )
    list_filter = ()
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
