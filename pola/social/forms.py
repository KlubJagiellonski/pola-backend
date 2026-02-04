import requests.exceptions
from django import forms
from django.conf import settings

from pola.integrations.get_response import get_response_client

try:
    import sentry_sdk
except ImportError:  # pragma: no cover - optional dependency
    sentry_sdk = None


class SubscribeNewsletterForm(forms.Form):
    contact_email = forms.EmailField(label='Contact e-mail', max_length=100, required=True)
    contact_name = forms.CharField(label='Contact name', max_length=100, required=False)

    def save(self):
        try:
            get_response_client.create_contact(
                campaign_id=settings.GET_RESPONSE['CAMPAIGN_ID'],
                email=self.cleaned_data['contact_email'],
                name=self.cleaned_data['contact_name'],
            )
            return True
        except requests.exceptions.HTTPError as error:
            if sentry_sdk:
                sentry_sdk.capture_exception(error)
            return False
