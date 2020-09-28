import json
from unittest.mock import patch

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from test_plus.test import TestCase

from company.factories import CompanyFactory
from pola.models import Query
from product.factories import ProductFactory
from report.factories import ReportFactory
from report.models import Attachment, Report


class JsonRequestMixin:
    def json_request(self, url, data=None, **kwargs):
        body = json.dumps(data)
        return self.client.post(url, body, content_type="application/json", **kwargs)


class TestGetAiPics(TestCase):
    url = '/a/v3/get_ai_pics'


class TestAddAiPics(TestCase):
    url = '/a/v3/add_ai_pics'


class TestGetByCodeV3(TestCase):
    url = '/a/v3/get_by_code'


class TestCreateReportV3(TestCase):
    url = '/a/v3/create_report'


class TestGetByCodeV2(TestCase):
    url = '/a/v2/get_by_code'


class TestCreateReportV2(TestCase):
    url = '/a/v2/create_report'


class TestUpdateReportV2(TestCase):
    url = '/a/v2/update_report'


class TestAttachFileV2(TestCase):
    url = '/a/v2/attach_file'


class TestGetByCode(TestCase):
    code = "5901887005100"
    url_pattern = '/a/get_by_code/%s'
    url = url_pattern % code

    def setUp(self):
        super().setUp()
        cache.clear()

    @patch('pola.logic.get_by_code')
    def test_not_found_product(self, get_by_code_mock):
        product = ProductFactory(code=self.code, company=None)
        get_by_code_mock.return_value = product
        resp = self.client.get(self.url, {'device_id': 123})

        self.assertEqual(
            resp.json(),
            {'report': 'ask_for_company', 'code': product.code, 'verified': False, 'plScore': None, 'id': product.pk},
        )

    # @patch('pola.logic.get_by_code')
    # def test_rate_limit(self, get_by_code_mock):
    #     get_by_code_mock.return_value = ProductFactory(code=self.code, company=None)
    #     for _ in range(2):
    #         resp = self.client.get(self.url, {'device_id': 123})
    #         self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.client.get(self.url, {'device_id': 123})
    #     self.assertEqual(resp.status_code, 403)

    @patch('pola.logic.get_by_code')
    def test_increment_product_query_counter(self, get_by_code_mock):
        p = ProductFactory(code=self.code, company=None)
        get_by_code_mock.return_value = p

        self.assertEqual(p.query_count, 0)
        self.client.get(self.url, {'device_id': 123})

        p.refresh_from_db()
        self.assertEqual(p.query_count, 1)

        self.client.get(self.url, {'device_id': 123})

        p.refresh_from_db()
        self.assertEqual(p.query_count, 2)

    @patch('pola.logic.get_by_code')
    def test_increment_company_query_counter(self, get_by_code_mock):
        c = CompanyFactory()
        p = ProductFactory(code=self.code, company=c)
        get_by_code_mock.return_value = p

        self.assertEqual(c.query_count, 0)
        self.client.get(self.url, {'device_id': 123})

        c.refresh_from_db()
        self.assertEqual(c.query_count, 1)

        self.client.get(self.url, {'device_id': 123})

        c.refresh_from_db()
        self.assertEqual(c.query_count, 2)

    @patch('pola.logic.get_by_code')
    def test_save_query(self, get_by_code_mock):
        p = ProductFactory(code=self.code)
        get_by_code_mock.return_value = p

        self.client.get(self.url, {'device_id': 123})
        query = Query.objects.latest()

        self.assertEqual(query.product_id, p.pk)
        self.assertEqual(query.client, '123')
        self.assertEqual(query.was_590, True)

    @patch('pola.logic.get_by_code')
    def test_save_query_not_590(self, get_by_code_mock):
        p = ProductFactory(code="1231887005100")
        get_by_code_mock.return_value = p

        self.client.get(self.url_pattern % p.code, {'device_id': 123})

        query = Query.objects.latest()
        self.assertEqual(query.was_590, False)


class TestCreateReport(JsonRequestMixin, TestCase):
    url = '/a/create_report'

    def setUp(self):
        super().setUp()
        cache.clear()
        self.product = ProductFactory()

    def test_success_without_product(self):
        resp = self._request(self.url + '?device_id=123',)
        report = Report.objects.latest()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"id": report.pk})
        self.assertEqual(report.product, None)

    def test_success_with_product(self):
        resp = self._request(self.url + '?device_id=123', json={'product_id': self.product.id})
        report = Report.objects.latest()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"id": report.pk})
        self.assertEqual(report.product, self.product)

    # def test_rate_limit(self):
    #     for _ in range(2):
    #         resp = self._request(self.url + '?device_id=123')
    #         self.assertEqual(resp.status_code, 200)
    #
    #     resp = self._request(self.url + '?device_id=123')
    #     self.assertEqual(resp.status_code, 403)

    def _request(self, url, json=None):
        r_json = {'description': "Desc"}
        if json:
            r_json.update(**json)
        return self.json_request(url, data=r_json)


class TestUpdateReport(JsonRequestMixin, TestCase):
    url = '/a/update_report'

    def setUp(self):
        super().setUp()
        cache.clear()
        self.report = ReportFactory()

    def test_success_update(self):
        resp = self.json_request(
            self.url + '?device_id={}&report_id={}'.format(self.report.client, self.report.id),
            data={'description': "New description"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"id": self.report.pk})
        self.report.refresh_from_db()
        self.assertEqual(self.report.description, "New description")

    # def test_rate_limit(self):
    #     for _ in range(2):
    #         resp = self.json_request(
    #             self.url + '?device_id=%s&report_id=%s' % (self.report.client, self.report.id),
    #             data={'description': "New description"}
    #         )
    #         self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.json_request(
    #         self.url + '?device_id=%s&report_id=%s' % (self.report.client, self.report.id),
    #         data={'description': "New description"}
    #     )
    #     self.assertEqual(resp.status_code, 403)


class TestAttachFile(TestCase):
    url = '/a/attach_file'

    def setUp(self):
        super().setUp()
        cache.clear()
        self.report = ReportFactory()

    def test_success_attach_file(self):
        file = SimpleUploadedFile("image1.jpeg", b"file_content", content_type="image/jpeg")
        resp = self.client.post(
            self.url + '?device_id={}&report_id={}'.format(self.report.client, self.report.id), {'file': file}
        )
        attachment = Attachment.objects.last()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"id": attachment.pk})

    # def test_rate_limit(self):
    #     file = SimpleUploadedFile("image1.jpeg", b"file_content", content_type="image/jpeg")
    #     for _ in range(5):
    #         resp = self.client.post(
    #             self.url + '?device_id=%s&report_id=%s' % (self.report.client, self.report.id),
    #             {'file': file}
    #         )
    #         self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.client.post(
    #         self.url + '?device_id=%s&report_id=%s' % (self.report.client, self.report.id),
    #         {'file': file}
    #     )
    #     self.assertEqual(resp.status_code, 403)
