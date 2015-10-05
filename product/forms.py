from django import forms

from . import models
from pola.forms import SaveButtonMixin, FormHorizontalMixin


class ProductForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'code', 'company']
