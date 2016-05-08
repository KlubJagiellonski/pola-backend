#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from mojepanstwo_api import KrsClient
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
            'Editor_notes',
            'nip',
            'address',
        ]


class CompanyCreateFromKRSForm(forms.Form):
    is_krs = forms.ChoiceField(widget=forms.RadioSelect, label="Identyfikator",
                               choices=((1, 'KRS'), (0, 'NIP')),
                               initial=1)
    no = forms.CharField(max_length=20, label="", required=False)

    def clean(self):
        cleaned_data = super(CompanyCreateFromKRSForm, self).clean()
        krs = KrsClient()
        if cleaned_data['is_krs'] == '1':
            json = krs.query_podmiot(
                'conditions[krs_podmioty.krs]', cleaned_data['no'])
        else:
            json = krs.query_podmiot(
                'conditions[krs_podmioty.nip]', cleaned_data['no'])

        if json is None or json['Count'] == 0:
            raise forms.ValidationError(
                "Nie znaleziono firmy o danym numerze KRS/NIP", 'error')
        if json is None or json['Count'] > 1:
            raise forms.ValidationError(
                "Jest wiele firm o tym numerze KRS/NIP (!)", 'error')

        company = krs.json_to_company(json, 0)
        cleaned_data['company'] = company

        c = models.Company.objects.filter(nip=company['nip']).count()
        if c > 0:
            raise forms.ValidationError(
                u"Ta firma istnieje już w naszej bazie", 'error')

        return cleaned_data
