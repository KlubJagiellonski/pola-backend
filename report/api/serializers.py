from rest_framework import serializers
from ..models import Report, Attachment
from product.models import Product


class AttachmentSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField()

    class Meta:
        model = Attachment
        fields = ('report', 'attachment', )


class ReportSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False, read_only=False)
    device_id = serializers.CharField(source='client')
    # attachments = ReportAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'product',
            'device_id',
            'desciption',
            'product')
