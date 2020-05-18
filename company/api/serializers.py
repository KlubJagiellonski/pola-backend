from rest_framework import serializers

from ..models import Company


class CompanySerializer(serializers.ModelSerializer):
    string_representation = serializers.CharField(
        source="__unicode__", read_only=True)

    class Meta:
        model = Company
        fields = (
            'string_representation',
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
