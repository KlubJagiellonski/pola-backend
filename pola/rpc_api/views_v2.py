import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from pola.report.models import Report
from pola.rpc_api.http import validate_report_ownership
from pola.rpc_api.jsonschema import validate_json_response
from pola.rpc_api.rates import whitelist
from pola.rpc_api.schemas import (
    ATTACH_FILE_V2_RESPONSE_SCHEMA,
    CREATE_REPORT_V2_RESPONSE_SCHEMA,
    GET_BY_CODE_RESPONSE_SCHEMA,
    UPDATE_REPORT_RESPONSE_SCHEMA,
)
from pola.rpc_api.views_v3 import attach_file_internal, create_report_internal
from pola.rpc_api.views_v4 import get_by_code_internal


@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(GET_BY_CODE_RESPONSE_SCHEMA)
def get_by_code_v2(request):
    result = get_by_code_internal(request)

    return JsonResponse(result)


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(CREATE_REPORT_V2_RESPONSE_SCHEMA)
def create_report_v2(request):
    return create_report_internal(request, extra_comma=True)


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(UPDATE_REPORT_RESPONSE_SCHEMA)
def update_report_v2(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    data = json.loads(request.body.decode("utf-8"))
    description = data['description']

    report = Report.objects.get(pk=report_id)

    error_response = validate_report_ownership(report, device_id)
    if error_response:
        return error_response

    report.description = description
    report.save()

    return JsonResponse({'id': report.id})


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(ATTACH_FILE_V2_RESPONSE_SCHEMA)
def attach_file_v2(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    report = Report.objects.get(pk=report_id)

    error_response = validate_report_ownership(report, device_id)
    if error_response:
        return error_response

    data = json.loads(request.body.decode("utf-8"))
    file_ext = data['file_ext']
    mime_type = data['mime_type']

    signed_request = attach_file_internal(report, file_ext, mime_type)

    return JsonResponse({'signed_request': [signed_request]})
