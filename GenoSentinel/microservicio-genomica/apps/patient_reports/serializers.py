from rest_framework import serializers

from .models import PatientVariantReport


class PatientVariantReportSerializer(serializers.ModelSerializer):
    variant_id = serializers.UUIDField(source="variant.id", read_only=True)
    gene_symbol = serializers.CharField(source="variant.gene.symbol", read_only=True)

    class Meta:
        model = PatientVariantReport
        fields = [
            "id",
            "patient_id",
            "variant",
            "variant_id",
            "gene_symbol",
            "detection_date",
            "allele_frequency",
            "created_at",
            "updated_at",
        ]
