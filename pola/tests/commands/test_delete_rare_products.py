from unittest import TestCase

from django.core.management import call_command


class DeleteRareProductsTestCase(TestCase):
    def test_run_command(self):
        call_command('delete_rare_products', '10')
