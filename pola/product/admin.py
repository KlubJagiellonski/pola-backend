from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )
    list_filter = ('company',)
    search_fields = ('name',)

    def get_search_results(self, request, queryset, search_term):
        queryset, _ = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.search(search_term)

        return queryset, _
