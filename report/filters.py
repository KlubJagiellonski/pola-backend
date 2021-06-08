import django_filters
from dal import autocomplete
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from company.models import Company
from pola.filters import CrispyFilterMixin
from product.models import Product

from .models import Report


class StatusFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        if 'label' not in kwargs:
            kwargs['label'] = _('Status')
        super().__init__(*args, **kwargs)
        self.extra['choices'] = (('', '---------'), ('open', _('Otwarte')), ('resolved', _('Rozpatrzone')))

    def filter(self, qs, value):
        if value == 'open':
            return qs.only_open()
        if value == 'resolved':
            return qs.only_resolved()
        return qs


def is_bot_client(queryset, name, value):
    if value:
        return queryset.filter(client='krs-bot')
    else:
        return queryset.filter(~Q(client='krs-bot'))


class ReportFilter(CrispyFilterMixin, django_filters.FilterSet):
    status = StatusFilter()
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(), widget=autocomplete.ModelSelect2(url='product:product-autocomplete')
    )
    product__company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(), widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )
    is_bot_client = django_filters.BooleanFilter(
        field_name='client', method=is_bot_client, label='Pokaż zgłoszenia od bota'
    )

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created_at', _('Data utowrzenia')),
            ('resolved_at', _('Data rozpatrzenia')),
            ('resolved_by', _('Rozpatrujący')),
        )
    )

    class Meta:
        model = Report
        fields = [
            'status',
            'product',
            'product__company',
            'client',
            'created_at',
            'resolved_at',
            'resolved_by',
        ]
