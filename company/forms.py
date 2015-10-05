from django import forms

from . import models
from pola.forms import SaveButtonMixin, FormHorizontalMixin


class CompanyForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ['nip', 'name', 'address',
                  'plCapital', 'plCapital_notes']
