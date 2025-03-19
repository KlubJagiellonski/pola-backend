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
from openapi_core.contrib.django.middlewares import DjangoOpenAPIMiddleware
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


def get_openapi_instance() -> OpenAPI:
    """
    Retrieves or initializes the OpenAPI instance based on Django settings
    (either OPENAPI or OPENAPI_SPEC).
    This function ensures the spec is only loaded once.
    """
    if hasattr(settings, "OPENAPI"):
        # Recommended (newer) approach
        return settings.OPENAPI
    elif hasattr(settings, "OPENAPI_SPEC"):
        # Backward compatibility
        warnings.warn(
            "OPENAPI_SPEC is deprecated. Use OPENAPI in your settings instead.",
            DeprecationWarning,
        )
        return OpenAPI(settings.OPENAPI_SPEC)
    else:
        raise ImproperlyConfigured("Neither OPENAPI nor OPENAPI_SPEC is defined in Django settings.")


class DjangoOpenAPIDecorator(DjangoIntegration):
    """
    A decorator-class that inherits from DjangoIntegration (openapi-core).
    It takes an OpenAPI object during initialization to avoid multiple
    instantiations of the same spec.

    Unfortunately, the openapi-core library does not provide a decorator out of the box
    and decorator_from_middleware is only available with the old style of Django 1.9 middlewares.
    """

    valid_request_handler_cls = DjangoOpenAPIValidRequestHandler
    errors_handler = PolaDjangoOpenAPIErrorsHandler()

    def __init__(self, openapi: OpenAPI):
        super().__init__(openapi)

        # If OPENAPI_RESPONSE_CLS is defined in settings.py (for custom response classes),
        # set the response_cls accordingly.
        if hasattr(settings, "OPENAPI_RESPONSE_CLS"):
            self.response_cls = settings.OPENAPI_RESPONSE_CLS

    def __call__(self, view_func):
        """
        Thanks to this method, the class acts as a decorator.
        Example usage:

            @openapi_decorator
            def my_view(request): ...

        """

        def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            # get_response is the function that openapi-core treats
            # as the "next step" in the chain (i.e., our original view).
            def get_response(r: HttpRequest) -> HttpResponse:
                return view_func(r, *args, **kwargs)

            # Create a handler that will validate the request.
            valid_request_handler = self.valid_request_handler_cls(request, get_response)

            # Validate the request (before running the view).
            response = self.handle_request(request, valid_request_handler, self.errors_handler)

            # Validate the response (after the view) if should_validate_response() returns True.
            return self.handle_response(request, response, self.errors_handler)

        return _wrapped_view


# 1) Load or create a single OpenAPI instance. This will only happen once.
openapi_instance = get_openapi_instance()

# 2) Build a single decorator object for the entire application.
openapi_decorator = DjangoOpenAPIDecorator(openapi_instance)

# For backward compatibility
validate_pola_openapi_spec = openapi_decorator
