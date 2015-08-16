from django import forms

from . import models
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit(
            'action', _('Save'), css_class="btn btn-primary"))

    class Meta:
        model = models.Company
        fields = ['nip', 'name', 'address',
                  'plCapital', 'plCapital_notes']
