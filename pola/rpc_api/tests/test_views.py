import io
import json

import requests
from test_plus.test import TestCase

from ai_pics.models import AIAttachment, AIPics
from company.factories import CompanyFactory
from product.factories import ProductFactory
from product.models import Product
from report.factories import ReportFactory
from report.models import Attachment, Report


class JsonRequestMixin:
    def json_request(self, url, data=None, **kwargs):
        body = json.dumps(data)
        return self.client.post(url, body, content_type="application/json", **kwargs)


def _create_image(width=100, height=None, color='blue', image_format='JPEG', image_palette='RGB'):
    # ImageField (both django's and factory_boy's) require PIL.
    # Try to import it along one of its known installation paths.
    from PIL import Image

    height = height or width

    thumb_io = io.BytesIO()
    with Image.new(image_palette, (width, height), color) as thumb:
        thumb.save(thumb_io, format=image_format)
    return thumb_io.getvalue()


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


class TestAddAiPics(TestCase, JsonRequestMixin):
    url = '/a/v3/add_ai_pics'

    def test_should_create_simple_report(self):
        p = ProductFactory.create(ai_pics_count=0)

        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID",
            data={
                'product_id': p.pk,
                'files_count': 1,
                'file_ext': "png",
                "mime_type": 'image/jpeg',
                'original_width': 1000,
                'original_height': 2000,
                'width': 100,
                'height': 200,
                'device_name': 'TEST-device',
                'flash_used': True,
                'was_portrait': False,
            },
        )

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(len(response_data['signed_requests']), 1)
        signed_url: str = response_data['signed_requests'][0]
        self.assertTrue(signed_url.startswith("http://minio:9000"))

        # Valid signed URL
        response = requests.put(
            signed_url, data=_create_image(), headers={"x-amz-acl": "public-read", 'Content-Type': 'image/jpeg'}
        )
        self.assertEqual(200, response.status_code, response.text)

        # Assert AIPics
        self.assertEqual(AIPics.objects.count(), 1)
        ai_pics: AIPics = AIPics.objects.first()
        self.assertEqual(p.pk, ai_pics.product_id)
        self.assertEqual("TEST-DEVICE-ID", ai_pics.client)
        self.assertEqual(1000, ai_pics.original_width)
        self.assertEqual(2000, ai_pics.original_height)
        self.assertEqual(100, ai_pics.width)
        self.assertEqual(200, ai_pics.height)
        self.assertEqual(True, ai_pics.flash_used)
        self.assertEqual(False, ai_pics.was_portrait)

        # Assert AIAttachment
        self.assertEqual(1, AIAttachment.objects.count())
        ai_attachment: AIAttachment = AIAttachment.objects.first()
        self.assertTrue(ai_attachment.attachment.name.endswith("png"))
        self.assertEqual(0, ai_attachment.file_no)
        self.assertEqual(200, requests.get(ai_attachment.get_absolute_url()).status_code)

        # Assert product
        self.assertEqual(1, Product.objects.get(pk=p.pk).ai_pics_count)

    def test_should_limit_file_count(self):
        p = ProductFactory.create(ai_pics_count=0)

        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID",
            data={
                'product_id': p.pk,
                'files_count': 50,
                'file_ext': "png",
                "mime_type": 'image/jpeg',
                'original_width': 1000,
                'original_height': 2000,
                'width': 100,
                'height': 200,
                'device_name': 'TEST-device',
                'flash_used': True,
                'was_portrait': False,
            },
        )

        self.assertEqual(403, response.status_code)
        self.assertEqual("Forbidden", response.reason_phrase)


class TestGetByCodeV3(TestCase, JsonRequestMixin):
    url = '/a/v3/get_by_code'

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
                "product_id": p.id,
                "code": "5900049011829",
                "name": c.official_name,
                "card_type": "type_white",
                "plScore": 70,
                "altText": None,
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
                "report_text": "Zg\u0142o\u015b je\u015bli posiadasz bardziej aktualne dane na temat tego produktu",
                "report_button_text": "Zg\u0142o\u015b",
                "report_button_type": "type_white",
                "is_friend": True,
                "friend_text": "To jest przyjaciel Poli",
                "description": "TEST",
                "sources": {"TEST": "BBBB"},
                "donate": {
                    "show_button": True,
                    "url": "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
                    "title": "Potrzebujemy 1 zł",
                },
            },
            json.loads(response.content),
        )

    def test_should_return_200_when_one_comand_in_brand_and_product(self):
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

        p = ProductFactory.create(code=5900049011829, company=c1, brand__company=c1)
        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=" + str(p.code))
        self.assertEqual(200, response.status_code, response.content)
        self.maxDiff = None
        self.assertEqual(
            {
                'altText': None,
                'card_type': 'type_white',
                'code': '5900049011829',
                'description': 'TEST',
                'donate': {
                    'show_button': True,
                    'title': 'Potrzebujemy 1 zł',
                    'url': 'https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/',
                },
                'friend_text': 'To jest przyjaciel Poli',
                'is_friend': True,
                'name': 'company_official_125',
                'plCapital': 100,
                'plCapital_notes': 'AAA',
                'plNotGlobEnt': 100,
                'plNotGlobEnt_notes': 'EEE',
                'plRegistered': 100,
                'plRegistered_notes': 'DDD',
                'plRnD': 100,
                'plRnD_notes': 'CCC',
                'plScore': 70,
                'plWorkers': 0,
                'plWorkers_notes': 'BBB',
                'product_id': p.pk,
                'report_button_text': 'Zgłoś',
                'report_button_type': 'type_white',
                'report_text': 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
                'sources': {'TEST': 'BBBB'},
            },
            json.loads(response.content),
        )


class TestCreateReportV3(TestCase, JsonRequestMixin):
    url = '/a/v3/create_report'

    def test_should_create_report(self):
        p = ProductFactory.create(ai_pics_count=0)

        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID",
            data={
                'description': "test-description",
                'product_id': p.pk,
                'files_count': 1,
                'file_ext': 'jpg',
                'mime_type': 'image/jpeg',
            },
        )
        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(len(response_data['signed_requests']), 1)
        signed_url: str = response_data['signed_requests'][0]
        self.assertTrue(signed_url.startswith("http://minio:9000"))

        # Valid signed URL
        response = requests.put(
            signed_url, data=_create_image(), headers={"x-amz-acl": "public-read", 'Content-Type': 'image/jpeg'}
        )
        self.assertEqual(200, response.status_code, response.text)

        # Assert Report
        self.assertEqual(Report.objects.count(), 1)
        report: Report = Report.objects.get(pk=response_data['id'])
        self.assertEqual(p.pk, report.product_id)
        self.assertEqual("test-description", report.description)
        self.assertEqual("TEST-DEVICE-ID", report.client)
        self.assertEqual(Report.OPEN, report.status())

        # Assert Attachment
        self.assertEqual(1, Attachment.objects.count())
        report = Attachment.objects.first()
        self.assertTrue(report.attachment.name.endswith("jpg"))
        self.assertEqual(200, requests.get(report.get_absolute_url()).status_code)

    def test_should_limit_file_count(self):
        p = ProductFactory.create(ai_pics_count=0)

        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID",
            data={
                'description': "test-description",
                'product_id': p.pk,
                'files_count': 50,
                'file_ext': 'jpg',
                'mime_type': 'image/jpeg',
            },
        )

        self.assertEqual(403, response.status_code)
        self.assertEqual("Forbidden", response.reason_phrase)


class TestGetByCodeV2(TestCase, JsonRequestMixin):
    url = '/a/v2/get_by_code'

    def test_should_return_200_for_non_ean_13(self):
        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&code=123",
        )
        self.assertEqual(200, response.status_code)

    def test_should_return_200_when_polish_and_known_product(self):
        c = CompanyFactory.create(
            plCapital=100,
            plWorkers=0,
            plRnD=100,
            plRegistered=100,
            plNotGlobEnt=100,
            description="KOTEK",
            sources="KOTEK|BBBB",
            verified=True,
            is_friend=True,
            plCapital_notes="AA",
            plWorkers_notes="BBB",
            plRnD_notes="CCC",
            plRegistered_notes="DDD",
            plNotGlobEnt_notes="EEEE",
        )
        p = ProductFactory.create(code=5900049011829, company=c, brand=None)
        response = self.json_request(self.url + "?device_id=TEST-DEVICE-ID&code=" + str(p.code))
        self.assertEqual(200, response.status_code)


class TestCreateReportV2(TestCase, JsonRequestMixin):
    url = '/a/v2/create_report'

    def test_should_return_200_for_non_ean_13(self):
        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&report_id=123", data={'description': "test-description"}
        )
        self.assertEqual(200, response.status_code)


class TestUpdateReportV2(TestCase, JsonRequestMixin):
    url = '/a/v2/update_report'

    def test_should_return_200_for_non_ean_13(self):
        report = ReportFactory.create(client="TEST-DEVICE-ID")

        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&&report_id=" + str(report.pk),
            data={'description': "test-description"},
        )
        self.assertEqual(200, response.status_code)


class TestAttachFileV2(TestCase, JsonRequestMixin):
    url = '/a/v2/attach_file'

    def test_should_return_200_for_non_ean_13(self):
        report = ReportFactory.create(client="TEST-DEVICE-ID")
        response = self.json_request(
            self.url + "?device_id=TEST-DEVICE-ID&report_id=" + str(report.pk),
            data={'file_ext': 'png', 'mime_type': 'AAA'},
        )
        self.assertEqual(200, response.status_code)
