# from django.utils.translation import ugettext_lazy as _
import django_filters
# from users.filters import UserChoiceFilter
from .models import Product
from django import forms
from django.utils.translation import ugettext_lazy as _
from pola.filters import (AutocompleteChoiceFilter,
                          CrispyFilterMixin,
                          NoHelpTextFilterMixin)


class NullProductFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def filter(self, qs, value):
        if value:
            return qs.filter(company=None)
        return qs


class ProductFilter(NoHelpTextFilterMixin,
                    CrispyFilterMixin,
                    django_filters.FilterSet):
    company_empty = NullProductFilter()
    company = AutocompleteChoiceFilter(
        autocomplete_name="CompanyAutocomplete")

    class Meta:
        model = Product
        fields = ['name', 'code', 'company_empty', 'company']
        order_by = (
            ('name', _('Name')),
            ('-name', _('Name (reversed)')),
            ('code', _('Code')),
            ('-code', _('Code (reversed)')),
            ('id', _('ID')),
            ('-id', _('ID (reversed)')),
            ('company__name', _('Comapny\'s name')),
            ('-company__name', _('Comapny\'s name (reversed)')),
            ('query_count', _('Query count')),
            ('-query_count', _('Query count (reversed)')),
        )
