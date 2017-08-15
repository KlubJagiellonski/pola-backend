# -*- coding: utf-8 -*-

from distutils.util import strtobool

import django_filters
from django.utils.translation import ugettext_lazy as _

from pola.filters import CrispyFilterMixin
from .models import Company


class CompanyFilter(CrispyFilterMixin,
                    django_filters.FilterSet):

    verified = django_filters.TypedChoiceFilter(
        choices=((None, _("----")), (True, _("Tak")), (False, _("Nie"))),
        coerce=strtobool,
        label=_(u"Dane zweryfikowane"))

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
            ('query_count', _(u'Liczba zapytań (rosnąco)')),
            ('-query_count', _(u'Liczba zapytań (malejąco)')),
        )
