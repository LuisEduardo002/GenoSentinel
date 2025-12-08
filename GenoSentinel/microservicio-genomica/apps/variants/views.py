from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .services import GeneticVariantService
from .serializers import (
    GeneticVariantSerializer, GeneticVariantCreateSerializer,
    GeneticVariantUpdateSerializer, GeneticVariantListSerializer,
    VariantsByGeneResultSerializer, VariantsByChromosomeResultSerializer,
    VariantStatisticsResultSerializer
)

# Inicializar el servicio (inyección de dependencia simple)
variant_service = GeneticVariantService()

@extend_schema_view(
    list=extend_schema(
        summary="Listar todas las variantes genéticas",
        description="Obtiene el listado completo de variantes genéticas registradas. Soporta filtros por gen, cromosoma e impacto. Si se aplican filtros y no hay resultados, retorna 404.",
        tags=['Variantes Genéticas'],
        parameters=[
            OpenApiParameter(name='gene_id', type=str, description='Filtrar por ID de gen (UUID)'),
            OpenApiParameter(name='chromosome', type=str, description='Filtrar por cromosoma (ej: chr17)'),
            OpenApiParameter(name='impact', type=str, description='Filtrar por impacto (ej: HIGH, MODERATE, LOW)')
        ],
        responses={
            200: GeneticVariantListSerializer(many=True),
            400: {'description': 'gene_id inválido - No es un UUID válido'},
            404: {'description': 'No se encontraron variantes con los filtros aplicados'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    create=extend_schema(
        summary="Crear una nueva variante genética",
        description="Registra una nueva variante genética (mutación) en el sistema",
        tags=['Variantes Genéticas'],
        request=GeneticVariantCreateSerializer,
        responses=GeneticVariantSerializer
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de una variante",
        description="Obtiene información detallada de una variante genética específica por su ID (UUID)",
        tags=['Variantes Genéticas'],
        responses={
            200: GeneticVariantSerializer,
            400: {'description': 'ID inválido - El parámetro no es un UUID válido'},
            404: {'description': 'Variante no encontrada'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    update=extend_schema(
        summary="Actualizar una variante completamente",
        description="Actualiza todos los campos de una variante existente. Requiere enviar al menos un campo.",
        tags=['Variantes Genéticas'],
        request=GeneticVariantUpdateSerializer,
        responses={
            200: GeneticVariantSerializer,
            400: {'description': 'ID inválido, datos vacíos, o datos de entrada inválidos'},
            404: {'description': 'Variante no encontrada'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    partial_update=extend_schema(
        summary="Actualizar una variante parcialmente",
        description="Actualiza uno o más campos de una variante existente (PATCH)",
        tags=['Variantes Genéticas'],
        request=GeneticVariantUpdateSerializer,
        responses={
            200: GeneticVariantSerializer,
            400: {'description': 'ID inválido, datos vacíos, o datos de entrada inválidos'},
            404: {'description': 'Variante no encontrada'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    destroy=extend_schema(
        summary="Eliminar una variante",
        description="Elimina una variante genética del sistema de forma permanente",
        tags=['Variantes Genéticas'],
        responses={
            204: {'description': 'Variante eliminada exitosamente (No Content)'},
            400: {'description': 'ID inválido - El parámetro no es un UUID válido'},
            404: {'description': 'Variante no encontrada'},
            500: {'description': 'Error interno del servidor'}
        }
    )
)
class GeneticVariantViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión completa de Variantes Genéticas.
    Actúa como orquestador entre la capa HTTP y la capa de Servicio.
    """
    
    def list(self, request):
        """Lista todas las variantes con filtros opcionales"""
        try:
            # 1. Obtener parámetros de la request
            gene_id = request.query_params.get('gene_id', None)
            chromosome = request.query_params.get('chromosome', None)
            impact = request.query_params.get('impact', None)
            
            # 2. Validar gene_id si se proporciona (debe ser UUID)
            if gene_id:
                try:
                    from uuid import UUID
                    gene_id = str(UUID(gene_id))  # Valida y convierte a string
                except (ValueError, AttributeError, TypeError):
                    return Response(
                        {'error': f'gene_id inválido: "{gene_id}" no es un UUID válido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # 3. Llamar al Service (lógica de negocio)
            variant_dtos = variant_service.get_all_variants(gene_id, chromosome, impact)
            
            # 4. Verificar si hay resultados cuando se usan filtros
            has_filters = gene_id or chromosome or impact
            if len(variant_dtos) == 0 and has_filters:
                filters_applied = []
                if gene_id:
                    filters_applied.append(f'gene_id={gene_id}')
                if chromosome:
                    filters_applied.append(f'chromosome={chromosome}')
                if impact:
                    filters_applied.append(f'impact={impact}')
                
                return Response(
                    {
                        'error': f'No se encontraron variantes con los filtros aplicados: {", ".join(filters_applied)}',
                        'count': 0,
                        'results': []
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 5. Serializar DTOs a JSON (Serializer de Salida)
            serializer = GeneticVariantListSerializer(variant_dtos, many=True)
            
            return Response({
                'count': len(variant_dtos),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener variantes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """Crea una nueva variante genética"""
        # 1. Validar y deserializar JSON a DTO (Serializer de Entrada)
        serializer = GeneticVariantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Obtener DTO de entrada
        create_dto = serializer.save()
        
        try:
            # 3. Llamar al Service (lógica de negocio)
            result_dto = variant_service.create_variant(create_dto)
            
            # 4. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneticVariantSerializer(result_dto)
            
            return Response(
                result_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError as e:
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
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                variant_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Llamar al Service (lógica de negocio)
            variant_dto = variant_service.get_variant_by_id(variant_id)
            
            # 3. Serializar DTO a JSON (Serializer de Salida)
            serializer = GeneticVariantSerializer(variant_dto)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener la variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """Actualiza una variante genética"""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                variant_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Validar que se envíe al menos un campo para actualizar
            if not request.data:
                return Response(
                    {'error': 'Debe proporcionar al menos un campo para actualizar'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Validar y deserializar JSON a UpdateDTO (Serializer de Entrada)
            serializer = GeneticVariantUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 4. Obtener DTO de entrada
            update_dto = serializer.save()
            
            # 5. Llamar al Service (lógica de negocio)
            result_dto = variant_service.update_variant(variant_id, update_dto)
            
            # 6. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneticVariantSerializer(result_dto)
            
            return Response(result_serializer.data, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar la variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente una variante (PATCH)."""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                variant_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Validar y deserializar JSON a UpdateDTO con partial=True
            serializer = GeneticVariantUpdateSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # 3. Obtener DTO de entrada
            update_dto = serializer.save()

            # 4. Llamar al Service (lógica de negocio)
            result_dto = variant_service.update_variant(variant_id, update_dto)

            # 5. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneticVariantSerializer(result_dto)

            return Response(result_serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar la variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """Elimina una variante"""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                variant_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Llamar al Service (lógica de negocio)
            variant_service.delete_variant(variant_id)
            
            # 3. HTTP 204 No Content (eliminación exitosa)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar la variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        responses={
            200: VariantsByGeneResultSerializer,
            400: {'description': 'Parámetro "gene_symbol" requerido'},
            404: {'description': 'Gen no encontrado o sin variantes'},
            500: {'description': 'Error interno del servidor'}
        },
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def by_gene(self, request):
        """Obtiene variantes de un gen específico por símbolo"""
        try:
            gene_symbol = request.query_params.get('gene_symbol', '')
            
            if not gene_symbol:
                return Response(
                    {'error': 'Parámetro "gene_symbol" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 1. Llamar al Service (lógica de negocio)
            result_dto = variant_service.get_variants_by_gene_symbol(gene_symbol)
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = VariantsByGeneResultSerializer(result_dto)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener variantes por gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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
        responses={
            200: VariantsByChromosomeResultSerializer,
            400: {'description': 'Parámetro "chr" requerido o inválido'},
            404: {'description': 'No se encontraron variantes para el cromosoma especificado'},
            500: {'description': 'Error interno del servidor'}
        },
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def by_chromosome(self, request):
        """Obtiene variantes por cromosoma"""
        try:
            chromosome = request.query_params.get('chr', '')
            
            if not chromosome:
                return Response(
                    {'error': 'Parámetro "chr" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 1. Llamar al Service (lógica de negocio)
            result_dto = variant_service.get_variants_by_chromosome(chromosome)
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = VariantsByChromosomeResultSerializer(result_dto)
            
            if not result_dto.variants:
                return Response(
                    {
                        'error': f'No se encontraron variantes para el cromosoma {chromosome}',
                        'chromosome': chromosome,
                        'count': 0,
                        'variants': []
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener variantes por cromosoma: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @extend_schema(
        summary="Estadísticas de variantes",
        description="Obtiene estadísticas generales de las variantes genéticas",
        responses={
            200: VariantStatisticsResultSerializer,
            500: {'description': 'Error interno del servidor'}
        },
        tags=['Variantes Genéticas']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de variantes"""
        try:
            # 1. Llamar al Service (lógica de negocio)
            stats_dto = variant_service.get_statistics()
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = VariantStatisticsResultSerializer(stats_dto)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener estadísticas de variantes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
