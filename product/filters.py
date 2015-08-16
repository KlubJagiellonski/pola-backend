# from django.utils.translation import ugettext_lazy as _
import django_filters
# from users.filters import UserChoiceFilter
from .models import Product
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
# class CrispyFilterMixin(object):
#     form_class = 'form-inline'


class NullProductFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def filter(self, qs, value):
        if value:
            return qs.filter(company=None)
        return qs


class ProductFilter(django_filters.FilterSet):
    @property
    def form(self):
        self._form = super(ProductFilter, self).form
        self._form.helper = FormHelper(self._form)
        self._form.helper.form_class = 'form'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', 'Filter',
                                               css_class="btn-block"))
        return self._form

    company_empty = NullProductFilter()

    class Meta:
        model = Product
        fields = ['name', 'code', 'company_empty', 'company']
        order_by = (
            ('name', _('Name')),
            ('-name', _('Name (reversed)')),
            ('code', _('Code')),
            ('-code', _('Code (reversed)')),
            ('id', _('ID')),
            ('-id', _('ID (reversed)')),
            ('company__name', _('Comapny\'s name')),
            ('-company__name', _('Comapny\'s name (reversed)')),
            ('query_count', _('Query count')),
            ('-query_count', _('Query count (reversed)')),
        )
