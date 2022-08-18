import os

from test_plus import TestCase
from vcr import VCR

from pola.integrations.produkty_w_sieci import (
    CompanyBase,
    ProductBase,
    ProductQueryResult,
    produkty_w_sieci_client,
)

TEST_EAN13 = "5901520000059"

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), 'cassettes'))


class TestGetProducts(TestCase):
    @vcr.use_cassette('product_ean13.yaml', filter_headers=['X-API-Key'])
    def test_should_response(self):
        dd = produkty_w_sieci_client.get_products(gtin_number__prefix="0" + TEST_EAN13)

        self.assertEqual(
            dd,
            ProductQueryResult(
                count=1,
                next=None,
                previous=None,
                results=[
                    ProductBase(
                        id='3830ebdb-cad0-482b-8e78-285de7a3ed0d',
                        gtinNumber='05901520000059',
                        name='Muszynianka Naturalna woda mineralna MUSZYNIANKA 1.5l',
                        targetMatket=None,
                        netVolume=None,
                        unit=None,
                        description=(
                            'Naturalna woda mineralna MUSZYNIANKA 1,5l wysokozmineralizowana niskonasycona CO2'
                        ),
                        descriptionLanguage='pl',
                        brand='Muszynianka',
                        isPublic=True,
                        gpc='10000232',
                        productPage=None,
                        imageUrls=[],
                        lastModified='2022-03-31T09:10:30.834000+00:00',
                        company=CompanyBase(
                            name='MUSZYNIANKA Sp. z o.o.',
                            nip='7343575005',
                            street='ul. Tadeusza Kościuszki 58',
                            webPage='http://muszynianka.pl/',
                            city='Krynica-Zdrój',
                            postalCode='33-380',
                        ),
                    )
                ],
            ),
        )
