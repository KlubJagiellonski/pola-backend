import django_filters
from .models import Company
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext_lazy as _


class CompanyFilter(django_filters.FilterSet):

    @property
    def form(self):
        self._form = super(CompanyFilter, self).form
        self._form.helper = FormHelper(self._form)
        self._form.helper.form_class = 'form'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', 'Filter',
                                               css_class="btn-block"))
        return self._form

    plCapital = django_filters.RangeFilter()

    class Meta:
        model = Company
        fields = {
            'nip': ['icontains'],
            'name': ['icontains'],
            'address': ['icontains'],
            'plCapital': []}
