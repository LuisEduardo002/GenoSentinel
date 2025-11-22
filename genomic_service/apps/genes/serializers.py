from rest_framework import serializers
from .models import Gene
from .dtos import GeneDTO, GeneCreateDTO, GeneUpdateDTO, GeneListDTO

class GeneSerializer(serializers.Serializer):
    """Serializer que transforma GeneDTO a/desde JSON"""
    id = serializers.UUIDField(read_only=True)
    symbol = serializers.CharField(max_length=50)
    full_name = serializers.CharField(max_length=255)
    function_summary = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """Convierte DTO a diccionario para JSON"""
        if isinstance(instance, GeneDTO):
            return {
                'id': str(instance.id),
                'symbol': instance.symbol,
                'full_name': instance.full_name,
                'function_summary': instance.function_summary,
                'created_at': instance.created_at.isoformat(),
                'updated_at': instance.updated_at.isoformat()
            }
        return super().to_representation(instance)


class GeneCreateSerializer(serializers.Serializer):
    """Serializer para crear DTOs desde JSON"""
    symbol = serializers.CharField(max_length=50, required=True)
    full_name = serializers.CharField(max_length=255, required=True)
    function_summary = serializers.CharField(required=True)
    
    def create(self, validated_data):
        """Crea un DTO desde datos validados"""
        try:
            return GeneCreateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar DTOs desde JSON"""
    full_name = serializers.CharField(max_length=255, required=False)
    function_summary = serializers.CharField(required=False)
    
    def create(self, validated_data):
        """Crea un UpdateDTO desde datos validados"""
        try:
            return GeneUpdateDTO(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class GeneListSerializer(serializers.Serializer):
    """Serializer para listado de genes"""
    id = serializers.UUIDField(read_only=True)
    symbol = serializers.CharField()
    full_name = serializers.CharField()
    variants_count = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        """Convierte GeneListDTO a diccionario"""
        if isinstance(instance, GeneListDTO):
            return {
                'id': str(instance.id),
                'symbol': instance.symbol,
                'full_name': instance.full_name,
                'variants_count': instance.variants_count
            }
        return super().to_representation(instance)