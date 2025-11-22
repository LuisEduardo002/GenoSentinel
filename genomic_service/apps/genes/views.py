from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Gene
from .dtos import (
    GeneDTO, GeneCreateDTO, GeneUpdateDTO, GeneListDTO,
    GeneSearchResultDTO, GeneStatisticsDTO, GeneMapper
)
from .serializers import (
    GeneSerializer, GeneCreateSerializer, GeneUpdateSerializer, GeneListSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los genes",
        description="Obtiene el listado completo de genes de interés oncológico",
        tags=['Genes']
    ),
    create=extend_schema(
        summary="Crear un nuevo gen",
        description="Registra un nuevo gen de interés oncológico en el catálogo",
        tags=['Genes']
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de un gen",
        description="Obtiene información detallada de un gen específico por su ID",
        tags=['Genes']
    ),
    update=extend_schema(
        summary="Actualizar un gen completamente",
        description="Actualiza todos los campos de un gen existente",
        tags=['Genes']
    ),
    partial_update=extend_schema(
        summary="Actualizar un gen parcialmente",
        description="Actualiza uno o más campos de un gen existente",
        tags=['Genes']
    ),
    destroy=extend_schema(
        summary="Eliminar un gen",
        description="Elimina un gen del catálogo (solo si no tiene variantes asociadas)",
        tags=['Genes']
    )
)
class GeneViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión completa de Genes de Interés Oncológico
    Usa DTOs para transferencia de datos
    """
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'create':
            return GeneCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GeneUpdateSerializer
        elif self.action == 'list':
            return GeneListSerializer
        return GeneSerializer
    
    def list(self, request):
        """Lista todos los genes con conteo de variantes"""
        # Obtener genes desde la BD
        genes = Gene.objects.annotate(variants_count=Count('variants')).all()
        
        # Filtro por símbolo
        symbol = request.query_params.get('symbol', None)
        if symbol:
            genes = genes.filter(symbol__icontains=symbol)
        
        # Convertir Models a DTOs
        gene_dtos = [
            GeneMapper.to_list_dto(gene, gene.variants_count) 
            for gene in genes
        ]
        
        # Serializar DTOs a JSON
        serializer = GeneListSerializer(gene_dtos, many=True)
        
        return Response({
            'count': len(gene_dtos),
            'results': serializer.data
        })
    
    def create(self, request):
        """Crea un nuevo gen"""
        # Validar y deserializar JSON a DTO
        serializer = GeneCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Crear DTO
            gene_dto = serializer.save()
            
            # Convertir DTO a Model
            gene = GeneMapper.to_model(gene_dto)
            
            # Guardar en BD
            gene.save()
            
            # Convertir Model guardado a DTO completo
            result_dto = GeneMapper.to_dto(gene)
            
            # Serializar DTO a JSON
            result_serializer = GeneSerializer(result_dto)
            
            return Response(
                result_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error al crear el gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Obtiene un gen específico por ID"""
        try:
            gene = Gene.objects.get(pk=pk)
            
            # Convertir Model a DTO
            gene_dto = GeneMapper.to_dto(gene)
            
            # Serializar DTO a JSON
            serializer = GeneSerializer(gene_dto)
            
            return Response(serializer.data)
            
        except Gene.DoesNotExist:
            return Response(
                {'error': f'Gen con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, pk=None):
        """Actualiza completamente un gen"""
        try:
            gene = Gene.objects.get(pk=pk)
            
            # Validar y deserializar JSON a UpdateDTO
            serializer = GeneUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Crear UpdateDTO
            update_dto = serializer.save()
            
            # Actualizar Model desde DTO
            gene = GeneMapper.update_model_from_dto(gene, update_dto)
            gene.save()
            
            # Convertir Model actualizado a DTO
            result_dto = GeneMapper.to_dto(gene)
            
            # Serializar DTO a JSON
            result_serializer = GeneSerializer(result_dto)
            
            return Response(result_serializer.data)
            
        except Gene.DoesNotExist:
            return Response(
                {'error': f'Gen con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un gen"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Elimina un gen si no tiene variantes asociadas"""
        try:
            gene = Gene.objects.get(pk=pk)
            
            # Validar que no tenga variantes
            if gene.variants.exists():
                return Response(
                    {
                        'error': 'No se puede eliminar el gen porque tiene variantes genéticas asociadas',
                        'variants_count': gene.variants.count()
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            gene.delete()
            
            return Response(
                {'message': f'Gen {gene.symbol} eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Gene.DoesNotExist:
            return Response(
                {'error': f'Gen con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Buscar genes por símbolo",
        description="Busca genes cuyo símbolo contenga el texto especificado",
        parameters=[
            OpenApiParameter(
                name='q',
                description='Término de búsqueda',
                required=True,
                type=str
            )
        ],
        tags=['Genes']
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Busca genes por símbolo"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Parámetro "q" es requerido para la búsqueda'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar en BD
        genes = Gene.objects.filter(symbol__icontains=query).annotate(
            variants_count=Count('variants')
        )
        
        # Convertir a DTOs
        gene_dtos = [
            GeneMapper.to_list_dto(gene, gene.variants_count) 
            for gene in genes
        ]
        
        # Crear DTO de resultado
        search_result = GeneSearchResultDTO(
            query=query,
            count=len(gene_dtos),
            results=gene_dtos
        )
        
        # Serializar
        serializer = GeneListSerializer(search_result.results, many=True)
        
        return Response({
            'query': search_result.query,
            'count': search_result.count,
            'results': serializer.data
        })
    
    @extend_schema(
        summary="Obtener estadísticas de genes",
        description="Obtiene estadísticas generales del catálogo de genes",
        tags=['Genes']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas del catálogo de genes"""
        total_genes = Gene.objects.count()
        genes_with_variants = Gene.objects.annotate(
            variant_count=Count('variants')
        ).filter(variant_count__gt=0).count()
        
        # Crear DTO de estadísticas
        stats_dto = GeneStatisticsDTO(
            total_genes=total_genes,
            genes_with_variants=genes_with_variants,
            genes_without_variants=total_genes - genes_with_variants
        )
        
        return Response({
            'total_genes': stats_dto.total_genes,
            'genes_with_variants': stats_dto.genes_with_variants,
            'genes_without_variants': stats_dto.genes_without_variants
        })