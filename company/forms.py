from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin, SaveButtonMixin,
                        ReadOnlyFieldsMixin)


class CompanyForm(ReadOnlyFieldsMixin, SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    readonly_fields = [
        'name'
        ]

    class Meta:
        model = models.Company
        fields = [
            'nip',
            'name',
            'official_name',
            'common_name',
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
