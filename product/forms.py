import csv
from tempfile import NamedTemporaryFile
from typing import NamedTuple

from dal import autocomplete
from django import forms
from django.db import IntegrityError

from company.models import Company
from pola.forms import (
    CommitDescriptionMixin,
    FormHorizontalMixin,
    SaveButtonMixin,
)

from . import models
from .models import Product


class ProductForm(SaveButtonMixin, FormHorizontalMixin, CommitDescriptionMixin, forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['code', 'name', 'code', 'company']
        widgets = {'company': autocomplete.ModelSelect2(url='company:company-autocomplete')}


class AddBulkProductForm(SaveButtonMixin, FormHorizontalMixin, forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects, widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )
    rows = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self):
        company = self.cleaned_data['company']
        success = []
        failed = []
        with NamedTemporaryFile(mode='w+', newline='') as csvfile:
            csvfile.write(self.cleaned_data['rows'])
            csvfile.seek(0)
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, dialect=dialect)
            for row in reader:
                code = row.get('code')
                name = row.get('name')
                p = Product(code=code, name=name, company=company)
                try:
                    p.save(commit_desc="Bulk import")
                    success.append(p)
                except IntegrityError as ex:
                    failed.append(p)
        return success, failed
