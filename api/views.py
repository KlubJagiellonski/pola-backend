from pola import logic
from django.http import JsonResponse
from product.models import Product
from pola.models import Query

def get_by_code(request, code):
    device_id =request.GET['device_id']

    product = Product.get_by_code(code=code)
    Query.objects.create(client=device_id, product=product)

    result = logic.serialize_product(product)

    return JsonResponse(result)

