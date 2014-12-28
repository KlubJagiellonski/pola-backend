from api.models import Company, Product
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(Product, SimpleHistoryAdmin)