import os

from django.test import override_settings
from test_plus import TestCase
from vcr import VCR

from pola.integrations.produkty_w_sieci import produkty_w_sieci_client

TEST_EAN13 = "5901520000059"

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), 'cassettes'))


@override_settings()
class TestGetProducts(TestCase):
    @vcr.use_cassette('product_ean13_v2.yaml', filter_headers=['X-API-KEY'])
    def test_should_response(self):
        dd = produkty_w_sieci_client.get_products(gtin_number=TEST_EAN13)
        print(dd)
