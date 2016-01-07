# -*- coding: utf-8 -*-

import django_filters
from .models import Report
from django.utils.translation import ugettext_lazy as _
from pola.filters import (AutocompleteChoiceFilter,
                          CrispyFilterMixin,
                          NoHelpTextFilterMixin)


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


class ReportFilter(NoHelpTextFilterMixin,
                   CrispyFilterMixin,
                   django_filters.FilterSet):
    status = StatusFilter()
    product = AutocompleteChoiceFilter(
        autocomplete_name="ProductAutocomplete")
    product__company = AutocompleteChoiceFilter(
        autocomplete_name="CompanyAutocomplete")

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
