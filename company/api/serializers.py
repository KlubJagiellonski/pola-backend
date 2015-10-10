from rest_framework import serializers
from ..models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'nip',
            'name',
            'common_name',
            'official_name',
            'address',
            'plCapital',
            'plCapital_notes',
            'plTaxes',
            'plTaxes_notes',
            'plRnD',
            'plRnD_notes',
            'plWorkers',
            'plWorkers_notes',
            'plBrand',
            'plBrand_notes',
            'verified'
            )
