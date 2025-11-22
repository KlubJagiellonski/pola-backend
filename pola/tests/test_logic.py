import os
from unittest import mock

from django.core.files.base import ContentFile
from parameterized import parameterized
from test_plus import TestCase
from vcr import VCR

from pola.company.factories import BrandFactory, CompanyFactory
from pola.gpc.factories import GPCBrickFactory
from pola.logic import (
    _find_replacements,
    get_by_code,
    get_result_from_code,
    handle_product_replacements,
)
from pola.product.factories import ProductFactory
from pola.product.models import Product
from pola.tests.test_utils import get_dummy_image

TEST_EAN13 = "5901520000059"

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), 'cassettes'))


class TestGetResultFromCode(TestCase):
    maxDiff = None

    def test_should_return_empty_message_on_invalid_code(self):
        self.maxDiff = None
        response = get_result_from_code("ABC")
        expected_response = (
            {
                "altText": (
                    "Pola rozpoznaje tylko kody kreskowe typu EAN8 i EAN13. "
                    "Zeskanowany przez Ciebie kod jest innego typu. Spróbuj "
                    "zeskanować kod z czegoś innego"
                ),
                "card_type": "type_white",
                "code": "ABC",
                "name": "Nieprawidłowy kod",
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": None,
                "plWorkers": None,
                "plWorkers_notes": None,
                "product_id": None,
                'official_url': None,
                'logotype_url': None,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_white",
                "report_text": "Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego " "produktu",
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            None,
        )
        self.assertEqual(expected_response, response)

        response = get_result_from_code("123123")
        expected_response[0]["code"] = "123123"
        self.assertEqual(expected_response, response)

    @mock.patch("pola.logic.get_by_code")
    def test_missing_company_and_590(self, mock_get_by_code):
        product = ProductFactory.create(code=TEST_EAN13, company=None, brand=None)
        mock_get_by_code.return_value = product
        response = get_result_from_code(TEST_EAN13)

        expected_response = (
            {
                "altText": (
                    "Każde skanowanie jest rejestrowane. Najczęściej skanowane firmy i produkty, "
                    "których nie mamy jeszcze w bazie, są weryfikowane w pierwszej kolejności. "
                    "Nie pobieramy przy tym żadnych informacji o użytkowniku.\n"
                    "\n"
                    "Jeśli chcesz zgłosić błąd lub wyrazić opinię, prosimy o kontakt: pola@klubjagiellonski.pl"
                ),
                "card_type": "type_grey",
                "code": TEST_EAN13,
                "name": "Tego produktu nie mamy jeszcze w bazie",
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": None,
                "plWorkers": None,
                "plWorkers_notes": None,
                'official_url': None,
                'logotype_url': None,
                "product_id": product.id,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_red",
                "report_text": "Bardzo prosimy o zgłoszenie nam tego produktu",
            },
            {"was_590": True, "was_plScore": False, "was_verified": False},
            product,
        )
        self.assertEqual(expected_response, response)

    @parameterized.expand([("977",), ('978',), ('979',)])
    def test_missing_company_and_book(self, prefix):
        current_ean = prefix + TEST_EAN13[3:]
        product = ProductFactory.create(code=current_ean, company=None, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                "altText": (
                    'Zeskanowany kod jest kodem ISBN/ISSN/ISMN dotyczącym książki,  '
                    'czasopisma lub albumu muzycznego. Wydawnictwa tego typu nie są '
                    'aktualnie w obszarze zainteresowań Poli.'
                ),
                "card_type": "type_white",
                "code": current_ean,
                "name": "Kod ISBN/ISSN/ISMN",
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": None,
                "plWorkers": None,
                "plWorkers_notes": None,
                'official_url': None,
                'logotype_url': None,
                "product_id": product.id,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_white",
                "report_text": 'To nie jest książka, czasopismo lub album muzyczny? Prosimy o zgłoszenie',
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response, response)

    @parameterized.expand([("481", "Białoruś"), ('462', "Federacja Rosyjska")])
    def test_missing_company_and_russia(self, prefix, country):
        current_ean = prefix + TEST_EAN13[3:]
        product = ProductFactory.create(code=current_ean, company=None, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                "altText": (
                    'Ten produkt został wyprodukowany przez zagraniczną firmę, której '
                    f'miejscem rejestracji jest: {country}. \n'
                    'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz go '
                    'kupić.'
                ),
                "card_type": "type_grey",
                "code": current_ean,
                "name": f'Miejsce rejestracji: {country}',
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": 0,
                "plWorkers": None,
                "plWorkers_notes": None,
                'official_url': None,
                'logotype_url': None,
                "product_id": product.id,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_white",
                "report_text": 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response, response)

    @parameterized.expand(
        [
            (
                "775",
                "Peru",
            ),
            (
                "777",
                "Boliwia",
            ),
            ("779", "Argentyna"),
        ]
    )
    def test_missing_company_and_wrong_country(self, prefix, country):
        current_ean = prefix + TEST_EAN13[3:]
        product = ProductFactory.create(code=current_ean, company=None, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                "altText": (
                    f'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    f'której miejscem rejestracji jest: {country}.'
                ),
                "card_type": "type_grey",
                "code": current_ean,
                "name": f'Miejsce rejestracji: {country}',
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": 0,
                "plWorkers": None,
                "plWorkers_notes": None,
                'official_url': None,
                'logotype_url': None,
                "product_id": product.id,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_white",
                "report_text": 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_internal_code(self):
        prefix = "000"
        current_ean = prefix + TEST_EAN13[3:]
        product = ProductFactory.create(code=current_ean, company=None, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                "altText": (
                    'Zeskanowany kod jest wewnętrznym kodem sieci handlowej. Pola nie '
                    'potrafi powiedzieć o nim nic więcej'
                ),
                "card_type": "type_white",
                "code": current_ean,
                "name": 'Kod wewnętrzny',
                "plCapital": None,
                "plCapital_notes": None,
                "plNotGlobEnt": None,
                "plNotGlobEnt_notes": None,
                "plRegistered": None,
                "plRegistered_notes": None,
                "plRnD": None,
                "plRnD_notes": None,
                "plScore": None,
                "plWorkers": None,
                "plWorkers_notes": None,
                'official_url': None,
                'logotype_url': None,
                "product_id": product.id,
                "report_button_text": "Zgłoś",
                "report_button_type": "type_white",
                "report_text": 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_replacements_are_included_and_report_text_updated(self):
        current_ean = TEST_EAN13
        company = CompanyFactory.create(description='desc')
        product = ProductFactory.create(code=current_ean, company=company, brand=None)

        # Create replacements
        r1 = ProductFactory.create(name="Alt1")
        r2 = ProductFactory.create(name="Alt2")
        r3 = ProductFactory.create(name="Alt3")
        r4 = ProductFactory.create(name="Alt4")
        product.replacements.add(r1, r2, r3, r4)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        result = response[0]
        # Replacements list should be present; compare key fields only
        self.assertIn("replacements", result)
        c1 = (
            (r1.brand.common_name or r1.brand.name)
            if r1.brand
            else (r1.company.common_name or r1.company.official_name or r1.company.name)
        )
        c2 = (
            (r2.brand.common_name or r2.brand.name)
            if r2.brand
            else (r2.company.common_name or r2.company.official_name or r2.company.name)
        )
        c3 = (
            (r3.brand.common_name or r3.brand.name)
            if r3.brand
            else (r3.company.common_name or r3.company.official_name or r3.company.name)
        )
        c4 = (
            (r4.brand.common_name or r4.brand.name)
            if r4.brand
            else (r4.company.common_name or r4.company.official_name or r4.company.name)
        )
        expected = [
            (r1.code, "Alt1", f"Alt1 ({c1})"),
            (r2.code, "Alt2", f"Alt2 ({c2})"),
            (r3.code, "Alt3", f"Alt3 ({c3})"),
            (r4.code, "Alt4", f"Alt4 ({c4})"),
        ]
        actual = [(d["code"], d["name"], d["display_name"]) for d in result["replacements"]]
        self.assertEqual(expected, actual)

        # Report text
        expected_prefix = "Polskie alternatywy"
        expected_suffix = "Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu"

        self.assertTrue(result["report_text"].startswith(expected_prefix))
        self.assertTrue(result["report_text"].endswith(expected_suffix))

    def test_code_with_one_company(self):
        current_ean = TEST_EAN13
        company = CompanyFactory.create(description='test-description')
        product = ProductFactory.create(code=current_ean, company=company, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': TEST_EAN13,
                'description': 'test-description',
                'is_friend': False,
                'name': company.official_name,
                'plCapital': None,
                'plCapital_notes': None,
                'plNotGlobEnt': None,
                'plNotGlobEnt_notes': None,
                'plRegistered': None,
                'plRegistered_notes': None,
                'plRnD': None,
                'plRnD_notes': None,
                'plScore': None,
                'plWorkers': None,
                'plWorkers_notes': None,
                'official_url': None,
                'logotype_url': None,
                'product_id': product.id,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': ('Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu'),
                'sources': {},
            },
            {"was_590": True, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_code_with_one_company_with_logo(self):
        current_ean = TEST_EAN13
        dummy_logo = get_dummy_image()
        dummy_file = ContentFile(dummy_logo, name="AA.jpg")

        company = CompanyFactory.create(
            description='test-description',
            official_url="https://google.com/",
            logotype=dummy_file,
        )
        product = ProductFactory.create(code=current_ean, company=company, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        self.assertIn(os.environ.get("POLA_APP_AWS_S3_ENDPOINT_URL"), response[0]["logotype_url"])
        self.assertEqual("https://google.com/", response[0]["official_url"])

    def test_russian_code_with_one_company(self):
        prefix = "462"
        current_ean = prefix + TEST_EAN13[3:]
        company = CompanyFactory.create(description='test-description')
        product = ProductFactory.create(code=current_ean, company=company, brand=None)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': '4621520000059',
                'description': (
                    'test-description\n'
                    'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    'której miejscem rejestracji jest: Federacja Rosyjska. \n'
                    'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz '
                    'go kupić.'
                ),
                'is_friend': False,
                'name': company.official_name,
                'plCapital': None,
                'plCapital_notes': None,
                'plNotGlobEnt': None,
                'plNotGlobEnt_notes': None,
                'plRegistered': None,
                'plRegistered_notes': None,
                'plRnD': None,
                'plRnD_notes': None,
                'plScore': None,
                'plWorkers': None,
                'plWorkers_notes': None,
                'official_url': None,
                'logotype_url': None,
                'product_id': product.id,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
                'sources': {},
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_display_brand_when_enabled_on_company(self):
        current_ean = TEST_EAN13
        company = CompanyFactory.create(description='test-description', display_brands_in_description=True)
        product = ProductFactory.create(code=current_ean, company=company, brand=None)
        BrandFactory.create(common_name="brand-1", company=company)
        BrandFactory.create(common_name="brand-2", company=company, website_url="test.pl")
        BrandFactory.create(common_name="brand-3", company=company, website_url="moja_domena_testowa_123.com")

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)

        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': TEST_EAN13,
                'description': ('test-description\n' 'Ten producent psoiada marki: brand-1, brand-2, brand-3.'),
                'is_friend': False,
                'name': company.official_name,
                'plCapital': None,
                'plCapital_notes': None,
                'plNotGlobEnt': None,
                'plNotGlobEnt_notes': None,
                'plRegistered': None,
                'plRegistered_notes': None,
                'plRnD': None,
                'plRnD_notes': None,
                'plScore': None,
                'plWorkers': None,
                'plWorkers_notes': None,
                'official_url': None,
                'logotype_url': None,
                'product_id': product.id,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
                'sources': {},
            },
            {"was_590": True, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_code_with_multiple_company(self):
        current_ean = TEST_EAN13
        company1 = CompanyFactory.create(name='test-company1', description='test-description1.')
        company2 = CompanyFactory.create(name='test-company2', description='test-description2.')

        product = ProductFactory.create(code=current_ean, company=company1, brand__company=company2)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)
        # TODO: Add support for multiple companies in this response
        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': TEST_EAN13,
                'description': 'test-description1.',
                'is_friend': False,
                'name': company1.official_name,
                'plCapital': None,
                'plCapital_notes': None,
                'plNotGlobEnt': None,
                'plNotGlobEnt_notes': None,
                'plRegistered': None,
                'plRegistered_notes': None,
                'plRnD': None,
                'plRnD_notes': None,
                'plScore': None,
                'plWorkers': None,
                'plWorkers_notes': None,
                'official_url': None,
                'logotype_url': None,
                'product_id': product.id,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': ('Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu'),
                'sources': {},
            },
            {"was_590": True, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)

    def test_russian_code_with_multiple_company(self):
        prefix = "462"
        current_ean = prefix + TEST_EAN13[3:]
        company1 = CompanyFactory.create(name='test-company1', description='test-description1.')
        company2 = CompanyFactory.create(name='test-company2', description='test-description2.')

        product = ProductFactory.create(code=current_ean, company=company1, brand__company=company2)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)
        # TODO: Add support for multiple companies in this response
        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': '4621520000059',
                'description': (
                    'test-description1.\n'
                    'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    'której miejscem rejestracji jest: Federacja Rosyjska. \n'
                    'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz '
                    'go kupić.'
                ),
                'is_friend': False,
                'name': company1.official_name,
                'plCapital': None,
                'plCapital_notes': None,
                'plNotGlobEnt': None,
                'plNotGlobEnt_notes': None,
                'plRegistered': None,
                'plRegistered_notes': None,
                'plRnD': None,
                'plRnD_notes': None,
                'plScore': None,
                'plWorkers': None,
                'plWorkers_notes': None,
                'official_url': None,
                'logotype_url': None,
                'product_id': product.id,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': ('Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu'),
                'sources': {},
            },
            {"was_590": False, "was_plScore": False, "was_verified": False},
            product,
        )
        self.maxDiff = None
        self.assertEqual(expected_response[0], response[0])
        self.assertEqual(expected_response, response)


class TestGetByCode(TestCase):
    @vcr.use_cassette('product_ean13_v2.yaml', filter_headers=['X-API-KEY'])
    def test_should_read_existing_object(self):
        # Ensure GPC exists for update flow when product has no company
        GPCBrickFactory(code="10000232")
        Product(code=TEST_EAN13, name="NAME").save()
        # Existing product without company should still trigger API update
        response = get_by_code(TEST_EAN13)
        self.assertEqual(response.name, "NAME")
        self.assertIsNotNone(response.company)
        self.assertEqual(1, Product.objects.count())

    @vcr.use_cassette('product_ean13_v2.yaml', filter_headers=['X-API-KEY'])
    def test_should_create_new_when_missing(self):
        GPCBrickFactory(code="10000232")
        self.assertEqual(0, Product.objects.count())
        response = get_by_code(TEST_EAN13)
        self.assertEqual(response.name, 'Muszynianka Naturalna woda mineralna MUSZYNIANKA. 1.5l')
        self.assertEqual(1, Product.objects.count())


class TestCreateFromApi(TestCase):
    pass


class TestUpdateCompanyFromKrs(TestCase):
    pass


class TestCreateBotReport(TestCase):
    pass


class TestGetPlScore(TestCase):
    pass


class TestShareholdersToStr(TestCase):
    pass


class TestHandleProductReplacements(TestCase):
    def test_no_replacements_keeps_report_unchanged(self):
        product = ProductFactory.create()
        result = {}
        report = {"text": "Original report"}

        handle_product_replacements(product, result, report)

        self.assertNotIn("replacements", result)
        self.assertEqual("Original report", report["text"])

    def test_adds_replacements_and_updates_report_text_default_topk(self):
        product = ProductFactory.create()
        r1 = ProductFactory.create(name="Alt1")
        r2 = ProductFactory.create(name="Alt2")
        r3 = ProductFactory.create(name="Alt3")
        r4 = ProductFactory.create(name="Alt4")
        product.replacements.add(r1, r2, r3, r4)

        result = {}
        report = {"text": "Please report updates"}

        handle_product_replacements(product, result, report)

        self.assertIn("replacements", result)
        expected = [
            (
                r1.code,
                "Alt1",
                (
                    (r1.brand.common_name or r1.brand.name)
                    if r1.brand
                    else (r1.company.common_name or r1.company.official_name or r1.company.name)
                ),
            ),
            (
                r2.code,
                "Alt2",
                (
                    (r2.brand.common_name or r2.brand.name)
                    if r2.brand
                    else (r2.company.common_name or r2.company.official_name or r2.company.name)
                ),
            ),
            (
                r3.code,
                "Alt3",
                (
                    (r3.brand.common_name or r3.brand.name)
                    if r3.brand
                    else (r3.company.common_name or r3.company.official_name or r3.company.name)
                ),
            ),
            (
                r4.code,
                "Alt4",
                (
                    (r4.brand.common_name or r4.brand.name)
                    if r4.brand
                    else (r4.company.common_name or r4.company.official_name or r4.company.name)
                ),
            ),
        ]
        actual = [(d["code"], d["name"], d["company"]) for d in result["replacements"]]
        self.assertEqual(expected, actual)
        # Default topK is 3, include brand/company names in parentheses in the prefix
        c1 = (
            (r1.brand.common_name or r1.brand.name)
            if r1.brand
            else (r1.company.common_name or r1.company.official_name or r1.company.name)
        )
        c2 = (
            (r2.brand.common_name or r2.brand.name)
            if r2.brand
            else (r2.company.common_name or r2.company.official_name or r2.company.name)
        )
        c3 = (
            (r3.brand.common_name or r3.brand.name)
            if r3.brand
            else (r3.company.common_name or r3.company.official_name or r3.company.name)
        )
        expected_prefix = f"Polskie alternatywy: Alt1 ({c1}), Alt2 ({c2}), Alt3 ({c3})\n"
        self.assertTrue(report["text"].startswith(expected_prefix))
        self.assertTrue(report["text"].endswith("Please report updates"))

    def test_uses_code_when_replacement_name_missing(self):
        product = ProductFactory.create()
        # Create a replacement with no name (but with a company)
        repl = ProductFactory.create(name=None)
        product.replacements.add(repl)

        result = {}
        report = {"text": "Report"}

        handle_product_replacements(product, result, report)

        expected_comp = repl.company.common_name or repl.company.official_name or repl.company.name
        expected_brand = repl.brand.common_name or repl.brand.name
        expected = [
            (
                repl.code,
                repl.code,  # falls back to code when name is missing
                f"{repl.code} ({expected_brand if repl.brand else expected_comp})",
            )
        ]
        actual = [(d["code"], d["name"], d["display_name"]) for d in result["replacements"]]
        self.assertEqual(expected, actual)
        self.assertIn(repl.code, report["text"])  # Listed in alternatives

    def test_does_modify_report_text_when_empty(self):
        product = ProductFactory.create()
        repl = ProductFactory.create(name="AltX")
        product.replacements.add(repl)

        result = {}
        report = {"text": ""}

        handle_product_replacements(product, result, report)

        # Replacements are added, but report text remains empty string
        self.assertEqual("", report["text"])
        expected_comp = repl.company.common_name or repl.company.official_name or repl.company.name
        expected_brand = repl.brand.common_name or repl.brand.name
        expected = [
            (
                repl.code,
                "AltX",
                f"AltX ({expected_brand if repl.brand else expected_comp})",
            )
        ]
        actual = [(d["code"], d["name"], d["display_name"]) for d in result["replacements"]]
        self.assertEqual(expected, actual)


class TestFindReplacements(TestCase):
    def test_empty_when_no_replacements(self):
        product = ProductFactory.create()
        self.assertEqual([], _find_replacements(product.replacements))

    def test_skips_when_no_brand_and_no_company(self):
        product = ProductFactory.create()
        repl = ProductFactory.create(company=None, brand=None)
        product.replacements.add(repl)
        items = _find_replacements(product.replacements)

        self.assertEqual(1, len(items))
        self.assertEqual(repl.code, items[0]["code"])
        # Uses name if present, otherwise code
        expected_name = repl.name or repl.code
        self.assertEqual(expected_name, items[0]["name"])
        self.assertEqual(expected_name, items[0]["display_name"])  # no brand/company to show
        self.assertIn("is_friend", items[0])
        self.assertFalse(items[0]["is_friend"])  # no company -> not a friend

    def test_prefers_brand_name_over_company(self):
        product = ProductFactory.create()
        repl = ProductFactory.create()
        # Ensure both brand and company exist with distinct names
        repl.brand.common_name = "PreferredBrand"
        repl.brand.name = "BrandName"
        repl.brand.save()
        repl.company.common_name = "CompanyCommon"
        repl.company.official_name = "CompanyOfficial"
        repl.company.name = "CompanyName"
        repl.company.save()
        product.replacements.add(repl)

        items = _find_replacements(product.replacements)
        self.assertEqual(1, len(items))
        self.assertEqual(repl.code, items[0]["code"])
        self.assertEqual(repl.name, items[0]["name"])  # uses product name when present
        self.assertEqual(f"{repl.name} (PreferredBrand)", items[0]["display_name"])  # brand wins
        self.assertIn("is_friend", items[0])
        # Reflects company friend flag
        self.assertEqual(repl.company.is_friend, items[0]["is_friend"])

    def test_fallback_to_company_when_no_brand(self):
        product = ProductFactory.create()
        repl = ProductFactory.create(brand=None)
        repl.company.common_name = "CompanyCommonX"
        repl.company.official_name = "CompanyOfficialX"
        repl.company.name = "CompanyNameX"
        repl.company.save()
        product.replacements.add(repl)

        items = _find_replacements(product.replacements)
        self.assertEqual(1, len(items))
        self.assertEqual(f"{repl.name} (CompanyCommonX)", items[0]["display_name"])  # uses company common name
        self.assertIn("is_friend", items[0])
        self.assertEqual(repl.company.is_friend, items[0]["is_friend"])

    def test_fallback_to_company_when_brand_has_no_name(self):
        product = ProductFactory.create()
        # Create a brand with empty names
        repl = ProductFactory.create()
        repl.brand.common_name = None
        repl.brand.name = None
        repl.brand.save()
        # Ensure company present
        repl.company.common_name = "CompanyY"
        repl.company.save()
        product.replacements.add(repl)

        items = _find_replacements(product.replacements)
        self.assertEqual(1, len(items))
        self.assertEqual(f"{repl.name} (CompanyY)", items[0]["display_name"])  # fallback to company
        self.assertIn("is_friend", items[0])
        self.assertEqual(repl.company.is_friend, items[0]["is_friend"])

    def test_uses_code_when_replacement_name_missing(self):
        product = ProductFactory.create()
        repl = ProductFactory.create(name=None)
        product.replacements.add(repl)

        items = _find_replacements(product.replacements)
        self.assertEqual(1, len(items))
        self.assertEqual(repl.code, items[0]["name"])  # fallback to code for name
        self.assertIn("is_friend", items[0])
        self.assertEqual(repl.company.is_friend, items[0]["is_friend"])
