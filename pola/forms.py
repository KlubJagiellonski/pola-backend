import reversion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Reset, Submit
from django import forms
from django.utils.translation import ugettext as _


class HelperMixin:
    form_helper_cls = FormHelper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = getattr(self, 'helper', self.form_helper_cls(self))


class SingleButtonMixin(HelperMixin):
    form_helper_cls = FormHelper

    @property
    def action_text(self):
        return _('Zapisz') if (hasattr(self, 'instance') and self.instance.pk) else _('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Submit('action', self.action_text, css_class="btn-primary"))


class SaveButtonMixin(SingleButtonMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Reset('reset', _('Przywróć poprzednie')))


class FormHorizontalMixin(HelperMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'


class CommitDescriptionMixin(forms.Form):
    commit_desc = forms.CharField(label=_('Opis zmiany'), widget=forms.Textarea)

    def save(self, *args, **kwargs):
        with reversion.create_revision(atomic=True):
            obj = super().save(*args, **kwargs)
            commit_desc = self.cleaned_data['commit_desc']
            reversion.set_comment(commit_desc)
            return obj


class ReadOnlyFieldsMixin:
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.items() if name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super().clean()
        for field in self.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data
