from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin, SaveButtonMixin)


class CompanyForm(SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ['nip', 'name', 'address',
                  'plCapital', 'plCapital_notes']
