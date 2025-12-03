from rest_framework import serializers
from uuid import UUID
from datetime import date
from decimal import Decimal

from .dtos import (
    PatientVariantReportDTO, PatientVariantReportCreateDTO, PatientVariantReportUpdateDTO,
    PatientVariantReportListDTO, PatientClinicalDataDTO, PatientReportsSummaryDTO,
    PatientStatisticsDTO, GeneralReportStatisticsDTO
)

# --- Serializers de DTOs ---

class PatientClinicalDataSerializer(serializers.Serializer):
    """Serializer para PatientClinicalDataDTO (Datos clínicos del paciente)"""
    patient_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(read_only=True, allow_null=True)
    last_name = serializers.CharField(read_only=True, allow_null=True)
    birth_date = serializers.DateField(read_only=True, allow_null=True)
    gender = serializers.CharField(read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True, allow_null=True)
    integration_status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True, allow_null=True)
    
    def to_representation(self, instance: PatientClinicalDataDTO):
        return {
            'patient_id': str(instance.patient_id),
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'birth_date': instance.birth_date.isoformat() if instance.birth_date else None,
            'gender': instance.gender,
            'status': instance.status,
            'integration_status': instance.integration_status,
            'message': instance.message
        }


class PatientVariantReportSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte PatientVariantReportDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    patient_id = serializers.UUIDField(read_only=True)
    variant_id = serializers.UUIDField(read_only=True)
    gene_symbol = serializers.CharField(read_only=True)
    gene_full_name = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(read_only=True)
    position = serializers.IntegerField(read_only=True)
    reference_base = serializers.CharField(read_only=True)
    alternate_base = serializers.CharField(read_only=True)
    impact = serializers.CharField(read_only=True)
    detection_date = serializers.DateField(read_only=True)
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    clinical_data = PatientClinicalDataSerializer(read_only=True)
    
    def to_representation(self, instance: PatientVariantReportDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
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
            'updated_at': instance.updated_at.isoformat(),
            'clinical_data': PatientClinicalDataSerializer(instance.clinical_data).data
        }


class PatientVariantReportCreateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a PatientVariantReportCreateDTO.
    """
    patient_id = serializers.UUIDField(required=True)
    variant_id = serializers.UUIDField(required=True)
    detection_date = serializers.DateField(required=True)
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4, required=True)
    
    def validate_allele_frequency(self, value):
        if value < Decimal('0') or value > Decimal('1'):
            raise serializers.ValidationError("La frecuencia alélica (VAF) debe estar entre 0 y 1.")
        return value
    
    def validate_detection_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de detección no puede ser futura.")
        return value
    
    def create(self, validated_data):
        """Crea un DTO desde datos validados"""
        try:
            return PatientVariantReportCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class PatientVariantReportUpdateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a PatientVariantReportUpdateDTO.
    """
    detection_date = serializers.DateField(required=False)
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4, required=False)
    
    def validate_allele_frequency(self, value):
        if value is not None and (value < Decimal('0') or value > Decimal('1')):
            raise serializers.ValidationError("La frecuencia alélica (VAF) debe estar entre 0 y 1.")
        return value
    
    def validate_detection_date(self, value):
        if value is not None and value > date.today():
            raise serializers.ValidationError("La fecha de detección no puede ser futura.")
        return value
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        try:
            return PatientVariantReportUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class PatientVariantReportListSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte PatientVariantReportListDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    patient_id = serializers.UUIDField(read_only=True)
    gene_symbol = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(read_only=True)
    impact = serializers.CharField(read_only=True)
    detection_date = serializers.DateField(read_only=True)
    allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4, read_only=True)
    
    def to_representation(self, instance: PatientVariantReportListDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
            'id': str(instance.id),
            'patient_id': str(instance.patient_id),
            'gene_symbol': instance.gene_symbol,
            'chromosome': instance.chromosome,
            'impact': instance.impact,
            'detection_date': instance.detection_date.isoformat(),
            'allele_frequency': str(instance.allele_frequency)
        }

# --- Serializers para DTOs de resultados complejos ---

class PatientReportsSummarySerializer(serializers.Serializer):
    """Serializer para PatientReportsSummaryDTO"""
    patient_id = serializers.UUIDField(read_only=True)
    total_variants = serializers.IntegerField(read_only=True)
    clinical_summary = PatientClinicalDataSerializer(read_only=True)
    reports = PatientVariantReportListSerializer(many=True, read_only=True)
    
    def to_representation(self, instance: PatientReportsSummaryDTO):
        return {
            'patient_id': str(instance.patient_id),
            'total_variants': instance.total_variants,
            'clinical_summary': PatientClinicalDataSerializer(instance.clinical_summary).data,
            'reports': PatientVariantReportListSerializer(instance.reports, many=True).data
        }

class PatientStatisticsSerializer(serializers.Serializer):
    """Serializer para PatientStatisticsDTO"""
    patient_id = serializers.UUIDField(read_only=True)
    total_variants = serializers.IntegerField(read_only=True)
    average_allele_frequency = serializers.DecimalField(max_digits=5, decimal_places=4, read_only=True, allow_null=True)
    variants_by_impact = serializers.ListField(child=serializers.DictField(), read_only=True)
    top_affected_genes = serializers.ListField(child=serializers.DictField(), read_only=True)
    
    def to_representation(self, instance: PatientStatisticsDTO):
        return {
            'patient_id': str(instance.patient_id),
            'total_variants': instance.total_variants,
            'average_allele_frequency': str(instance.average_allele_frequency) if instance.average_allele_frequency else None,
            'variants_by_impact': instance.variants_by_impact,
            'top_affected_genes': instance.top_affected_genes
        }

class GeneralReportStatisticsSerializer(serializers.Serializer):
    """Serializer para GeneralReportStatisticsDTO"""
    total_reports = serializers.IntegerField(read_only=True)
    total_patients_with_reports = serializers.IntegerField(read_only=True)
    average_variants_per_patient = serializers.FloatField(read_only=True)
    
    def to_representation(self, instance: GeneralReportStatisticsDTO):
        return {
            'total_reports': instance.total_reports,
            'total_patients_with_reports': instance.total_patients_with_reports,
            'average_variants_per_patient': instance.average_variants_per_patient
        }
