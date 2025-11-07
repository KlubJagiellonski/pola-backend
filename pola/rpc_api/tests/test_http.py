from django.http import HttpResponseForbidden
from test_plus import TestCase

from pola.report.factories import ReportFactory
from pola.rpc_api.http import validate_report_ownership


class TestValidateReportOwnership(TestCase):
    def test_should_return_none_when_device_matches(self):
        """validate_report_ownership should return None when device_id matches report.client"""
        device_id = "TEST-DEVICE-ID"
        report = ReportFactory.create(client=device_id)

        result = validate_report_ownership(report, device_id)

        self.assertIsNone(result)

    def test_should_return_forbidden_when_device_mismatch(self):
        """validate_report_ownership should return HttpResponseForbidden when device_id doesn't match"""
        report = ReportFactory.create(client="DEVICE-1")
        different_device_id = "DEVICE-2"

        result = validate_report_ownership(report, different_device_id)

        self.assertIsInstance(result, HttpResponseForbidden)
        self.assertEqual(result.status_code, 403)

    def test_should_have_descriptive_error_message(self):
        """validate_report_ownership should return error with descriptive message"""
        report = ReportFactory.create(client="DEVICE-1")
        different_device_id = "DEVICE-2"

        result = validate_report_ownership(report, different_device_id)

        self.assertIn(b"Device_id mismatch", result.content)
