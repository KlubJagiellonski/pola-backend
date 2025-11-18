from distutils.util import strtobool

import django_filters
from dal import autocomplete
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from pola.filters import CrispyFilterMixin

from .models import Brand, Company


class CompanyFilter(CrispyFilterMixin, django_filters.FilterSet):
    verified = django_filters.TypedChoiceFilter(
        choices=((None, _("----")), (True, _("Tak")), (False, _("Nie"))),
        coerce=strtobool,
        label=_("Dane zweryfikowane"),
    )

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', _('Nazwa (A-Z)')),
            ('query_count', _('Liczba zapytań')),
            ('modified', _('Data modyfikacji')),
            ('created', _('Data utworzenia')),
        )
    )

    class Meta:
        model = Company
        fields = {
            'nip': ['icontains'],
            'name': ['icontains'],
            'official_name': ['icontains'],
            'common_name': ['icontains'],
            'Editor_notes': ['icontains'],
        }


class BrandFilter(CrispyFilterMixin, django_filters.FilterSet):
    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(), widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', _('Nazwa (A-Z)')),
            ('modified', _('Data modyfikacji (rosnąco)')),
            ('created', _('Data utworzenia (rosnąco)')),
        )
    )

    class Meta:
        model = Brand
        fields = {}


class CompanyMergeFilter(CrispyFilterMixin, django_filters.FilterSet):
    q = django_filters.CharFilter(label=_("Nazwa"), method='filter_q')

    def filter_q(self, queryset, name, value):
        if not value:
            return queryset
        # Search across name, official_name, and common_name and ensure unique results
        return queryset.filter(
            Q(name__icontains=value) | Q(official_name__icontains=value) | Q(common_name__icontains=value)
        ).distinct()

    class Meta:
        model = Company
        fields = []
