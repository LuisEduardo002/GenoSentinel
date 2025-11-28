from rest_framework import serializers

from .models import GeneticVariant


class GeneticVariantSerializer(serializers.ModelSerializer):
    gene_symbol = serializers.CharField(source="gene.symbol", read_only=True)

    class Meta:
        model = GeneticVariant
        fields = [
            "id",
            "gene",
            "gene_symbol",
            "chromosome",
            "position",
            "reference_base",
            "alternate_base",
            "impact",
            "created_at",
            "updated_at",
        ]
