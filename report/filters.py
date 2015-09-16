import django_filters
from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext_lazy as _


class StatusFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        super(StatusFilter, self).__init__(*args, **kwargs)
        self.extra['choices'] = (
            ('', '---------'),
            ('open', _('Open')),
            ('resolved', _('Resolved'))
        )

    def filter(self, qs, value):
        if value == 'open':
            return qs.only_open()
        if value == 'resolved':
            return qs.only_resolved()
        return qs


class ReportFilter(django_filters.FilterSet):
    status = StatusFilter()

    @property
    def form(self):
        self._form = super(ReportFilter, self).form
        self._form.helper = FormHelper(self._form)
        self._form.helper.form_class = 'form'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', 'Filter',
                                               css_class="btn-block"))
        return self._form

    class Meta:
        model = Report
        fields = [
            'status',
            'product',
            'client',
            'created_at',
            'resolved_at',
            'resolved_by']
