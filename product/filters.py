# -*- coding: utf-8 -*-

import django_filters
from .models import Product
from django import forms
from django.utils.translation import ugettext_lazy as _
from pola.filters import (AutocompleteChoiceFilter,
                          CrispyFilterMixin,
                          NoHelpTextFilterMixin)


class NullFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def __init__(self, null_field, *args, **kwargs):
        self.null_field = null_field
        super(NullFilter, self).__init__(field, *args, **kwargs)

    def filter(self, qs, value):
        if value:
            return qs.filter(**{self.null_field: None})
        return qs


class ProductFilter(NoHelpTextFilterMixin,
                    CrispyFilterMixin,
                    django_filters.FilterSet):
    company_empty = NullFilter(null_field='company', label="Tylko produkty bez producenta")
    company = AutocompleteChoiceFilter(
        autocomplete_name="CompanyAutocomplete")

    class Meta:
        model = Product
        fields = ['name', 'code', 'company_empty', 'company']
        order_by = (
            ('name', _('Nazwa (A-Z)')),
            ('-name', _('Nazawa (Z-A)')),
            ('company__name', _('Nazwa producenta (A-Z)')),
            ('-company__name', _('Nazwa producenta (Z-A)')),
            ('query_count', _(u'Liczba zeskanowań (rosnąco)')),
            ('-query_count', _(u'Liczba zeskanowań (malejąco)')),
        )
