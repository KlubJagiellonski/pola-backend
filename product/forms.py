from dal import autocomplete
from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin,
                        ReadOnlyFieldsMixin,
                        SaveButtonMixin)


class ProductForm(ReadOnlyFieldsMixin, SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    readonly_fields = ['code']

    class Meta:
        model = models.Product
        fields = ['name', 'code', 'company']
        widgets = {
            'company': autocomplete.ModelSelect2(url='company:company-autocomplete')
        }
