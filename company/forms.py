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
            'name',
            'official_name',
            'common_name',
            'plCapital',
            'plWorkers',
            'plRnD',
            'plRegistered',
            'plNotGlobEnt',
            'description',
            'sources',
            'verified',
            'plCapital_notes',
            'plWorkers_notes',
            'plRnD_notes',
            'plRegistered_notes',
            'plNotGlobEnt_notes',
            'Editor_notes',
            'nip',
            'address',
        ]
