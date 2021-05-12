import functools
import json
import logging
import uuid
from datetime import timedelta

import boto3
from botocore.config import Config
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from jsonschema.validators import validator_for
from ratelimit.decorators import ratelimit

from ai_pics.models import AIAttachment, AIPics
from pola import logic, logic_ai
from pola.models import Query
from pola.rpc_api.rates import whitelist
from product.models import Product
from report.models import Attachment, Report

MAX_RECORDS = 5000

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


# API v4
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
            "companies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
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
                    },
                    "required": [
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
                    ],
                },
            },
            "product_id": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
            "report": {
                "type": "object",
                "properties": {
                    "button_text": {"type": "string"},
                    "button_type": {"type": "string"},
                    "text": {"type": "string"},
                },
            },
        },
        "required": [
            "altText",
            "card_type",
            "code",
            "name",
            "donate",
            "product_id",
        ],
    }
)
def get_by_code_v4(request):
    noai = request.GET.get('noai')
    result = get_by_code_internal(
        request, ai_supported=noai is None, multiple_company_supported=True, report_as_object=True
    )

    response = JsonResponse(result)
    response["Access-Control-Allow-Origin"] = "*"

    return response


# API v3
@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"signed_requests": {"type": "array", "items": {"type": "string"}}},
        "required": ["signed_requests"],
    }
)
def add_ai_pics(request):
    device_id = request.GET['device_id']

    data = json.loads(request.body.decode("utf-8"))
    product_id = data.get('product_id')
    files_count = data['files_count']
    file_ext = data['file_ext']
    mime_type = data['mime_type']

    original_width = data['original_width']
    original_height = data['original_height']

    width = data['width']
    height = data['height']

    device_name = data['device_name']
    flash_used = data.get('flash_used', None)
    was_portrait = data.get('was_portrait', None)

    product = Product.objects.get(pk=product_id)

    ai_pics = AIPics.objects.create(
        product=product,
        client=device_id,
        original_width=original_width,
        original_height=original_height,
        width=width,
        height=height,
        device_name=device_name,
        flash_used=flash_used,
        was_portrait=was_portrait,
    )

    signed_requests = []
    if files_count and file_ext and mime_type:
        if files_count > 24:
            return HttpResponseForbidden("files_count can be between 0 and 24")

        for i in range(0, files_count):
            signed_request = attach_pic_internal(ai_pics, i, file_ext, mime_type)
            signed_requests.append(signed_request)

    product.increment_ai_pics_count()

    return JsonResponse({'signed_requests': signed_requests})


def attach_pic_internal(ai_pics, file_no, file_ext, mime_type):
    object_name = '{}/{}_{}_{}.{}'.format(
        str(ai_pics.product.code), str(ai_pics.id), str(file_no), str(uuid.uuid1()), file_ext
    )

    signed_request = create_signed_request_boto3(mime_type, object_name, settings.AWS_STORAGE_BUCKET_AI_NAME)

    attachment = AIAttachment(ai_pics=ai_pics)
    attachment.attachment.name = object_name
    attachment.file_no = file_no
    attachment.save()

    return signed_request


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
def get_by_code_v3(request):
    noai = request.GET.get('noai')
    result = get_by_code_internal(request, ai_supported=noai is None)

    response = JsonResponse(result)
    response["Access-Control-Allow-Origin"] = "*"

    return response


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_json_response(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"signed_requests": {"type": "array", "items": {"type": "string"}}},
        "required": ["signed_requests"],
    }
)
def create_report_v3(request):
    return create_report_internal(request)


# API v2


def get_by_code_internal(request, ai_supported=False, multiple_company_supported=False, report_as_object=False):
    code = request.GET['code']
    device_id = request.GET['device_id']

    result, stats, product = logic.get_result_from_code(
        code, multiple_company_supported=multiple_company_supported, report_as_object=report_as_object
    )

    if product is not None:
        Query.objects.create(
            client=device_id,
            product=product,
            was_verified=stats['was_verified'],
            was_590=stats['was_590'],
            was_plScore=stats['was_plScore'],
        )

    if product:
        product.increment_query_count()
        companies = list(product.companies.all())
        if companies:
            for company in companies:
                company.increment_query_count()

    if ai_supported:
        result = logic_ai.add_ask_for_pics(product, result)

    result["donate"] = {
        "show_button": True,
        "url": "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
        "title": "Potrzebujemy 1 zł",
    }
    return result


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


def create_report_internal(request, extra_comma=False):
    device_id = request.GET['device_id']

    data = json.loads(request.body.decode("utf-8"))
    description = data['description']
    product_id = data.get('product_id', None)
    files_count = data.get('files_count', None)
    file_ext = data.get('file_ext', None)
    mime_type = data.get('mime_type', None)

    product = None
    if product_id:
        product = Product.objects.get(pk=product_id)

    report = Report.objects.create(product=product, description=description, client=device_id)

    signed_requests = []
    if files_count and file_ext and mime_type:
        if files_count > 10:
            return HttpResponseForbidden("files_count can be between 0 and 10")

        for _ in range(0, files_count):
            signed_request = attach_file_internal(report, file_ext, mime_type)
            signed_requests.append(signed_request)

    return JsonResponse({'id': report.id, 'signed_requests': signed_requests})


def attach_file_internal(report, file_ext, mime_type):
    object_name = f'{str(report.id)}/{str(uuid.uuid1())}.{file_ext}'

    signed_request = create_signed_request_boto3(mime_type, object_name, settings.AWS_STORAGE_BUCKET_NAME)

    attachment = Attachment(report=report)
    attachment.attachment.name = object_name
    attachment.save()

    return signed_request


def create_signed_request_boto3(mime_type, object_name, bucket_name):
    expires = int(timedelta(days=1).total_seconds())
    client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-2',
    )
    response = client.generate_presigned_url(
        'put_object',
        Params=dict(Bucket=bucket_name, Key=object_name, ACL='public-read', ContentType=mime_type),
        ExpiresIn=expires,
    )
    return response


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


# Debug stuff
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
