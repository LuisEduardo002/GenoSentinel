from rest_framework import serializers
from .dtos import (
    GeneDTO, GeneCreateDTO, GeneUpdateDTO, GeneListDTO, 
    GeneSearchResultDTO, GeneStatisticsDTO
)

# --- Serializers de Gene ---

class GeneSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte GeneDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    symbol = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    function_summary = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance: GeneDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
            'id': str(instance.id),
            'symbol': instance.symbol,
            'full_name': instance.full_name,
            'function_summary': instance.function_summary,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat()
        }


class GeneCreateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a GeneCreateDTO.
    """
    symbol = serializers.CharField(max_length=50, required=True)
    full_name = serializers.CharField(max_length=255, required=True)
    function_summary = serializers.CharField(required=True)
    
    def create(self, validated_data):
        """Crea un DTO desde datos validados"""
        # La validación de unicidad se mueve al Service
        try:
            return GeneCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneUpdateSerializer(serializers.Serializer):
    """
    Serializer de Entrada (Input Adapter): Valida JSON y lo convierte a GeneUpdateDTO.
    """
    full_name = serializers.CharField(max_length=255, required=False)
    function_summary = serializers.CharField(required=False)
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        try:
            return GeneUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneListSerializer(serializers.Serializer):
    """
    Serializer de Salida (Output Adapter): Convierte GeneListDTO a JSON.
    """
    id = serializers.UUIDField(read_only=True)
    symbol = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    variants_count = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance: GeneListDTO):
        """Convierte DTO a diccionario para JSON"""
        return {
            'id': str(instance.id),
            'symbol': instance.symbol,
            'full_name': instance.full_name,
            'variants_count': instance.variants_count,
        }

class GeneSearchResultSerializer(serializers.Serializer):
    """Serializer para GeneSearchResultDTO"""
    query = serializers.CharField(read_only=True)
    count = serializers.IntegerField(read_only=True)
    results = GeneListSerializer(many=True, read_only=True)
    
    def to_representation(self, instance: GeneSearchResultDTO):
        return {
            'query': instance.query,
            'count': instance.count,
            'results': GeneListSerializer(instance.results, many=True).data
        }

class GeneStatisticsSerializer(serializers.Serializer):
    """Serializer para GeneStatisticsDTO"""
    total_genes = serializers.IntegerField(read_only=True)
    genes_with_variants = serializers.IntegerField(read_only=True)
    genes_without_variants = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance: GeneStatisticsDTO):
        return {
            'total_genes': instance.total_genes,
            'genes_with_variants': instance.genes_with_variants,
            'genes_without_variants': instance.genes_without_variants
        }
