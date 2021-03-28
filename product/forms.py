import csv
from tempfile import NamedTemporaryFile
from typing import Dict

from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
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
        fields = ['code', 'name', 'code', 'company', 'brand']
        widgets = {
            'company': autocomplete.ModelSelect2(url='company:company-autocomplete'),
            'brand': autocomplete.ModelSelect2(url='company:brand-autocomplete'),
        }


class AddBulkProductForm(SaveButtonMixin, FormHorizontalMixin, forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects, widget=autocomplete.ModelSelect2(url='company:company-autocomplete')
    )
    rows = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'name\\tcode\\nMleko\\t590...\\nMasło\\t590...'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_rows(self):
        try:
            with NamedTemporaryFile(mode='w+', newline='') as csvfile:
                csvfile.write(self.data['rows'])
                csvfile.seek(0)
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.DictReader(csvfile, dialect=dialect)
                if set(reader.fieldnames) != {'code', 'name'}:
                    raise ValidationError(
                        f'Następujące kolumny są wymagane: code, name. Aktualne kolumny: {reader.fieldnames}',
                        code='invalid',
                    )
                errors = []
                result = []
                for row in reader:
                    if 'code' not in row or 'name' not in row:
                        errors.append(
                            ValidationError(
                                f"Nieprawidlowe wiersz - Linia {reader.line_num} - Brakujace kolumny: {dict(row)}"
                            )
                        )
                    elif not row['code'].strip() or not row['name'].strip():
                        errors.append(
                            ValidationError(
                                f"Nieprawidlowe wiersz - Linia {reader.line_num} - Puste kolumny: {dict(row)}"
                            )
                        )
                    elif not row['code'].strip().isdigit():
                        errors.append(
                            ValidationError(
                                f"Nieprawidlowe wiersz - Linia {reader.line_num} - "
                                f"Kod musi zawierać tylko cyfry: {dict(row)}"
                            )
                        )

                    else:
                        code = row['code'].strip()
                        name = row['name'].strip()
                        result.append({'code': code, 'name': name})
                if errors:
                    raise ValidationError(errors)
                return result
        except csv.Error as ex:
            raise ValidationError(f"Blad odczytu pliku CSV: {ex}")

    def save(self):
        company = self.cleaned_data['company']
        success = []
        failed = []
        row: Dict[str, str]
        product_by_code = {
            p.code: p for p in Product.objects.filter(code__in=[row['code'] for row in self.cleaned_data['rows']])
        }
        for row in self.cleaned_data['rows']:
            code = row['code']
            name = row['name']
            p = product_by_code.get(code)
            changed = False
            if p is None:
                p = Product(code=code, name=name, company=company)
                changed = True
            else:
                if p.company is None:
                    p.company = company
                    changed = True
                if not p.name:
                    p.name = row['name']
                    changed = True
            if not changed:
                failed.append(p)
                continue
            try:
                p.save(commit_desc="Bulk import")
                success.append(p)
            except IntegrityError:
                failed.append(p)
        return success, failed
