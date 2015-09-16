from rest_framework.response import Response
from .serializers import ReportSerializer, AttachmentSerializer
# from ..models import Report
from rest_framework import status
from rest_framework.generics import CreateAPIView


class ReportCreate(CreateAPIView):
    serializer_class = ReportSerializer

    def __init__(self, *args, **kwargs):
        super(ReportCreate, self).__init__(*args, **kwargs)
        # import ipdb; ipdb.set_trace()

    def create(self, request, format=None):
        device_id = request.query_params.get('device_id', None)
        serializer = ReportSerializer(
            data=dict(request.data, client=device_id))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttachmentCreate(CreateAPIView):
    serializer_class = AttachmentSerializer

    def __init__(self, *args, **kwargs):
        super(AttachmentCreate, self).__init__(*args, **kwargs)
        # import ipdb; ipdb.set_trace()

    def create(self, request, format=None):
        device_id = request.query_params.get('device_id', None)
        # import ipdb; ipdb.set_trace()
        serializer = AttachmentSerializer(
            data=dict(request.data, client=device_id))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
