#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

from mojepanstwo_api2.krs import Krs
from pola.forms import CommitDescriptionMixin, FormHorizontalMixin, ReadOnlyFieldsMixin, \
    SaveButtonMixin, SingleButtonMixin

from . import models


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
            'Editor_notes',
            'nip',
            'address',
        ]


class CompanyCreateFromKRSForm(SingleButtonMixin, FormHorizontalMixin, forms.Form):
    is_krs = forms.ChoiceField(widget=forms.RadioSelect, label="Typ",
                               choices=((1, 'KRS'), (0, 'NIP')),
                               initial=1)
    no = forms.CharField(label="Numer", max_length=20, required=False)

    def clean(self):
        cleaned_data = super(CompanyCreateFromKRSForm, self).clean()

        is_krs = cleaned_data['is_krs'] == '1'
        no = cleaned_data['no']
        companies = self.get_companies_from_api(is_krs, no)
        if len(companies) == 0:
            raise forms.ValidationError(
                "Nie znaleziono firmy o danym numerze KRS/NIP", 'error')
        if len(companies) >= 2:
            raise forms.ValidationError(
                "Jest wiele firm o tym numerze KRS/NIP (!)", 'error')
        first_company = companies[0]

        cleaned_data['company'] = first_company._asdict()

        if models.Company.objects.filter(nip=int(first_company.nip)).exists():
            raise forms.ValidationError(
                u"Ta firma istnieje już w naszej bazie", 'error')

        return cleaned_data

    def get_companies_from_api(self, is_krs, no):
        client = Krs()
        if is_krs:
            return client.get_companies(krs_no=no)
        return client.get_companies(nip_no=no)
