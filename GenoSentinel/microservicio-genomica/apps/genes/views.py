from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .services import GeneService
from .serializers import (
    GeneSerializer, GeneCreateSerializer, GeneUpdateSerializer, 
    GeneSearchResultSerializer, GeneStatisticsSerializer
)

# Inicializar el servicio (inyección de dependencia simple)
gene_service = GeneService()

@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los genes",
        description="Obtiene el listado completo de genes registrados. Si se proporciona un parámetro de búsqueda y no se encuentran resultados, retorna 404.",
        tags=['Genes'],
        parameters=[
            OpenApiParameter(name='search', type=str, description='Búsqueda por símbolo o nombre completo')
        ],
        responses={
            200: GeneSearchResultSerializer,
            404: {'description': 'No se encontraron genes para la búsqueda especificada'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    create=extend_schema(
        summary="Crear un nuevo gen",
        description="Registra un nuevo gen en el sistema",
        tags=['Genes'],
        request=GeneCreateSerializer,
        responses=GeneSerializer
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de un gen",
        description="Obtiene información detallada de un gen específico por su ID (UUID)",
        tags=['Genes'],
        responses={
            200: GeneSerializer,
            400: {'description': 'ID inválido - El parámetro no es un UUID válido'},
            404: {'description': 'Gen no encontrado'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    update=extend_schema(
        summary="Actualizar un gen completamente",
        description="Actualiza todos los campos de un gen existente. Requiere enviar al menos un campo.",
        tags=['Genes'],
        request=GeneUpdateSerializer,
        responses={
            200: GeneSerializer,
            400: {'description': 'ID inválido, datos vacíos, o datos de entrada inválidos'},
            404: {'description': 'Gen no encontrado'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    partial_update=extend_schema(
        summary="Actualizar un gen parcialmente",
        description="Actualiza uno o más campos de un gen existente (PATCH)",
        tags=['Genes'],
        request=GeneUpdateSerializer,
        responses={
            200: GeneSerializer,
            400: {'description': 'ID inválido, datos vacíos, o datos de entrada inválidos'},
            404: {'description': 'Gen no encontrado'},
            500: {'description': 'Error interno del servidor'}
        }
    ),
    destroy=extend_schema(
        summary="Eliminar un gen",
        description="Elimina un gen del sistema de forma permanente",
        tags=['Genes'],
        responses={
            204: {'description': 'Gen eliminado exitosamente (No Content)'},
            400: {'description': 'ID inválido - El parámetro no es un UUID válido'},
            404: {'description': 'Gen no encontrado'},
            500: {'description': 'Error interno del servidor'}
        }
    )
)
class GeneViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión completa de Genes.
    Actúa como orquestador entre la capa HTTP y la capa de Servicio.
    """
    
    def list(self, request):
        """Lista todos los genes con búsqueda opcional"""
        try:
            # 1. Obtener parámetros de la request
            search_query = request.query_params.get('search', None)
            
            # 2. Llamar al Service (lógica de negocio)
            result_dto = gene_service.get_all_genes(search_query)
            
            # 3. Verificar si hay resultados
            if result_dto.count == 0 and search_query:
                # Si se hizo una búsqueda específica y no se encontraron resultados
                return Response(
                    {
                        'error': f'No se encontraron genes para la búsqueda: "{search_query}"',
                        'query': search_query,
                        'count': 0,
                        'results': []
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 4. Serializar DTO a JSON (Serializer de Salida)
            serializer = GeneSearchResultSerializer(result_dto)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener genes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """Crea un nuevo gen"""
        # 1. Validar y deserializar JSON a DTO (Serializer de Entrada)
        serializer = GeneCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Obtener DTO de entrada
        create_dto = serializer.save()
        
        try:
            # 3. Llamar al Service (lógica de negocio)
            result_dto = gene_service.create_gene(create_dto)
            
            # 4. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneSerializer(result_dto)
            
            return Response(
                result_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except IntegrityError as e:
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
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                gene_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Llamar al Service (lógica de negocio)
            gene_dto = gene_service.get_gene_by_id(gene_id)
            
            # 3. Serializar DTO a JSON (Serializer de Salida)
            serializer = GeneSerializer(gene_dto)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener el gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """Actualiza un gen genético"""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                gene_id = UUID(pk)
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
            serializer = GeneUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 4. Obtener DTO de entrada
            update_dto = serializer.save()
            
            # 5. Llamar al Service (lógica de negocio)
            result_dto = gene_service.update_gene(gene_id, update_dto)
            
            # 6. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneSerializer(result_dto)
            
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
                {'error': f'Error al actualizar el gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un gen (PATCH)."""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                gene_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Validar y deserializar JSON a UpdateDTO con partial=True
            serializer = GeneUpdateSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # 3. Obtener DTO de entrada
            update_dto = serializer.save()

            # 4. Llamar al Service (lógica de negocio)
            result_dto = gene_service.update_gene(gene_id, update_dto)

            # 5. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = GeneSerializer(result_dto)

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
                {'error': f'Error al actualizar el gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """Elimina un gen"""
        try:
            # 1. Validar formato UUID
            try:
                from uuid import UUID
                gene_id = UUID(pk)
            except (ValueError, AttributeError, TypeError):
                return Response(
                    {'error': f'ID inválido: "{pk}" no es un UUID válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2. Llamar al Service (lógica de negocio)
            gene_symbol = gene_service.delete_gene(gene_id)
            
            # 3. HTTP 204 No Content (eliminación exitosa)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar el gen: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @extend_schema(
        summary="Estadísticas de genes",
        description="Obtiene estadísticas generales de los genes",
        responses=GeneStatisticsSerializer,
        tags=['Genes']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de genes"""
        # 1. Llamar al Service (lógica de negocio)
        stats_dto = gene_service.get_statistics()
        
        # 2. Serializar DTO a JSON (Serializer de Salida)
        serializer = GeneStatisticsSerializer(stats_dto)
        
        return Response(serializer.data)
