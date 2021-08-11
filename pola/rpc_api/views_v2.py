import json

from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

from pola.rpc_api.jsonschema import validate_json_response
from pola.rpc_api.rates import whitelist
from pola.rpc_api.views_v3 import attach_file_internal, create_report_internal
from pola.rpc_api.views_v4 import get_by_code_internal
from report.models import Report


@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "altText": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "card_type": {"type": "string"},
            "code": {"type": "string"},
            "donate": {
                "type": "object",
                "properties": {
                    "show_button": {"type": "boolean"},
                    "title": {"type": "string"},
                    "url": {"type": "string"},
                },
                "required": ["show_button", "title", "url"],
            },
            "name": {"type": "string"},
            "plCapital": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plCapital_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "plNotGlobEnt": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plNotGlobEnt_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "plRegistered": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plRegistered_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "plRnD": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plRnD_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "plScore": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plWorkers": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "plWorkers_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
            "product_id": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "report_button_text": {"type": "string"},
            "report_button_type": {"type": "string"},
            "report_text": {"type": "string"},
        },
        "required": [
            "altText",
            "card_type",
            "code",
            "donate",
            "name",
            "plCapital",
            "plCapital_notes",
            "plNotGlobEnt",
            "plNotGlobEnt_notes",
            "plRegistered",
            "plRegistered_notes",
            "plRnD",
            "plRnD_notes",
            "plScore",
            "plWorkers",
            "plWorkers_notes",
            "product_id",
            "report_button_text",
            "report_button_type",
            "report_text",
        ],
    }
)
def get_by_code_v2(request):
    result = get_by_code_internal(request)

    return JsonResponse(result)


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"id": {"type": "integer"}, "signed_requests": {"type": "array", "items": {"type": "string"}}},
        "required": ["id", "signed_requests"],
    }
)
def create_report_v2(request):
    return create_report_internal(request, extra_comma=True)


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"id": {"type": "integer"}},
        "required": ["id"],
    }
)
def update_report_v2(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    data = json.loads(request.body.decode("utf-8"))
    description = data['description']

    report = Report.objects.get(pk=report_id)

    if report.client != device_id:
        return HttpResponseForbidden("Device_id mismatch")

    report.description = description
    report.save()

    return JsonResponse({'id': report.id})


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"signed_request": {"type": "array", "items": {"type": "string"}}},
        "required": ["signed_request"],
    }
)
def attach_file_v2(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    report = Report.objects.get(pk=report_id)

    if report.client != device_id:
        return HttpResponseForbidden("Device_id mismatch")

    data = json.loads(request.body.decode("utf-8"))
    file_ext = data['file_ext']
    mime_type = data['mime_type']

    signed_request = attach_file_internal(report, file_ext, mime_type)

    return JsonResponse({'signed_request': [signed_request]})
