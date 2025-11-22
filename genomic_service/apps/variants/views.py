from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import GeneticVariant
from apps.genes.models import Gene
from .dtos import (
    GeneticVariantDTO, GeneticVariantCreateDTO, GeneticVariantUpdateDTO,
    GeneticVariantListDTO, VariantsByGeneDTO, VariantsByChromosomeDTO,
    VariantStatisticsDTO, GeneticVariantMapper
)
from .serializers import (
    GeneticVariantSerializer, GeneticVariantCreateSerializer,
    GeneticVariantUpdateSerializer, GeneticVariantListSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar todas las variantes genéticas",
        description="Obtiene el listado completo de variantes genéticas registradas",
        tags=['Variantes Genéticas']
    ),
    create=extend_schema(
        summary="Crear una nueva variante genética",
        description="Registra una nueva variante genética (mutación) en el sistema",
        tags=['Variantes Genéticas']
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de una variante",
        description="Obtiene información detallada de una variante genética específica",
        tags=['Variantes Genéticas']
    ),
    update=extend_schema(
        summary="Actualizar una variante completamente",
        description="Actualiza todos los campos de una variante existente",
        tags=['Variantes Genéticas']
    ),
    partial_update=extend_schema(
        summary="Actualizar una variante parcialmente",
        description="Actualiza uno o más campos de una variante existente",
        tags=['Variantes Genéticas']
    ),
    destroy=extend_schema(
        summary="Eliminar una variante",
        description="Elimina una variante genética del sistema",
        tags=['Variantes Genéticas']
    )
)
class GeneticVariantViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión completa de Variantes Genéticas
    Usa DTOs para transferencia de datos
    """
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'create':
            return GeneticVariantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GeneticVariantUpdateSerializer
        elif self.action == 'list':
            return GeneticVariantListSerializer
        return GeneticVariantSerializer
    
    def list(self, request):
        """Lista todas las variantes con filtros opcionales"""
        # Obtener variantes desde BD
        variants = GeneticVariant.objects.select_related('gene').all()
        
        # Aplicar filtros
        gene_id = request.query_params.get('gene_id', None)
        if gene_id:
            variants = variants.filter(gene_id=gene_id)
        
        chromosome = request.query_params.get('chromosome', None)
        if chromosome:
            variants = variants.filter(chromosome=chromosome)
        
        impact = request.query_params.get('impact', None)
        if impact:
            variants = variants.filter(impact=impact)
        
        # Convertir Models a DTOs
        variant_dtos = [
            GeneticVariantMapper.to_list_dto(variant) 
            for variant in variants
        ]
        
        # Serializar DTOs a JSON
        serializer = GeneticVariantListSerializer(variant_dtos, many=True)
        
        return Response({
            'count': len(variant_dtos),
            'results': serializer.data
        })
    
    def create(self, request):
        """Crea una nueva variante genética"""
        # Validar y deserializar JSON a DTO
        serializer = GeneticVariantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Crear DTO
            variant_dto = serializer.save()
            
            # Validar que el gen existe
            try:
                gene = Gene.objects.get(pk=variant_dto.gene_id)
            except Gene.DoesNotExist:
                return Response(
                    {'error': f'Gen con ID {variant_dto.gene_id} no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Convertir DTO a Model
            variant = GeneticVariantMapper.to_model(variant_dto, gene)
            
            # Guardar en BD
            variant.save()
            
            # Convertir Model guardado a DTO completo
            result_dto = GeneticVariantMapper.to_dto(variant)
            
            # Serializar DTO a JSON
            result_serializer = GeneticVariantSerializer(result_dto)
            
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
                {'error': f'Error al crear la variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Obtiene una variante específica por ID"""
        try:
            variant = GeneticVariant.objects.select_related('gene').get(pk=pk)
            
            # Convertir Model a DTO
            variant_dto = GeneticVariantMapper.to_dto(variant)
            
            # Serializar DTO a JSON
            serializer = GeneticVariantSerializer(variant_dto)
            
            return Response(serializer.data)
            
        except GeneticVariant.DoesNotExist:
            return Response(
                {'error': f'Variante con ID {pk} no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, pk=None):
        """Actualiza una variante genética"""
        try:
            variant = GeneticVariant.objects.select_related('gene').get(pk=pk)
            
            # Validar y deserializar JSON a UpdateDTO
            serializer = GeneticVariantUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Crear UpdateDTO
            update_dto = serializer.save()
            
            # Actualizar Model desde DTO
            variant = GeneticVariantMapper.update_model_from_dto(variant, update_dto)
            variant.save()
            
            # Convertir Model actualizado a DTO
            result_dto = GeneticVariantMapper.to_dto(variant)
            
            # Serializar DTO a JSON
            result_serializer = GeneticVariantSerializer(result_dto)
            
            return Response(result_serializer.data)
            
        except GeneticVariant.DoesNotExist:
            return Response(
                {'error': f'Variante con ID {pk} no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente una variante"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Elimina una variante genética"""
        try:
            variant = GeneticVariant.objects.get(pk=pk)
            gene_symbol = variant.gene.symbol
            variant.delete()
            
            return Response(
                {'message': f'Variante del gen {gene_symbol} eliminada exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except GeneticVariant.DoesNotExist:
            return Response(
                {'error': f'Variante con ID {pk} no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener variantes por gen",
        description="Lista todas las variantes asociadas a un gen específico",
        parameters=[
            OpenApiParameter(
                name='gene_symbol',
                description='Símbolo del gen (ej: BRCA1)',
                required=True,
                type=str
            )
        ],
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def by_gene(self, request):
        """Obtiene variantes de un gen específico por símbolo"""
        gene_symbol = request.query_params.get('gene_symbol', '')
        
        if not gene_symbol:
            return Response(
                {'error': 'Parámetro "gene_symbol" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            gene = Gene.objects.get(symbol=gene_symbol.upper())
        except Gene.DoesNotExist:
            return Response(
                {'error': f'No se encontró el gen con símbolo {gene_symbol}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener variantes del gen
        variants = GeneticVariant.objects.filter(gene=gene).select_related('gene')
        
        # Convertir a DTOs
        variant_dtos = [
            GeneticVariantMapper.to_list_dto(variant) 
            for variant in variants
        ]
        
        # Crear DTO de resultado
        result_dto = VariantsByGeneDTO(
            gene_symbol=gene.symbol,
            gene_name=gene.full_name,
            total_variants=len(variant_dtos),
            variants=variant_dtos
        )
        
        # Serializar
        serializer = GeneticVariantListSerializer(result_dto.variants, many=True)
        
        return Response({
            'gene_symbol': result_dto.gene_symbol,
            'gene_name': result_dto.gene_name,
            'total_variants': result_dto.total_variants,
            'variants': serializer.data
        })
    
    @extend_schema(
        summary="Obtener variantes por cromosoma",
        description="Lista todas las variantes en un cromosoma específico",
        parameters=[
            OpenApiParameter(
                name='chr',
                description='Cromosoma (ej: chr17)',
                required=True,
                type=str
            )
        ],
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def by_chromosome(self, request):
        """Obtiene variantes por cromosoma"""
        chromosome = request.query_params.get('chr', '')
        
        if not chromosome:
            return Response(
                {'error': 'Parámetro "chr" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener variantes del cromosoma
        variants = GeneticVariant.objects.filter(
            chromosome=chromosome
        ).select_related('gene')
        
        # Convertir a DTOs
        variant_dtos = [
            GeneticVariantMapper.to_list_dto(variant) 
            for variant in variants
        ]
        
        # Crear DTO de resultado
        result_dto = VariantsByChromosomeDTO(
            chromosome=chromosome,
            total_variants=len(variant_dtos),
            variants=variant_dtos
        )
        
        # Serializar
        serializer = GeneticVariantListSerializer(result_dto.variants, many=True)
        
        return Response({
            'chromosome': result_dto.chromosome,
            'total_variants': result_dto.total_variants,
            'variants': serializer.data
        })
    
    @extend_schema(
        summary="Estadísticas de variantes",
        description="Obtiene estadísticas generales de las variantes genéticas",
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de variantes"""
        total_variants = GeneticVariant.objects.count()
        
        # Contar por impacto
        impact_stats = list(
            GeneticVariant.objects.values('impact').annotate(count=Count('id'))
        )
        
        # Contar por cromosoma (top 5)
        chromosome_stats = list(
            GeneticVariant.objects.values('chromosome').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
        )
        
        # Crear DTO de estadísticas
        stats_dto = VariantStatisticsDTO(
            total_variants=total_variants,
            by_impact=impact_stats,
            top_chromosomes=chromosome_stats
        )
        
        return Response({
            'total_variants': stats_dto.total_variants,
            'by_impact': stats_dto.by_impact,
            'top_chromosomes': stats_dto.top_chromosomes
        })