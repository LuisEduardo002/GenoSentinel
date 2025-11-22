from rest_framework import serializers
from .dtos import (
    GeneticVariantDTO, GeneticVariantCreateDTO, GeneticVariantUpdateDTO,
    GeneticVariantListDTO, ImpactType
)

class GeneticVariantSerializer(serializers.Serializer):
    """Serializer que transforma GeneticVariantDTO a/desde JSON"""
    id = serializers.UUIDField(read_only=True)
    gene_id = serializers.UUIDField()
    gene_symbol = serializers.CharField(read_only=True)
    gene_full_name = serializers.CharField(read_only=True)
    chromosome = serializers.CharField(max_length=10)
    position = serializers.IntegerField()
    reference_base = serializers.CharField(max_length=100)
    alternate_base = serializers.CharField(max_length=100)
    impact = serializers.ChoiceField(choices=[(e.value, e.value) for e in ImpactType])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """Convierte DTO a diccionario para JSON"""
        if isinstance(instance, GeneticVariantDTO):
            return {
                'id': str(instance.id),
                'gene_id': str(instance.gene_id),
                'gene_symbol': instance.gene_symbol,
                'gene_full_name': instance.gene_full_name,
                'chromosome': instance.chromosome,
                'position': instance.position,
                'reference_base': instance.reference_base,
                'alternate_base': instance.alternate_base,
                'impact': instance.impact,
                'created_at': instance.created_at.isoformat(),
                'updated_at': instance.updated_at.isoformat()
            }
        return super().to_representation(instance)


class GeneticVariantCreateSerializer(serializers.Serializer):
    """Serializer para crear DTOs desde JSON"""
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
        try:
            return GeneticVariantCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneticVariantUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar DTOs desde JSON"""
    impact = serializers.ChoiceField(
        choices=[(e.value, e.value) for e in ImpactType],
        required=False
    )
    reference_base = serializers.CharField(max_length=100, required=False)
    alternate_base = serializers.CharField(max_length=100, required=False)
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        try:
            return GeneticVariantUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneticVariantListSerializer(serializers.Serializer):
    """Serializer para listado de variantes"""
    id = serializers.UUIDField()
    gene_symbol = serializers.CharField()
    chromosome = serializers.CharField()
    position = serializers.IntegerField()
    mutation = serializers.CharField()
    impact = serializers.CharField()
    
    def to_representation(self, instance):
        """Convierte GeneticVariantListDTO a diccionario"""
        if isinstance(instance, GeneticVariantListDTO):
            return {
                'id': str(instance.id),
                'gene_symbol': instance.gene_symbol,
                'chromosome': instance.chromosome,
                'position': instance.position,
                'mutation': instance.mutation,
                'impact': instance.impact
            }
        return super().to_representation(instance)