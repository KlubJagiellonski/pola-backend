# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Product
import reversion


class ProductAdmin(reversion.VersionAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'company',
    )
    list_filter = ('company',)
    search_fields = ('name',)
admin.site.register(Product, ProductAdmin)
