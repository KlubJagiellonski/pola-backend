# Create your views here.
from django.http import JsonResponse
from pola.models import Client, Product
from django.core.exceptions import ObjectDoesNotExist
from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='100/h')
def product(request, barcode):
    client_id = request.GET.get('client_id', 0)
    client, created = Client.objects.get_or_create(pk=client_id)
    response = {}
    response['client'] = client.to_dict()
    try:
        company = Product.objects.get(code=barcode).company
        response['status'] = 1
        response['data'] = company.to_dict()
    except ObjectDoesNotExist:
        response['status'] = 0

    return JsonResponse(response)
