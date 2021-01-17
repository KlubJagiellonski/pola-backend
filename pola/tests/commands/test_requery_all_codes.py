from unittest import TestCase

from django.core.management import call_command


class RequeryAllCodesTestCase(TestCase):
    def test_run_command(self):
        call_command('requery_all_codes')
