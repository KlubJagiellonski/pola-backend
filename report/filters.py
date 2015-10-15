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
            ('open', _('Open')),
            ('resolved', _('Resolved'))
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

    class Meta:
        model = Report
        fields = [
            'status',
            'product',
            'client',
            'created_at',
            'resolved_at',
            'resolved_by']
        order_by = [
            ('product', _('Product')),
            ('-product', _('Product (reversed)')),
            ('client', _('Client')),
            ('-client', _('Client (reversed)')),
            ('created_at', _('Created at')),
            ('-created_at', _('Created at (reversed)')),
            ('resolved_at', _('Resolved at')),
            ('-resolved_at', _('Resolved at (reversed)')),
            ('resolved_by', _('Resolved by')),
            ('-resolved_by', _('Resolved by (reversed)')),
        ]
