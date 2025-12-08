from rest_framework import serializers
from .dtos import (
    GeneticVariantDTO, GeneticVariantCreateDTO, GeneticVariantUpdateDTO,
    GeneticVariantListDTO, ImpactType, VariantsByGeneDTO, VariantsByChromosomeDTO,
    VariantStatisticsDTO
)
from enum import Enum

# --- Serializers de GeneticVariant ---

class GeneticVariantSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte GeneticVariantDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    gene_id = serializers.UUIDField(read_only=True)
    gene_symbol = serializers.CharField(read_only=True)
    gene_full_name = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(max_length=10, read_only=True)
    position = serializers.IntegerField(read_only=True)
    reference_base = serializers.CharField(max_length=100, read_only=True)
    alternate_base = serializers.CharField(max_length=100, read_only=True)
    impact = serializers.ChoiceField(choices=[(e.value, e.value) for e in ImpactType], read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance: GeneticVariantDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
            'id': str(instance.id),
            'gene_id': str(instance.gene_id),
            'gene_symbol': instance.gene_symbol,
            'gene_full_name': instance.gene_full_name,
            'chromosome': instance.chromosome,
            'position': instance.position,
            'reference_base': instance.reference_base,
            'alternate_base': instance.alternate_base,
            'impact': instance.impact.value if isinstance(instance.impact, Enum) else instance.impact,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat()
        }


class GeneticVariantCreateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a GeneticVariantCreateDTO.
    """
    gene_id = serializers.UUIDField(required=True)
    chromosome = serializers.CharField(max_length=10, required=True)
    position = serializers.IntegerField(required=True)
    reference_base = serializers.CharField(max_length=100, required=True)
    alternate_base = serializers.CharField(max_length=100, required=True)
    impact = serializers.ChoiceField(
        choices=[(e.value, e.value) for e in ImpactType],
        required=True
    )
    
    def create(self, validated_data):
        """Crea un DTO desde datos validados"""
        # Convertir el string de impacto a ImpactType Enum
        validated_data['impact'] = ImpactType(validated_data['impact'])
        try:
            return GeneticVariantCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneticVariantUpdateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a GeneticVariantUpdateDTO.
    """
    impact = serializers.ChoiceField(
        choices=[(e.value, e.value) for e in ImpactType],
        required=True
    )
    reference_base = serializers.CharField(max_length=100, required=True)
    alternate_base = serializers.CharField(max_length=100, required=True)
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        # Convertir el string de impacto a ImpactType Enum si existe
        if 'impact' in validated_data:
            validated_data['impact'] = ImpactType(validated_data['impact'])
            
        try:
            return GeneticVariantUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneticVariantListSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte GeneticVariantListDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    gene_symbol = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(read_only=True)
    position = serializers.IntegerField(read_only=True)
    mutation = serializers.CharField(read_only=True)
    impact = serializers.CharField(read_only=True)
    
    def to_representation(self, instance: GeneticVariantListDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
            'id': str(instance.id),
            'gene_symbol': instance.gene_symbol,
            'chromosome': instance.chromosome,
            'position': instance.position,
            'mutation': instance.mutation,
            'impact': instance.impact.value if isinstance(instance.impact, Enum) else instance.impact,
        }

# --- Serializers para DTOs de resultados complejos ---

class VariantsByGeneResultSerializer(serializers.Serializer):
    """Serializer para VariantsByGeneDTO"""
    gene_symbol = serializers.CharField(read_only=True)
    gene_name = serializers.CharField(read_only=True)
    total_variants = serializers.IntegerField(read_only=True)
    variants = GeneticVariantListSerializer(many=True, read_only=True)
    
    def to_representation(self, instance: VariantsByGeneDTO):
        return {
            'gene_symbol': instance.gene_symbol,
            'gene_name': instance.gene_name,
            'total_variants': instance.total_variants,
            'variants': GeneticVariantListSerializer(instance.variants, many=True).data
        }

class VariantsByChromosomeResultSerializer(serializers.Serializer):
    """Serializer para VariantsByChromosomeDTO"""
    chromosome = serializers.CharField(read_only=True)
    total_variants = serializers.IntegerField(read_only=True)
    variants = GeneticVariantListSerializer(many=True, read_only=True)
    
    def to_representation(self, instance: VariantsByChromosomeDTO):
        return {
            'chromosome': instance.chromosome,
            'total_variants': instance.total_variants,
            'variants': GeneticVariantListSerializer(instance.variants, many=True).data
        }

class VariantStatisticsResultSerializer(serializers.Serializer):
    """Serializer para VariantStatisticsDTO"""
    total_variants = serializers.IntegerField(read_only=True)
    by_impact = serializers.ListField(child=serializers.DictField(), read_only=True)
    top_chromosomes = serializers.ListField(child=serializers.DictField(), read_only=True)
    
    def to_representation(self, instance: VariantStatisticsDTO):
        return {
            'total_variants': instance.total_variants,
            'by_impact': instance.by_impact,
            'top_chromosomes': instance.top_chromosomes
        }
