from rest_framework import serializers
from .models import Gene


class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = [
            'id',
            'symbol',
            'full_name',
            'function_summary',
            'created_at',
            'updated_at',
        ]
