from .serializers import ProductSerializer
from ..models import Product
from pola.models import Query
from rest_framework import viewsets
from pola.logic import get_by_code


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        code = self.kwargs['pk']
        return get_by_code(code=code)

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        self.save_query(product, request)
        return super(ProductViewSet, self).retrieve(request, *args, **kwargs)

    def save_query(self, product, request):
        device_id = request.query_params.get('device_id', None)
        Query.objects.create(client=device_id, product=product)
