from django import forms

from . import models
from pola.forms import (AutocompleteChoiceField,
                        CommitDescriptionMixin,
                        FormHorizontalMixin,
                        ReadOnlyFieldsMixin,
                        SaveButtonMixin)


class ProductForm(ReadOnlyFieldsMixin, SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    company = AutocompleteChoiceField('CompanyAutocomplete')
    readonly_fields = ['code']

    class Meta:
        model = models.Product
        fields = ['name', 'code', 'company']
