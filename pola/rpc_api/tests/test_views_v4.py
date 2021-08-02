import json

from test_plus import TestCase

from company.factories import CompanyFactory
from pola.rpc_api.tests.test_views import JsonRequestMixin
from product.factories import ProductFactory
from product.models import Product


class TestGetByCodeV4(TestCase, JsonRequestMixin):
    url = '/a/v4/get_by_code'

    def test_should_return_200_for_non_ean_13(self):
        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&code=123",
        )
        self.assertEqual(200, response.status_code)

    def test_should_return_200_when_ai_not_supported(self):
        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&code=123&noai=false",
        )
        self.assertEqual(200, response.status_code)

    def test_should_return_200_when_polish_product(self):
        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=5900049011829")
        self.assertEqual(200, response.status_code, response.content)

    def test_should_return_200_when_product_without_company(self):
        p = Product(code=5900049011829)
        p.name = "test-product"
        p.save()

        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=" + str(p.code))
        self.assertEqual(200, response.status_code, response.content)

    def test_should_return_200_when_polish_and_known_product(self):
        c = CompanyFactory(
            plCapital=100,
            plWorkers=0,
            plRnD=100,
            plRegistered=100,
            plNotGlobEnt=100,
            description="TEST",
            sources="TEST|BBBB",
            verified=True,
            is_friend=True,
            plCapital_notes="AAA",
            plWorkers_notes="BBB",
            plRnD_notes="CCC",
            plRegistered_notes="DDD",
            plNotGlobEnt_notes="EEE",
        )
        p = ProductFactory.create(code=5900049011829, company=c, brand=None)
        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=" + str(p.code))

        self.assertEqual(200, response.status_code, response.content)
        self.maxDiff = None
        self.assertEqual(
            {
                "product_id": p.pk,
                "code": "5900049011829",
                "name": c.common_name,
                "card_type": "type_white",
                "altText": None,
                "report": {
                    "text": "Zg\u0142o\u015b je\u015bli posiadasz bardziej aktualne dane na temat tego produktu",
                    "button_text": "Zg\u0142o\u015b",
                    "button_type": "type_white",
                },
                "companies": [
                    {
                        "name": c.official_name,
                        "plCapital": 100,
                        "plCapital_notes": "AAA",
                        "plWorkers": 0,
                        "plWorkers_notes": "BBB",
                        "plRnD": 100,
                        "plRnD_notes": "CCC",
                        "plRegistered": 100,
                        "plRegistered_notes": "DDD",
                        "plNotGlobEnt": 100,
                        "plNotGlobEnt_notes": "EEE",
                        "plScore": 70,
                        "is_friend": True,
                        "friend_text": "To jest przyjaciel Poli",
                        "description": "TEST",
                        "sources": {"TEST": "BBBB"},
                    }
                ],
                "donate": {
                    "show_button": True,
                    "url": "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
                    "title": "Potrzebujemy 1 zł",
                },
            },
            json.loads(response.content),
        )

    def test_should_return_200_when_multiple_companies(self):
        c1 = CompanyFactory(
            plCapital=100,
            plWorkers=0,
            plRnD=100,
            plRegistered=100,
            plNotGlobEnt=100,
            description="TEST",
            sources="TEST|BBBB",
            verified=True,
            is_friend=True,
            plCapital_notes="AAA",
            plWorkers_notes="BBB",
            plRnD_notes="CCC",
            plRegistered_notes="DDD",
            plNotGlobEnt_notes="EEE",
        )
        c2 = CompanyFactory(
            plCapital=100,
            plWorkers=0,
            plRnD=100,
            plRegistered=100,
            plNotGlobEnt=100,
            description="TEST",
            sources="TEST|BBBB",
            verified=True,
            is_friend=True,
            plCapital_notes="AAA",
            plWorkers_notes="BBB",
            plRnD_notes="CCC",
            plRegistered_notes="DDD",
            plNotGlobEnt_notes="EEE",
        )

        p = ProductFactory.create(code=5900049011829, company=c1, brand__company=c2)
        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=" + str(p.code))
        self.assertEqual(200, response.status_code, response.content)
        self.maxDiff = None

        self.assertEqual(
            {
                "product_id": p.id,
                "code": "5900049011829",
                "name": 'Marka własna - Sieć Lidl',
                "card_type": "type_white",
                "altText": None,
                "report": {
                    "text": "Zg\u0142o\u015b je\u015bli posiadasz bardziej aktualne dane na temat tego produktu",
                    "button_text": "Zg\u0142o\u015b",
                    "button_type": "type_white",
                },
                "companies": [
                    {
                        "name": c1.official_name,
                        "plCapital": 100,
                        "plCapital_notes": "AAA",
                        "plWorkers": 0,
                        "plWorkers_notes": "BBB",
                        "plRnD": 100,
                        "plRnD_notes": "CCC",
                        "plRegistered": 100,
                        "plRegistered_notes": "DDD",
                        "plNotGlobEnt": 100,
                        "plNotGlobEnt_notes": "EEE",
                        "plScore": 70,
                        "is_friend": True,
                        "friend_text": "To jest przyjaciel Poli",
                        "description": "TEST",
                        "sources": {"TEST": "BBBB"},
                    },
                    {
                        "name": c2.official_name,
                        "plCapital": 100,
                        "plCapital_notes": "AAA",
                        "plWorkers": 0,
                        "plWorkers_notes": "BBB",
                        "plRnD": 100,
                        "plRnD_notes": "CCC",
                        "plRegistered": 100,
                        "plRegistered_notes": "DDD",
                        "plNotGlobEnt": 100,
                        "plNotGlobEnt_notes": "EEE",
                        "plScore": 70,
                        "is_friend": True,
                        "friend_text": "To jest przyjaciel Poli",
                        "description": "TEST",
                        "sources": {"TEST": "BBBB"},
                    },
                ],
                "donate": {
                    "show_button": True,
                    "url": "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
                    "title": "Potrzebujemy 1 zł",
                },
            },
            json.loads(response.content),
        )
