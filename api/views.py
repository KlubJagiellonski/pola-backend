from pola import logic
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from pola.models import Query
from report.models import Report, Attachment
import json
import os
import uuid
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='2/s', block=True)
def get_by_code(request, code):
    device_id =request.GET['device_id']

    product = logic.get_by_code(code=code)

    result = logic.serialize_product(product)

    Query.objects.create(client=device_id, product=product,
                         was_verified = result['verified'],
                         was_590 = code.startswith('590'),
                         was_plScore = result['plScore'] is not None)

    return JsonResponse(result)

@csrf_exempt
@ratelimit(key='ip', rate='2/s', block=True)
def create_report(request):
    device_id = request.GET['device_id']

    data = json.loads(request.body)
    description = data['description']
    product_id = data.get('product_id', None)

    product = None
    if product_id:
        product = Product.objects.get(pk=product_id)

    report = Report.objects.create(product=product, description=description,
                                   client=device_id)

    return JsonResponse({'id':report.id})

@csrf_exempt
@ratelimit(key='ip', rate='2/s', block=True)
def update_report(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    data = json.loads(request.body)
    description = data['description']

    report = Report.objects.get(pk=report_id)

    if report.client != device_id:
        return HttpResponseForbidden("Device_id mismatch")

    report.description = description
    report.save()

    return JsonResponse({'id':report.id})

@csrf_exempt
@ratelimit(key='ip', rate='2/s', block=True)
def attach_file(request):
    device_id = request.GET['device_id']
    report_id = request.GET['report_id']

    report = Report.objects.get(pk=report_id)

    if report.client != device_id:
        return HttpResponseForbidden("Device_id mismatch")

    attachment = Attachment(attachment=request.FILES['file'], report=report)
    file_name, file_extension = os.path.splitext(attachment.attachment.name)
    attachment.attachment.name = str(uuid.uuid1()) + file_extension
    attachment.save()

    return JsonResponse({'id':attachment.id})
