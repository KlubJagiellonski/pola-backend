import json

from test_plus import TestCase

from pola.company.factories import CompanyFactory
from pola.product.factories import ProductFactory
from pola.product.models import Product
from pola.rpc_api.tests.test_views import JsonRequestMixin


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
        self.maxDiff = None
        self.assertEqual(
            {
                'product_id': p.pk,
                'code': '5900049011829',
                'name': 'Tego produktu nie mamy jeszcze w bazie',
                'card_type': 'type_grey',
                'altText': (
                    'Każde skanowanie jest rejestrowane. Najczęściej skanowane firmy i produkty, których nie '
                    'mamy jeszcze w bazie, są weryfikowane w pierwszej kolejności. Nie pobieramy przy tym '
                    'żadnych informacji o użytkowniku.\n\nJeśli chcesz zgłosić błąd lub wyrazić opinię, '
                    'prosimy o kontakt: pola@klubjagiellonski.pl'
                ),
                'report': {
                    'text': 'Bardzo prosimy o zgłoszenie nam tego produktu',
                    'button_text': 'Zgłoś',
                    'button_type': 'type_red',
                },
                'donate': {
                    'show_button': True,
                    'url': 'https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/',
                    'title': 'Potrzebujemy 1 zł',
                },
            },
            json.loads(response.content),
        )

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
                    "url": 'https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/',
                    "title": 'Potrzebujemy 1 zł',
                },
            },
            json.loads(response.content),
        )


class TestSearchV4(TestCase):
    url = '/a/v4/search'

    def test_should_return_error_when_parameter_missing(self):
        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {
                'detail': '1 errors encountered',
                'errors': ['Missing required parameter: query'],
                'status': 400,
                'title': 'Request validation failed',
                'type': 'about:blank',
            },
            json.loads(response.content),
        )

    def test_should_return_error_when_query_is_empty(self):
        response = self.client.get(f"{self.url}?query=", content_type="application/json")
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {
                'detail': '1 errors encountered',
                'errors': ['Value of parameter cannot be empty: query'],
                'status': 400,
                'title': 'Request validation failed',
                'type': 'about:blank',
            },
            json.loads(response.content),
        )

    def test_should_return_empty_result_when_no_product_found(self):
        response = self.client.get(f"{self.url}?query=invalid_name", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual({'nextPageToken': None, 'products': [], 'totalItems': 0}, json.loads(response.content))

    def test_should_return_results_by_product_name(self):
        p1 = ProductFactory(name="baton")
        response = self.client.get(f"{self.url}?query=bat", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': None},
                        'name': p1.name,
                    }
                ],
                'totalItems': 1,
            },
            json.loads(response.content),
        )

    def test_should_return_results_by_product_code(self):
        p1 = ProductFactory(name="test-product")
        response = self.client.get(f"{self.url}?query={p1.code}", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': None},
                        'name': p1.name,
                    }
                ],
                'totalItems': 1,
            },
            json.loads(response.content),
        )

    def test_should_return_results_by_product_code_ean_9(self):
        p1 = ProductFactory(name="test-product", code=f"{42:09}")
        response = self.client.get(f"{self.url}?query={p1.code}", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': None},
                        'name': p1.name,
                    }
                ],
                'totalItems': 1,
            },
            json.loads(response.content),
        )

    def test_should_skip_brand_without_name(self):
        p1 = ProductFactory(name="test-product", brand__name=None)
        response = self.client.get(f"{self.url}?query={p1.code}", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': None,
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': None},
                        'name': p1.name,
                    }
                ],
                'totalItems': 1,
            },
            json.loads(response.content),
        )

    def test_should_skip_company_without_name(self):
        p1 = ProductFactory(name="test-product", company__name=None)
        response = self.client.get(f"{self.url}?query={p1.code}", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': None,
                        'name': p1.name,
                    }
                ],
                'totalItems': 1,
            },
            json.loads(response.content),
        )

    def test_should_serialize_products(self):
        p1 = ProductFactory(name="baton1")
        p2 = ProductFactory(name="baton2", company=None)
        p3 = ProductFactory(name="baton3", brand=None)

        response = self.client.get(f"{self.url}?query=baton", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': None},
                        'name': p1.name,
                    },
                    {
                        'brand': {'name': p2.brand.name},
                        'code': p2.code,
                        'company': None,
                        'name': p2.name,
                    },
                    {
                        'brand': None,
                        'code': p3.code,
                        'company': {'name': p3.company.name, 'score': None},
                        'name': p3.name,
                    },
                ],
                'totalItems': 3,
            },
            json.loads(response.content),
        )

    def test_should_calculate_products(self):
        p1 = ProductFactory(
            name="baton1",
            company__plCapital=100,
            company__plWorkers=100,
            company__plRnD=100,
            company__plRegistered=100,
            company__plNotGlobEnt=100,
        )
        p2 = ProductFactory(
            name="baton2",
            company__plCapital=0,
            company__plWorkers=100,
            company__plRnD=100,
            company__plRegistered=100,
            company__plNotGlobEnt=100,
        )
        p3 = ProductFactory(
            name="baton4",
            company__plCapital=0,
            company__plWorkers=0,
            company__plRnD=100,
            company__plRegistered=100,
            company__plNotGlobEnt=100,
        )

        response = self.client.get(f"{self.url}?query=baton", content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.maxDiff = None
        self.assertEqual(
            {
                'nextPageToken': None,
                'products': [
                    {
                        'brand': {'name': p1.brand.name},
                        'code': p1.code,
                        'company': {'name': p1.company.name, 'score': 100},
                        'name': p1.name,
                    },
                    {
                        'brand': {'name': p2.brand.name},
                        'code': p2.code,
                        'company': {'name': p2.company.name, 'score': 65},
                        'name': p2.name,
                    },
                    {
                        'brand': {'name': p3.brand.name},
                        'code': p3.code,
                        'company': {'name': p3.company.name, 'score': 35},
                        'name': p3.name,
                    },
                ],
                'totalItems': 3,
            },
            json.loads(response.content),
        )

    def test_should_support_pagination(self):
        ProductFactory.create_batch(11, name="baton")

        response = self.client.get(f"{self.url}?query=baton", content_type="application/json")
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.content)
        self.assertEqual(10, len(response_data['products']))
        self.assertEqual(11, response_data['totalItems'])
        next_page_token = response_data['nextPageToken']

        response = self.client.get(
            f"{self.url}?query=baton&pageToken={next_page_token}", content_type="application/json"
        )
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.content)
        self.assertEqual(1, len(response_data['products']))
        self.assertEqual(11, response_data['totalItems'])
