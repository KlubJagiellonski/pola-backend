from api.models import Company, Product
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

class CompanyAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'nip', 'capital_in_poland', 'created_date')
    search_fields = ['name', 'nip']
    list_filter = ['created_date', 'updated_date']

class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('barcode', 'name', 'made_in_poland', 'company', 'created_date')
    search_fields = ['name', 'barcode']
    list_filter = ['created_date', 'updated_date']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)