#!/usr/bin/python
from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.forms import inlineformset_factory

from pola.forms import (
    CommitDescriptionMixin,
    FormHorizontalMixin,
    ReadOnlyFieldsMixin,
    SaveButtonMixin,
    SingleButtonMixin,
)

from . import models


class CompanyForm(ReadOnlyFieldsMixin, FormHorizontalMixin, CommitDescriptionMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False

    readonly_fields = ['name']

    class Meta:
        model = models.Company
        fields = [
            'name',
            'official_name',
            'common_name',
            'is_friend',
            'display_brands_in_description',
            'plCapital',
            'plWorkers',
            'plRnD',
            'plRegistered',
            'plNotGlobEnt',
            'description',
            'sources',
            'verified',
            'Editor_notes',
            'nip',
            'address',
            'logotype',
            'official_url',
        ]


class CompanyCreateFromKRSForm(SingleButtonMixin, FormHorizontalMixin, forms.Form):
    is_krs = forms.ChoiceField(widget=forms.RadioSelect, label="Typ", choices=((1, 'KRS'), (0, 'NIP')), initial=1)
    no = forms.CharField(label="Numer", max_length=20, required=False)

    def clean(self):
        cleaned_data = super().clean()

        is_krs = cleaned_data['is_krs'] == '1'
        no = cleaned_data['no']
        companies = self.get_companies_from_api(is_krs, no)
        if len(companies) == 0:
            raise forms.ValidationError("Nie znaleziono firmy o danym numerze KRS/NIP", 'error')
        if len(companies) >= 2:
            raise forms.ValidationError("Jest wiele firm o tym numerze KRS/NIP (!)", 'error')
        first_company = companies[0]

        cleaned_data['company'] = first_company._asdict()

        if models.Company.objects.filter(nip=int(first_company.nip)).exists():
            raise forms.ValidationError("Ta firma istnieje już w naszej bazie", 'error')

        return cleaned_data

    def get_companies_from_api(self, is_krs, no):
        del is_krs
        del no
        return []


class BrandForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow creating a brand without selecting a company in the form.
        if 'company' in self.fields:
            self.fields['company'].required = False

    class Meta:
        model = models.Brand
        fields = ['name', 'common_name', 'company', 'logotype']
        widgets = {'company': autocomplete.ModelSelect2(url='company:company-autocomplete')}


BrandFormSet = inlineformset_factory(
    models.Company, models.Brand, fields=['name', 'common_name', 'company'], exclude=[], can_delete=True
)


class BrandFormSetHelper(FormHelper):
    template = 'bootstrap/table_inline_formset.html'
    form_tag = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
