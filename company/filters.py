# -*- coding: utf-8 -*-

import django_filters
from .models import Company
from django.utils.translation import ugettext_lazy as _
from pola.filters import NoHelpTextFilterMixin, CrispyFilterMixin
from distutils.util import strtobool


class CompanyFilter(NoHelpTextFilterMixin,
                    CrispyFilterMixin,
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
