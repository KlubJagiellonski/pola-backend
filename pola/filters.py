from django.utils.translation import ugettext_lazy as _


class CrispyFilterMixin:
    form_class = 'form'

    @property
    def form(self):
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit

        self._form = super().form
        self._form.helper = FormHelper(self._form)
        if self.form_class:
            self._form.helper.form_class = 'form'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', _('Filtruj')))
        return self._form
