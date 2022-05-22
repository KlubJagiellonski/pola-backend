import os.path
import unittest
from unittest import mock

from faker import Faker
from parameterized import parameterized
from vcr import VCR

from pola.social.forms import SubscribeNewsletterForm

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), 'cassettes'))
fake = Faker()


class TestSubscribeNewsletterForm(unittest.TestCase):
    @parameterized.expand(
        [
            (True,),
            (False,),
        ]
    )
    @vcr.use_cassette('get_response_create_contact_success.yaml', filter_headers=['X-Auth-Token'])
    def test_form_valid(self, include_contact_name):
        data = {
            'contact_email': fake.free_email(),
            'contact_name': fake.name(),
        }
        if not include_contact_name:
            del data['contact_name']
        form = SubscribeNewsletterForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

    @vcr.use_cassette('get_response_create_contact_invalid_email.yaml', filter_headers=['X-Auth-Token'])
    @mock.patch('pola.integrations.get_response.sleep')
    def test_form_server_error(self, mock_sleep):
        form = SubscribeNewsletterForm(
            data={
                'contact_email': 'A@example.org',
                'contact_name': fake.name(),
            }
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(len(mock_sleep.mock_calls), 5)
        self.assertLess(sum(d.args[0] for d in mock_sleep.mock_calls), 20)

    def test_form_invalid_email(self):
        form = SubscribeNewsletterForm(
            data={
                'contact_email': '@a.pl',
                'contact_name': fake.name(),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.get_json_data(),
            {"contact_email": [{"message": "Wprowad\u017a poprawny adres email.", "code": "invalid"}]},
        )

    @vcr.use_cassette('get_response_create_contact_duplicate_email.yaml', filter_headers=['X-Auth-Token'])
    @mock.patch('pola.integrations.get_response.sleep')
    def test_form_duplicate_email(self, mock_sleep):
        for _ in range(2):
            form = SubscribeNewsletterForm(
                data={
                    'contact_email': fake.email(domain="kj.org.pl"),
                    'contact_name': fake.name(),
                }
            )
            self.assertTrue(form.is_valid())
            form.save()

        self.assertEqual(len(mock_sleep.mock_calls), 0)

    def test_form_empty_email(self):
        form = SubscribeNewsletterForm(
            data={
                'contact_email': '',
                'contact_name': fake.name(),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.get_json_data(), {'contact_email': [{'code': 'required', 'message': 'To pole jest wymagane.'}]}
        )
