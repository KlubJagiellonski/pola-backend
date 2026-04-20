import json

import pytest
from django.test import RequestFactory, override_settings

from pola.rpc_api.auth import require_static_bearer_token


@pytest.fixture()
def rf():
    return RequestFactory()


def _make_request(rf, path="/", auth_header=None):
    headers = {}
    if auth_header is not None:
        headers["HTTP_AUTHORIZATION"] = auth_header
    # Using GET is sufficient; function only inspects META
    return rf.get(path, **headers)


def _response_payload(resp):
    return json.loads(resp.content.decode("utf-8"))


@override_settings(SET_BEARER_TOKEN=None)
def test_none_token_configured_returns_none_even_with_header(rf):
    request = _make_request(rf, auth_header="Bearer anything")
    assert require_static_bearer_token(request) is None


@override_settings(SET_BEARER_TOKEN="s3cr3t")
def test_missing_authorization_header_returns_401_with_bearer_challenge(rf):
    request = _make_request(rf)
    resp = require_static_bearer_token(request)
    assert resp is not None
    assert resp.status_code == 401
    assert _response_payload(resp) == {"detail": "Unauthorized"}
    assert resp["WWW-Authenticate"] == "Bearer"


@override_settings(SET_BEARER_TOKEN="s3cr3t")
def test_non_bearer_header_returns_401_with_bearer_challenge(rf):
    request = _make_request(rf, auth_header="Basic abcdef")
    resp = require_static_bearer_token(request)
    assert resp is not None
    assert resp.status_code == 401
    assert _response_payload(resp) == {"detail": "Unauthorized"}
    assert resp["WWW-Authenticate"] == "Bearer"


@override_settings(SET_BEARER_TOKEN="s3cr3t")
def test_incorrect_bearer_token_returns_401_with_invalid_token_error(rf):
    request = _make_request(rf, auth_header="Bearer wrong")
    resp = require_static_bearer_token(request)
    assert resp is not None
    assert resp.status_code == 401
    assert _response_payload(resp) == {"detail": "Unauthorized"}
    assert resp["WWW-Authenticate"] == 'Bearer error="invalid_token"'


@override_settings(SET_BEARER_TOKEN="s3cr3t")
def test_correct_bearer_token_returns_none(rf):
    request = _make_request(rf, auth_header="Bearer s3cr3t")
    assert require_static_bearer_token(request) is None
