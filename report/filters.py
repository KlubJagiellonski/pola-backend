import django_filters
from .models import Report
from django.utils.translation import ugettext_lazy as _
from pola.filters import CrispyFilterMixin


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


class ReportFilter(CrispyFilterMixin, django_filters.FilterSet):
    status = StatusFilter()

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
            ('product', 'Product'),
            ('-product', 'Product (reversed)'),
            ('client', 'Client'),
            ('-client', 'Client (reversed)'),
            ('created_at', 'Created at'),
            ('-created_at', 'Created at (reversed)'),
            ('resolved_at', 'Resolved at'),
            ('-resolved_at', 'Resolved at (reversed)'),
            ('resolved_by', 'Resolved by'),
            ('-resolved_by', 'Resolved by (reversed)'),
        ]
