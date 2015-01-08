import json

from django.core import serializers
from django.http import HttpResponse


def create_json_http_response(list):
    return HttpResponse(json.dumps(json_with_success(list)), content_type="application/json")


def json_with_success(result):
    return {
        "success": True,
        "result": result
    }


def correct_nip(nip):
    nip = nip.strip().replace(" ", "").replace("-", "")
    if len(nip) == 10:
        nip = 'PL' + nip
    return nip