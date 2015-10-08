from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin, SaveButtonMixin)


class CompanyForm(SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    class Meta:
        model = models.Company
        fields = [
            'nip',
            'name',
            'official_name',
            'address',
            'plCapital',
            'plCapital_notes',
            'plTaxes',
            'plTaxes_notes',
            'plRnD',
            'plRnD_notes',
            'plWorkers',
            'plWorkers_notes',
            'plBrand',
            'plBrand_notes',
            'verified',
        ]
