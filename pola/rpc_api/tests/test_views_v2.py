from test_plus import TestCase

from pola.company.factories import CompanyFactory
from pola.product.factories import ProductFactory
from pola.report.factories import ReportFactory
from pola.rpc_api.tests.test_views import JsonRequestMixin


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
