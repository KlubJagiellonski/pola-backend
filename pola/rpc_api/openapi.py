import functools
from pathlib import Path

from django.http import HttpRequest, HttpResponse
from openapi_core import create_spec
from openapi_core.contrib.django import (
    DjangoOpenAPIRequest,
    DjangoOpenAPIResponse,
)
from openapi_core.spec.paths import SpecPath
from openapi_core.unmarshalling.schemas.exceptions import InvalidSchemaValue
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from sentry_sdk import capture_exception
from yaml import safe_load as yaml_load

from pola.rpc_api.http import JsonProblemResponse

SPEC_FILE = Path(__file__).resolve().parent / "openapi-v1.yaml"


def validate_openapi_spec(spec: SpecPath):
    def wrapper(func):
        @functools.wraps(func)
        def validate_json_schema(django_request: HttpRequest):
            openapi_request = DjangoOpenAPIRequest(django_request)
            validator = RequestValidator(spec)
            result = validator.validate(openapi_request)
            if result.errors:
                return JsonProblemResponse(
                    status=400,
                    title="Request validation failed",
                    detail=f"{len(result.errors)} errors encountered",
                    context_data={'errors': [str(e) for e in result.errors]},
                )

            django_response: HttpResponse = func(request=django_request)
            openapi_response = DjangoOpenAPIResponse(django_response)
            validator = ResponseValidator(spec)
            result = validator.validate(openapi_request, openapi_response)
            if result.errors:
                for error in result.errors:
                    capture_exception(error)
                if len(result.errors) == 1 and isinstance(result.errors[0], InvalidSchemaValue):
                    error: InvalidSchemaValue = result.errors[0]
                    return JsonProblemResponse(
                        title="Response schema validation failed",
                        detail=f"Value {error.value} not valid for schema of type {error.type}",
                        context_data={'schema_errors': [str(e) for e in error.schema_errors]},
                    )
                else:
                    return JsonProblemResponse(
                        title="Response validation failed",
                        detail=f"{len(result.errors)} errors encountered",
                        context_data={'errors': [str(e) for e in result.errors]},
                    )

            return django_response

        return validate_json_schema

    return wrapper


def create_pola_openapi_spec_validator():
    with open(SPEC_FILE) as spec_file:
        spec_dict = yaml_load(spec_file)

    spec = create_spec(spec_dict)
    return validate_openapi_spec(spec)


validate_pola_openapi_spec = create_pola_openapi_spec_validator()
