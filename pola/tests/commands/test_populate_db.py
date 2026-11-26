from django.core.management import call_command
from django.test import TestCase

from pola.openfoodfacts.models import Product
from pola.openfoodfacts.samples import load_samples


class PopulateDbTestCase(TestCase):
    def test_run_command(self):
        call_command('populate_db')

    def test_delete_removes_openfoodfacts_samples(self):
        load_samples()
        self.assertEqual(Product.objects.count(), 100)
        call_command('populate_db', '--delete')
        self.assertEqual(Product.objects.count(), 0)
