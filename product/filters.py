# -*- coding: utf-8 -*-

import django_filters
from dal import autocomplete
from django import forms
from django.utils.translation import ugettext_lazy as _

from company.models import Company
from pola.filters import (CrispyFilterMixin)
from .models import Product


class NullProductFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def filter(self, qs, value):
        if value:
            return qs.filter(company=None)
        return qs


class ProductFilter(CrispyFilterMixin,
                    django_filters.FilterSet):
    company_empty = NullProductFilter(label="Tylko produkty bez producenta")

    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company:company-autocomplete'))

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
