# -*- coding: utf-8 -*-

import django_filters
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _

from company.models import Company
from pola.filters import CrispyFilterMixin
from product.models import Product
from .models import Report


class StatusFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        super(StatusFilter, self).__init__(*args, **kwargs)
        self.extra['choices'] = (
            ('', '---------'),
            ('open', _('Otwarte')),
            ('resolved', _('Rozpatrzone'))
        )

    def filter(self, qs, value):
        if value == 'open':
            return qs.only_open()
        if value == 'resolved':
            return qs.only_resolved()
        return qs


class ReportFilter(CrispyFilterMixin,
                   django_filters.FilterSet):
    status = StatusFilter()
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='product:product-autocomplete'))
    product__company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company:company-autocomplete'))

    class Meta:
        model = Report
        fields = [
            'status',
            'product',
            'product__company',
            'client',
            'created_at',
            'resolved_at',
            'resolved_by']
        order_by = [
            ('created_at', _('Data utowrzenia')),
            ('-created_at', _('Data utworzenia (reversed)')),
            ('resolved_at', _('Data rozpatrzenia')),
            ('-resolved_at', _('Data rozpatrzenia (reversed)')),
            ('resolved_by', _(u'Rozpatrujący')),
            ('-resolved_by', _(u'Rozpatrujący (reversed)')),
        ]
