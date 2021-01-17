from unittest import TestCase

from django.core.management import call_command


class Requery590CodesTestCase(TestCase):
    def test_run_command(self):
        call_command('requery_590_codes')
