from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'ingredients',
    )
    list_filter = ('company',)
    search_fields = ('name',)
