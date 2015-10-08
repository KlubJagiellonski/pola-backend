import django_filters
from .models import Company
from django.utils.translation import ugettext_lazy as _
from pola.filters import CrispyFilterMixin


class CompanyFilter(CrispyFilterMixin, django_filters.FilterSet):

    plCapital = django_filters.RangeFilter()

    class Meta:
        model = Company
        fields = {
            'nip': ['icontains'],
            'name': ['icontains'],
            'address': ['icontains'],
            'plCapital': []}
        order_by = (
            ('nip', _('NIP')),
            ('-nip', _('NIP (reversed)')),
            ('name', _('name')),
            ('-name', _('name (reversed)')),
            ('plCapital', _('plCapital')),
            ('-plCapital', _('plCapital  (reversed)')),
            ('query_count', _('query_count')),
            ('-query_count', _('query_count (reversed)')),
        )
