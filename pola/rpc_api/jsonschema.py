import functools
import json
import logging

from django.http import HttpResponse, HttpResponseServerError
from jsonschema.validators import validator_for

log = logging.getLogger(__file__)


def validate_json_response(schema, *args, **kwargs):
    cls = validator_for(schema)

    cls.check_schema(schema)
    validator = cls(schema, *args, **kwargs)

    def wrapper(func):
        @functools.wraps(func)
        def validate_json_schema(*args, **kwargs):
            response: HttpResponse = func(*args, **kwargs)
            if response['Content-Type'] == 'application/json':
                errors = list(validator.iter_errors(json.loads(response.content)))
                if errors:
                    log.error("Invalid response. %d errors encountered", len(errors))
                    for error in errors:
                        log.error("%s", error)
                        print(error)
                    return HttpResponseServerError("The server generated an invalid response.")
            return response

        return validate_json_schema

    return wrapper
