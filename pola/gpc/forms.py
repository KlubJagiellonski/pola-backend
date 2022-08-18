from django import forms

from pola.forms import FormHorizontalMixin, SaveButtonMixin

from . import models


class GPCBrickForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.GPCBrick
        fields = ['alias']


class GPCClassForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.GPCClass
        fields = ['alias']


class GPCFamilyForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.GPCFamily
        fields = ['alias']


class GPCSegmentForm(SaveButtonMixin, FormHorizontalMixin, forms.ModelForm):
    class Meta:
        model = models.GPCClass
        fields = ['alias']
