from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin, SaveButtonMixin,
                        ReadOnlyFieldsMixin)


class CompanyForm(ReadOnlyFieldsMixin, SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    brands = forms.CharField(required=False)

    readonly_fields = [
        'name'
        ]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['brands'].initial = self.instance.get_brands()

    def save(self, *args, **kwargs):
        self.instance.set_brands(self.cleaned_data['brands'])
        return super(CompanyForm, self).save(self, *args, **kwargs)

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
