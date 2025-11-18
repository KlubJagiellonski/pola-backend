import os
from unittest import mock

import pytest
from django.test import TestCase, override_settings
from requests.exceptions import HTTPError
from vcr import VCR

from pola.integrations.produkty_w_sieci import (
    ApiException,
    ProduktyWSieciClient,
    produkty_w_sieci_client,
)

TEST_EAN13 = "5901520000059"

vcr = VCR(cassette_library_dir=os.path.join(os.path.dirname(__file__), "cassettes"))


# 🔹 Test z użyciem rzeczywistego API (v2)
@override_settings()
class TestGetProductsFromRealAPI(TestCase):
    @vcr.use_cassette("product_ean13_v2.yaml", filter_headers=["X-API-KEY"])
    def test_should_return_product(self):
        product = produkty_w_sieci_client.get_products(gtin_number=TEST_EAN13)
        assert product.gtinNumber.lstrip("0") == TEST_EAN13.lstrip("0")
        assert product.company.nip is not None


# 🔸 Testy mockowane
class TestProduktyWSieciClientMocked:
    def setup_method(self):
        self.client = ProduktyWSieciClient(api_token="FAKE-TOKEN")

    def test_should_return_none_when_not_found(self):
        mocked_resp = {"errors": [{"message": "not_found"}]}
        with mock.patch("requests.Session.request") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = mocked_resp
            mock_response.raise_for_status = mock.Mock()
            mock_request.return_value = mock_response

            result = self.client.get_products(gtin_number=TEST_EAN13, num_retries=0)
            assert result is None

    def test_should_raise_api_exception_on_custom_error(self):
        mocked_resp = {"errors": [{"message": "rate_limit_exceeded"}]}
        with mock.patch("requests.Session.request") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mocked_resp
            mock_response.raise_for_status = mock.Mock()
            mock_request.return_value = mock_response

            with pytest.raises(ApiException, match="rate_limit_exceeded"):
                self.client.get_products(gtin_number=TEST_EAN13, num_retries=0)

    def test_should_raise_key_error_on_unknown_error_structure(self):
        mocked_resp = {"errors": [{"foo": "bar"}]}
        with mock.patch("requests.Session.request") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mocked_resp
            mock_response.raise_for_status = mock.Mock()
            mock_request.return_value = mock_response

            with pytest.raises(KeyError, match="'message'"):
                self.client.get_products(gtin_number=TEST_EAN13, num_retries=0)

    def test_should_handle_empty_response_json(self):
        """Test dla odpowiedzi: pusty słownik, brak 'errors'"""
        mocked_resp = {}
        with mock.patch("requests.Session.request") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mocked_resp
            mock_response.raise_for_status = mock.Mock()
            mock_request.return_value = mock_response

            with pytest.raises(Exception):
                self.client.get_products(gtin_number=TEST_EAN13, num_retries=0)

    def test_should_handle_non_list_errors_field(self):
        """Test dla: {'errors': 'unexpected string'}"""
        mocked_resp = {"errors": "unexpected string"}
        with mock.patch("requests.Session.request") as mock_request:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mocked_resp
            mock_response.raise_for_status = mock.Mock()
            mock_request.return_value = mock_response

            with pytest.raises(ApiException, match="Unknown error response"):
                self.client.get_products(gtin_number=TEST_EAN13, num_retries=0)

    def test_should_retry_until_failure_and_raise_error(self):
        """Test, który wyczerpuje wszystkie próby i rzuca HTTPError"""
        failing_resp = mock.Mock()
        failing_resp.status_code = 500
        failing_resp.raise_for_status.side_effect = HTTPError("Server error")

        with mock.patch("requests.Session.request", return_value=failing_resp):
            with pytest.raises(HTTPError, match="Server error"):
                self.client.get_products(gtin_number=TEST_EAN13, num_retries=2)

    def test_should_retry_on_server_error_then_succeed(self):
        retry_resp = mock.Mock()
        retry_resp.status_code = 500
        retry_resp.raise_for_status.side_effect = HTTPError("Server error")

        success_resp = mock.Mock()
        success_resp.status_code = 200
        success_resp.json.return_value = {
            "gtinNumber": TEST_EAN13,
            "gtinStatus": "active",
            "name": "Mocked Product",
            "targetMarket": ["PL"],
            "netContent": ["500", "ml"],
            "description": "Mocked description",
            "descriptionLanguage": "pl",
            "imageUrls": [],
            "productPage": None,
            "isPublic": True,
            "isVerified": True,
            "lastModified": "2023-01-01T00:00:00+00:00",
            "gpc": [],
            "brand": None,
            "company": None,
        }
        success_resp.raise_for_status = mock.Mock()

        with mock.patch("requests.Session.request", side_effect=[retry_resp, success_resp]) as mock_request:
            result = self.client.get_products(gtin_number=TEST_EAN13, num_retries=1)
            assert result.gtinNumber == TEST_EAN13
            assert mock_request.call_count == 2

    def test_should_raise_http_error_on_client_error(self):
        client_error = mock.Mock()
        client_error.status_code = 404
        client_error.raise_for_status.side_effect = HTTPError("Not found")

        with mock.patch("requests.Session.request", return_value=client_error):
            with pytest.raises(HTTPError, match="Not found"):
                self.client.get_products(gtin_number="BAD-CODE", num_retries=1)
