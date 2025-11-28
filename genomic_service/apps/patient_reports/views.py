from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from uuid import UUID

from .services import PatientVariantReportService
from .serializers import (
    PatientVariantReportSerializer, PatientVariantReportCreateSerializer,
    PatientVariantReportUpdateSerializer, PatientVariantReportListSerializer,
    PatientReportsSummarySerializer, PatientStatisticsSerializer,
    GeneralReportStatisticsSerializer
)

# Inicializar el servicio (inyección de dependencia simple)
report_service = PatientVariantReportService()

@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los reportes de variantes",
        description="Obtiene el listado completo de reportes de variantes de pacientes. Se puede filtrar por patient_id o gene_symbol.",
        tags=['Reportes de Pacientes'],
        parameters=[
            OpenApiParameter(name='patient_id', type=str, description='Filtrar por ID de paciente'),
            OpenApiParameter(name='gene_symbol', type=str, description='Filtrar por símbolo de gen')
        ]
    ),
    create=extend_schema(
        summary="Crear un nuevo reporte de variante",
        description="Registra una nueva variante genética detectada en un paciente",
        tags=['Reportes de Pacientes'],
        request=PatientVariantReportCreateSerializer,
        responses=PatientVariantReportSerializer
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de un reporte",
        description="Obtiene información detallada de un reporte específico, incluyendo datos clínicos integrados.",
        tags=['Reportes de Pacientes'],
        responses=PatientVariantReportSerializer
    ),
    update=extend_schema(
        summary="Actualizar un reporte completamente",
        description="Actualiza los campos de un reporte existente",
        tags=['Reportes de Pacientes'],
        request=PatientVariantReportUpdateSerializer,
        responses=PatientVariantReportSerializer
    ),
    partial_update=extend_schema(
        summary="Actualizar un reporte parcialmente",
        description="Actualiza uno o más campos de un reporte existente",
        tags=['Reportes de Pacientes'],
        request=PatientVariantReportUpdateSerializer,
        responses=PatientVariantReportSerializer
    ),
    destroy=extend_schema(
        summary="Eliminar un reporte",
        description="Elimina un reporte de variante del sistema",
        tags=['Reportes de Pacientes']
    )
)
class PatientVariantReportViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Reportes de Variantes de Pacientes.
    Actúa como orquestador entre la capa HTTP y la capa de Servicio.
    """
    
    def list(self, request):
        """Lista todos los reportes con filtros opcionales"""
        # 1. Obtener parámetros de la request
        patient_id_str = request.query_params.get('patient_id', None)
        gene_symbol = request.query_params.get('gene_symbol', None)
        
        patient_id = UUID(patient_id_str) if patient_id_str else None
        
        # 2. Llamar al Service (lógica de negocio)
        report_dtos = report_service.get_all_reports(patient_id, gene_symbol)
        
        # 3. Serializar DTOs a JSON (Serializer de Salida)
        serializer = PatientVariantReportListSerializer(report_dtos, many=True)
        
        return Response({
            'count': len(report_dtos),
            'results': serializer.data
        })
    
    def create(self, request):
        """Crea un nuevo reporte de variante para un paciente"""
        # 1. Validar y deserializar JSON a DTO (Serializer de Entrada)
        serializer = PatientVariantReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Obtener DTO de entrada
        create_dto = serializer.save()
        
        try:
            # 3. Llamar al Service (lógica de negocio)
            result_dto = report_service.create_report(create_dto)
            
            # 4. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = PatientVariantReportSerializer(result_dto)
            
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
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error al crear el reporte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Obtiene un reporte específico por ID"""
        try:
            # 1. Llamar al Service (lógica de negocio)
            report_dto = report_service.get_report_by_id(UUID(pk))
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = PatientVariantReportSerializer(report_dto)
            
            return Response(serializer.data)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'ID de reporte inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, pk=None):
        """Actualiza un reporte de paciente"""
        # 1. Validar y deserializar JSON a UpdateDTO (Serializer de Entrada)
        serializer = PatientVariantReportUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Obtener DTO de entrada
        update_dto = serializer.save()
        
        try:
            # 3. Llamar al Service (lógica de negocio)
            result_dto = report_service.update_report(UUID(pk), update_dto)
            
            # 4. Serializar DTO a JSON (Serializer de Salida)
            result_serializer = PatientVariantReportSerializer(result_dto)
            
            return Response(result_serializer.data)
            
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
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un reporte"""
        # Reutiliza la lógica de update, ya que UpdateSerializer maneja campos opcionales
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Elimina un reporte de paciente"""
        try:
            # 1. Llamar al Service (lógica de negocio)
            report_service.delete_report(UUID(pk))
            
            return Response(
                {'message': f'Reporte con ID {pk} eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'ID de reporte inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Obtener todos los reportes de un paciente",
        description="Lista todas las variantes genéticas detectadas en un paciente específico con información clínica integrada",
        parameters=[
            OpenApiParameter(
                name='patient_id',
                description='UUID del paciente',
                required=True,
                type=str
            )
        ],
        responses=PatientReportsSummarySerializer,
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def by_patient(self, request, patient_id=None):
        """
        Obtiene todos los reportes de un paciente específico
        Integra información del Microservicio de Clínica
        """
        try:
            patient_uuid = UUID(patient_id)
            
            # 1. Llamar al Service (lógica de negocio)
            summary_dto = report_service.get_reports_by_patient(patient_uuid)
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = PatientReportsSummarySerializer(summary_dto)
            
            return Response(serializer.data)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'ID de paciente inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Estadísticas de reportes por paciente",
        description="Obtiene estadísticas de las variantes detectadas en un paciente",
        parameters=[
            OpenApiParameter(
                name='patient_id',
                description='UUID del paciente',
                required=True,
                type=str
            )
        ],
        responses=PatientStatisticsSerializer,
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'])
    def patient_statistics(self, request):
        """Estadísticas de variantes por paciente"""
        patient_id_str = request.query_params.get('patient_id', '')
        
        if not patient_id_str:
            return Response(
                {'error': 'Parámetro "patient_id" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient_uuid = UUID(patient_id_str)
            
            # 1. Llamar al Service (lógica de negocio)
            stats_dto = report_service.get_patient_statistics(patient_uuid)
            
            # 2. Serializar DTO a JSON (Serializer de Salida)
            serializer = PatientStatisticsSerializer(stats_dto)
            
            return Response(serializer.data)
            
        except ObjectDoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'ID de paciente inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Estadísticas generales de reportes",
        description="Obtiene estadísticas globales del sistema de reportes",
        responses=GeneralReportStatisticsSerializer,
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'])
    def general_statistics(self, request):
        """Estadísticas generales del sistema"""
        # 1. Llamar al Service (lógica de negocio)
        stats_dto = report_service.get_general_statistics()
        
        # 2. Serializar DTO a JSON (Serializer de Salida)
        serializer = GeneralReportStatisticsSerializer(stats_dto)
        
        return Response(serializer.data)
