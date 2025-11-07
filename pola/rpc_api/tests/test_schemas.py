from django.test import TestCase
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from pola.rpc_api.schemas import (
    ADD_AI_PICS_RESPONSE_SCHEMA,
    ATTACH_FILE_V2_RESPONSE_SCHEMA,
    CREATE_REPORT_V2_RESPONSE_SCHEMA,
    CREATE_REPORT_V3_RESPONSE_SCHEMA,
    GET_BY_CODE_RESPONSE_SCHEMA,
    UPDATE_REPORT_RESPONSE_SCHEMA,
)


class TestGetByCodeResponseSchema(TestCase):
    def test_valid_response_passes_validation(self):
        """Valid get_by_code response should pass schema validation"""
        valid_response = {
            "altText": "Test product",
            "card_type": "type1",
            "code": "1234567890123",
            "donate": {"show_button": True, "title": "Donate", "url": "http://example.com"},
            "name": "Product Name",
            "plCapital": 100,
            "plCapital_notes": "Notes",
            "plNotGlobEnt": 50,
            "plNotGlobEnt_notes": "Notes",
            "plRegistered": 100,
            "plRegistered_notes": "Notes",
            "plRnD": 75,
            "plRnD_notes": "Notes",
            "plScore": 80,
            "plWorkers": 60,
            "plWorkers_notes": "Notes",
            "product_id": 123,
            "report_button_text": "Report",
            "report_button_type": "button",
            "report_text": "Report this",
        }

        # Should not raise ValidationError
        validate(instance=valid_response, schema=GET_BY_CODE_RESPONSE_SCHEMA)

    def test_null_values_are_accepted(self):
        """Null values should be accepted for nullable fields"""
        response_with_nulls = {
            "altText": None,
            "card_type": "type1",
            "code": "1234567890123",
            "donate": {"show_button": True, "title": "Donate", "url": "http://example.com"},
            "name": "Product Name",
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
            "report_button_text": "Report",
            "report_button_type": "button",
            "report_text": "Report this",
        }

        # Should not raise ValidationError
        validate(instance=response_with_nulls, schema=GET_BY_CODE_RESPONSE_SCHEMA)

    def test_missing_required_field_fails_validation(self):
        """Missing required field should fail validation"""
        invalid_response = {
            "code": "1234567890123",
            "name": "Product Name",
            # Missing other required fields
        }

        with self.assertRaises(ValidationError):
            validate(instance=invalid_response, schema=GET_BY_CODE_RESPONSE_SCHEMA)


class TestCreateReportSchemas(TestCase):
    def test_v2_schema_requires_id_and_signed_requests(self):
        """V2 schema should require both id and signed_requests"""
        valid_v2_response = {"id": 123, "signed_requests": ["url1", "url2"]}

        validate(instance=valid_v2_response, schema=CREATE_REPORT_V2_RESPONSE_SCHEMA)

    def test_v2_schema_fails_without_id(self):
        """V2 schema should fail without id"""
        invalid_response = {"signed_requests": ["url1"]}

        with self.assertRaises(ValidationError):
            validate(instance=invalid_response, schema=CREATE_REPORT_V2_RESPONSE_SCHEMA)

    def test_v3_schema_only_requires_signed_requests(self):
        """V3 schema should only require signed_requests"""
        valid_v3_response = {"signed_requests": ["url1", "url2"]}

        validate(instance=valid_v3_response, schema=CREATE_REPORT_V3_RESPONSE_SCHEMA)

    def test_v3_schema_accepts_empty_signed_requests(self):
        """V3 schema should accept empty signed_requests array"""
        valid_response = {"signed_requests": []}

        validate(instance=valid_response, schema=CREATE_REPORT_V3_RESPONSE_SCHEMA)


class TestUpdateReportSchema(TestCase):
    def test_valid_update_report_response(self):
        """Valid update_report response should pass validation"""
        valid_response = {"id": 456}

        validate(instance=valid_response, schema=UPDATE_REPORT_RESPONSE_SCHEMA)


class TestAttachFileV2Schema(TestCase):
    def test_valid_attach_file_v2_response(self):
        """Valid attach_file v2 response should pass validation"""
        valid_response = {"signed_request": ["url1", "url2"]}

        validate(instance=valid_response, schema=ATTACH_FILE_V2_RESPONSE_SCHEMA)


class TestAddAIPicsSchema(TestCase):
    def test_valid_add_ai_pics_response(self):
        """Valid add_ai_pics response should pass validation"""
        valid_response = {"signed_requests": ["url1", "url2", "url3"]}

        validate(instance=valid_response, schema=ADD_AI_PICS_RESPONSE_SCHEMA)

    def test_empty_signed_requests_is_valid(self):
        """Empty signed_requests array should be valid"""
        valid_response = {"signed_requests": []}

        validate(instance=valid_response, schema=ADD_AI_PICS_RESPONSE_SCHEMA)
