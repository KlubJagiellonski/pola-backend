import json
import os
from unittest import mock

from django.urls import reverse_lazy
from test_plus.test import TestCase
from vcr import VCR

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), 'cassettes'))


class TestSubscribeNewsletterFormView(TestCase):
    url = reverse_lazy('api:subscribe_newsletter_v4')

    @vcr.use_cassette('get_response_create_contact_success.yaml', filter_headers=['X-Auth-Token'])
    def test_form_valid(self):
        response = self.client.post(
            self.url, data=json.dumps({'contact_email': 'Aasdasda@a.pl'}), content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)

    @vcr.use_cassette('get_response_create_contact_success.yaml', filter_headers=['X-Auth-Token'])
    def test_form_invalid_missing_email(self):
        response = self.client.post(self.url, data=json.dumps({'contact_email': ''}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'type': 'about:blank',
                'title': 'Weryfikacja formularza nie powiodła się.',
                'detail': 'Formularz zawiera błędy i nie można go zapisać.',
                'status': 400,
                'contact_email': [{'message': 'To pole jest wymagane.', 'code': 'required'}],
            },
        )

    @vcr.use_cassette('get_response_create_contact_invalid_email.yaml', filter_headers=['X-Auth-Token'])
    @mock.patch('pola.integrations.get_response.sleep')
    def test_form_valid_unable_to_save(self, mock_sleep):
        response = self.client.post(
            self.url, data=json.dumps({'contact_email': 'A@example.org'}), content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {
                'type': 'about:blank',
                'title': 'Nie zapisano.',
                'detail': 'Nie udało się zapisać formularza.',
                'status': 500,
            },
        )
