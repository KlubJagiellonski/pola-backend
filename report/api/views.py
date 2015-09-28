from .serializers import ReportSerializer, AttachmentSerializer
from ..models import Report, Attachment
from rest_framework import viewsets


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        device_id = self.request.query_params.get('device_id', None)
        serializer.save(client=device_id)

    def perform_update(self, serializer):
        device_id = self.request.query_params.get('device_id', None)
        serializer.save(client=device_id)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
