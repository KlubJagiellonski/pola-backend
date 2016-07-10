# -*- coding: utf-8 -*-

import django_filters
from .models import Brand
from pola.filters import NoHelpTextFilterMixin, CrispyFilterMixin


class BrandFilter(NoHelpTextFilterMixin,
                  CrispyFilterMixin,
                  django_filters.FilterSet):

    class Meta:
        model = Brand
