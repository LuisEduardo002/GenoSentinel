from rest_framework import serializers
from decimal import Decimal
from .dtos import (
    PatientVariantReportDTO, PatientVariantReportCreateDTO,
    PatientVariantReportUpdateDTO, PatientVariantReportListDTO
)

class PatientVariantReportSerializer(serializers.Serializer):
    """Serializer que transforma PatientVariantReportDTO a/desde JSON"""
    id = serializers.UUIDField(read_only=True)
    patient_id = serializers.UUIDField()
    variant_id = serializers.UUIDField()
    gene_symbol = serializers.CharField(read_only=True)
    gene_full_name = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(read_only=True)
    position = serializers.IntegerField(read_only=True)
    reference_base = serializers.CharField(read_only=True)
    alternate_base = serializers.CharField(read_only=True)
    impact = serializers.CharField(read_only=True)
    detection_date = serializers.DateField()
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    clinical_data = serializers.DictField(read_only=True)
    
    def to_representation(self, instance):
        """Convierte DTO a diccionario para JSON"""
        if isinstance(instance, PatientVariantReportDTO):
            result = {
                'id': str(instance.id),
                'patient_id': str(instance.patient_id),
                'variant_id': str(instance.variant_id),
                'gene_symbol': instance.gene_symbol,
                'gene_full_name': instance.gene_full_name,
                'chromosome': instance.chromosome,
                'position': instance.position,
                'reference_base': instance.reference_base,
                'alternate_base': instance.alternate_base,
                'impact': instance.impact,
                'detection_date': instance.detection_date.isoformat(),
                'allele_frequency': str(instance.allele_frequency),
                'created_at': instance.created_at.isoformat(),
                'updated_at': instance.updated_at.isoformat()
            }
            
            if instance.clinical_data:
                result['clinical_data'] = {
                    'patient_id': str(instance.clinical_data.patient_id),
                    'first_name': instance.clinical_data.first_name,
                    'last_name': instance.clinical_data.last_name,
                    'birth_date': instance.clinical_data.birth_date.isoformat() if instance.clinical_data.birth_date else None,
                    'gender': instance.clinical_data.gender,
                    'status': instance.clinical_data.status,
                    'integration_status': instance.clinical_data.integration_status,
                    'message': instance.clinical_data.message
                }
            
            return result
        return super().to_representation(instance)


class PatientVariantReportCreateSerializer(serializers.Serializer):
    """Serializer para crear DTOs desde JSON"""
    patient_id = serializers.UUIDField(required=True)
    variant_id = serializers.UUIDField(required=True)
    detection_date = serializers.DateField(required=True)
    allele_frequency = serializers.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        required=True
    )
    
    def create(self, validated_data):
        """Crea un DTO desde datos validados"""
        try:
            return PatientVariantReportCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class PatientVariantReportUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar DTOs desde JSON"""
    detection_date = serializers.DateField(required=False)
    allele_frequency = serializers.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        required=False
    )
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        try:
            return PatientVariantReportUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class PatientVariantReportListSerializer(serializers.Serializer):
    """Serializer para listado de reportes"""
    id = serializers.UUIDField()
    patient_id = serializers.UUIDField()
    gene_symbol = serializers.CharField()
    chromosome = serializers.CharField()
    impact = serializers.CharField()
    detection_date = serializers.DateField()
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4)
    
    def to_representation(self, instance):
        """Convierte PatientVariantReportListDTO a diccionario"""
        if isinstance(instance, PatientVariantReportListDTO):
            return {
                'id': str(instance.id),
                'patient_id': str(instance.patient_id),
                'gene_symbol': instance.gene_symbol,
                'chromosome': instance.chromosome,
                'impact': instance.impact,
                'detection_date': instance.detection_date.isoformat(),
                'allele_frequency': str(instance.allele_frequency)
            }
        return super().to_representation(instance)