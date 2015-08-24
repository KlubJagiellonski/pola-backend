from rest_framework.response import Response
from .serializers import ProductSerializer
from ..models import Product
from pola.models import Query
from django.http import Http404
from rest_framework.views import APIView


class ProductDetail(APIView):
    """
    Retrieve a product instance.
    """
    def get_object(self, code):
        try:
            return Product.get_by_code(code=code)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        product = self.get_object(slug)
        self.save_query(product, request)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def save_query(self, product, request):
        device_id = request.query_params.get('device_id', None)
        Query.objects.create(client=device_id, product=product)
