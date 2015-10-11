from pola import logic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from pola.models import Query
from report.models import Report
import json

def get_by_code(request, code):
    device_id =request.GET['device_id']

    product = Product.get_by_code(code=code)
    Query.objects.create(client=device_id, product=product)

    result = logic.serialize_product(product)

    return JsonResponse(result)

@csrf_exempt
def create_report(request):
    device_id = request.GET['device_id']

    data = json.loads(request.body)
    description = data['description']
    product_id = data.get('product_id', None)

    product = None
    if product_id:
        product = Product.objects.get(pk=product_id)

    report = Report.objects.create(product=product, desciption=description, client=device_id)

    return JsonResponse({'id':report.id})

@csrf_exempt
def update_report(request):
    device_id = request.GET['device_id']

    data = json.loads(request.body)
    report_id = data['report_id']
    description = data['description']

    report = Report.objects.get(pk=report_id)
    report.desciption = description
    report.save()

    return JsonResponse({'id':report.id})
