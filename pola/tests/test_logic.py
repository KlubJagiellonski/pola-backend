from unittest import mock

from parameterized import parameterized
from test_plus import TestCase

from company.factories import CompanyFactory
from pola.logic import get_by_code, get_result_from_code
from product.factories import ProductFactory
from product.models import Product

TEST_EAN13 = "5900084231145"


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
                "code": "5900084231145",
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
                    'Ten produkt został wyprodukowany przez zagraniczną firmę, której '
                    'miejscem rejestracji jest: {}.'.format(country)
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
                'code': '5900084231145',
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

    def test_code_with_multiple_company(self):
        current_ean = TEST_EAN13
        company1 = CompanyFactory.create(name='test-company1', description='test-description')
        company2 = CompanyFactory.create(name='test-company2', description='test-description')

        product = ProductFactory.create(code=current_ean, company=company1, brand__company=company2)

        with mock.patch("pola.logic.get_by_code", return_value=product):
            response = get_result_from_code(current_ean)
        # TODO: Add support for multiple companies in this response
        expected_response = (
            {
                'altText': None,
                'card_type': 'type_grey',
                'code': '5900084231145',
                'description': 'test-description',
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


class TestGetByCode(TestCase):
    def test_should_read_existing_object(self):
        Product(code=TEST_EAN13, name="NAME").save()
        response = get_by_code(TEST_EAN13)
        self.assertEqual(response.name, "NAME")

    def test_should_create_new_when_missing(self):
        self.assertEqual(0, Product.objects.count())
        response = get_by_code(TEST_EAN13)
        self.assertEqual(response.name, None)
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


class TestRemDblNewlines(TestCase):
    pass


class TestStripDblSpaces(TestCase):
    pass


class TestIlimCompareStr(TestCase):
    pass


class TestStripUrlsNewlines(TestCase):
    pass
