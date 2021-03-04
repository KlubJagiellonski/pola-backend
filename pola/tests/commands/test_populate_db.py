from django.core.management import call_command
from django.test import TestCase


class PopulateDbTestCase(TestCase):
    def test_run_command(self):
        call_command('populate_db')
