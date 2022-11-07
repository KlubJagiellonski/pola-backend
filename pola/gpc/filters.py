import django_filters
from django.utils.translation import gettext_lazy as _

from pola.filters import CrispyFilterMixin

from . import models


class GPCBrickFilter(CrispyFilterMixin, django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('text', _('Nazwa (A-Z)')),)
    )

    class Meta:
        model = models.GPCBrick
        fields = {
            'text': ['icontains'],
            'code': ['icontains', 'istartswith'],
        }


class GPCClassFilter(CrispyFilterMixin, django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('text', _('Nazwa (A-Z)')),)
    )

    class Meta:
        model = models.GPCClass
        fields = {
            'text': ['icontains'],
            'code': ['icontains', 'istartswith'],
        }


class GPCFamilyFilter(CrispyFilterMixin, django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('text', _('Nazwa (A-Z)')),)
    )

    class Meta:
        model = models.GPCFamily
        fields = {
            'text': ['icontains'],
            'code': ['icontains', 'istartswith'],
        }


class GPCSegmentFilter(CrispyFilterMixin, django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('text', _('Nazwa (A-Z)')),)
    )

    class Meta:
        model = models.GPCFamily
        fields = {
            'text': ['icontains'],
            'code': ['icontains', 'istartswith'],
        }
