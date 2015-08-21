from rest_framework import serializers
from ..models import Product
from company.api.serializers import CompanySerializer


class ProductSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'code', 'company')
