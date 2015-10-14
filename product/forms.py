from django import forms

from . import models
from pola.forms import (CommitDescriptionMixin,
                        FormHorizontalMixin, SaveButtonMixin,
                        ReadOnlyFieldsMixin)


class ProductForm(ReadOnlyFieldsMixin, SaveButtonMixin, FormHorizontalMixin,
                  CommitDescriptionMixin, forms.ModelForm):
    readonly_fields = ['code']

    class Meta:
        model = models.Product
        fields = ['name', 'code', 'company']
