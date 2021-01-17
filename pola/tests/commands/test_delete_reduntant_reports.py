from unittest import TestCase

from django.core.management import call_command


class DeleteRaduntantProductsTestCase(TestCase):
    def test_run_command(self):
        call_command('delete_reduntant_reports', '10')
