from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer
from ..models import Product
from django.http import Http404
from rest_framework.views import APIView


class ProductDetail(APIView):
    permission_classes = (IsAuthenticated,)
    """
    Retrieve a product instance.
    """
    def get_object(self, code):
        try:
            return Product.get_by_code(code=code)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        snippet = self.get_object(slug)
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)
