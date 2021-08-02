from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

from pola.rpc_api.jsonschema import validate_json_response
from pola.rpc_api.rates import whitelist


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('5/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"id": {"type": "number"}},
        "required": ["id"],
    }
)
def raise_exception(request):
    del request
    return JsonResponse({'invalid': "42"})
