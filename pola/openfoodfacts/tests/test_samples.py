from django.test import TestCase

from pola.openfoodfacts.models import Product
from pola.openfoodfacts.samples import delete_samples, load_samples


class OpenFoodFactsSamplesTests(TestCase):
    def test_load_and_delete_samples(self):
        self.assertEqual(load_samples(), 100)
        self.assertEqual(Product.objects.count(), 100)
        self.assertEqual(Product.objects.get(code='5900000000001').product_name, 'Mleko owsiane')
        self.assertIsNone(Product.objects.get(code='5900000000003').energy_kcal)
        self.assertEqual(Product.objects.get(code='5900000000100').product_name, 'Jabłka suszone 100')

        delete_samples()

        self.assertFalse(Product.objects.exists())
