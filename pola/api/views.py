from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Client
from .serializers import ClientSerializer


class ObtainToken(APIView):
    """
    Retrieve a product instance.
    """
    def get_object(self):
        return Client.objects.create()

    def get(self, request, format=None):
        client = self.get_object()
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class TestCredential(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)
