from django.utils.translation import ugettext_lazy as _


class CrispyFilterMixin(object):
    form_class = 'form'

    @property
    def form(self):
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit
        self._form = super(CrispyFilterMixin, self).form
        self._form.helper = FormHelper(self._form)
        if self.form_class:
            self._form.helper.form_class = 'form'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', _('Filtruj')))
        return self._form


class NoHelpTextFilterMixin(object):
    def __init__(self, *args, **kwargs):
        super(NoHelpTextFilterMixin, self).__init__(*args, **kwargs)
        for key in self.filters.iteritems():
            self.filters[key[0]].extra.update(
                {'help_text': ''}
            )
