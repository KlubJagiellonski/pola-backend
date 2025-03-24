import warnings
from collections.abc import Iterable

import sentry_sdk
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse, JsonResponse
from openapi_core import OpenAPI
from openapi_core.contrib.django.handlers import (
    DjangoOpenAPIErrorsHandler,
    DjangoOpenAPIValidRequestHandler,
)
from openapi_core.contrib.django.integrations import DjangoIntegration
from openapi_core.contrib.django.middlewares import DjangoOpenAPIMiddleware, DjangoOpenAPIViewDecorator
from openapi_core.validation.schemas.exceptions import InvalidSchemaValue

from pola.rpc_api.http import JsonProblemResponse


class PolaDjangoOpenAPIErrorsHandler(DjangoOpenAPIErrorsHandler):

    def __call__(
        self,
        errors: Iterable[Exception],
    ) -> JsonResponse:
        errors = list(errors)
        for error in errors:
            sentry_sdk.capture_exception(error)
        if len(errors) == 1 and isinstance(errors[0], InvalidSchemaValue):
            error = errors[0]
            openapi_error = self.format_openapi_error(error)
            return JsonProblemResponse(
                status=openapi_error['status'],
                title="OpenAPI Spec validation failed",
                detail=f"Value {error.value} not valid for schema of type {error.type}",
                context_data={'schema_errors': [str(e) for e in error.schema_errors]},
                type=str(type(error)),
            )

        data_errors = [self.format_openapi_error(err) for err in errors]

        data_error_max = max(data_errors, key=self.get_error_status)
        return JsonProblemResponse(
            title="OpenAPI Spec validation failed",
            detail=f"{len(errors)} errors encountered",
            context_data={'errors': [e['title'] for e in data_errors]},
            status=data_error_max['status'],
        )


# For now, it is unused. It is here for future reference.
class PolaDjangoOpenAPIMiddleware(DjangoOpenAPIMiddleware):
    errors_handler = PolaDjangoOpenAPIErrorsHandler()


# Build a single decorator object for the entire application.
openapi_decorator = DjangoOpenAPIViewDecorator(
    errors_handler_cls=PolaDjangoOpenAPIErrorsHandler
)

# For backward compatibility
validate_pola_openapi_spec = openapi_decorator
