from distutils.util import strtobool

import django_filters
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _

from pola.filters import CrispyFilterMixin

from .models import Brand, CapitalGroup, Company


class CompanyFilter(CrispyFilterMixin, django_filters.FilterSet):

    verified = django_filters.TypedChoiceFilter(
        choices=((None, _("----")), (True, _("Tak")), (False, _("Nie"))),
        coerce=strtobool,
        label=_("Dane zweryfikowane"),
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
        order_by = (
            ('name', _('Nazwa (A-Z)')),
            ('-name', _('Nazwa (Z-A)')),
            ('query_count', _('Liczba zapytań (rosnąco)')),
            ('-query_count', _('Liczba zapytań (malejąco)')),
        )


class BrandFilter(CrispyFilterMixin, django_filters.FilterSet):
    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(), widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )

    class Meta:
        model = Brand
        fields = {}
        order_by = ()


class CapitalGroupFilter(CrispyFilterMixin, django_filters.FilterSet):
    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(), widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )

    class Meta:
        model = CapitalGroup
        fields = {
            'nip': ['icontains'],
            'name': ['icontains'],
            'official_name': ['icontains'],
            'common_name': ['icontains'],
            'Editor_notes': ['icontains'],
        }
        order_by = (
            ('name', _('Nazwa (A-Z)')),
            ('-name', _('Nazwa (Z-A)')),
            ('query_count', _('Liczba zapytań (rosnąco)')),
            ('-query_count', _('Liczba zapytań (malejąco)')),
        )
