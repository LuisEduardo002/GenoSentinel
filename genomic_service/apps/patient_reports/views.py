from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import PatientVariantReport
from apps.variants.models import GeneticVariant
from .dtos import (
    PatientVariantReportDTO, PatientVariantReportCreateDTO,
    PatientVariantReportUpdateDTO, PatientVariantReportListDTO,
    PatientReportsSummaryDTO, PatientStatisticsDTO,
    GeneralReportStatisticsDTO, PatientVariantReportMapper
)
from .serializers import (
    PatientVariantReportSerializer, PatientVariantReportCreateSerializer,
    PatientVariantReportUpdateSerializer, PatientVariantReportListSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los reportes de variantes",
        description="Obtiene el listado completo de reportes de variantes de pacientes",
        tags=['Reportes de Pacientes']
    ),
    create=extend_schema(
        summary="Crear un nuevo reporte de variante",
        description="Registra una nueva variante genética detectada en un paciente",
        tags=['Reportes de Pacientes']
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de un reporte",
        description="Obtiene información detallada de un reporte específico",
        tags=['Reportes de Pacientes']
    ),
    update=extend_schema(
        summary="Actualizar un reporte completamente",
        description="Actualiza todos los campos de un reporte existente",
        tags=['Reportes de Pacientes']
    ),
    partial_update=extend_schema(
        summary="Actualizar un reporte parcialmente",
        description="Actualiza uno o más campos de un reporte existente",
        tags=['Reportes de Pacientes']
    ),
    destroy=extend_schema(
        summary="Eliminar un reporte",
        description="Elimina un reporte de variante del sistema",
        tags=['Reportes de Pacientes']
    )
)
class PatientVariantReportViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Reportes de Variantes de Pacientes
    Usa DTOs para transferencia de datos e integración con Microservicio Clínica
    """
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'create':
            return PatientVariantReportCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PatientVariantReportUpdateSerializer
        elif self.action == 'list':
            return PatientVariantReportListSerializer
        return PatientVariantReportSerializer
    
    def list(self, request):
        """Lista todos los reportes con filtros opcionales"""
        # Obtener reportes desde BD
        reports = PatientVariantReport.objects.select_related(
            'variant', 'variant__gene'
        ).all()
        
        # Aplicar filtros
        patient_id = request.query_params.get('patient_id', None)
        if patient_id:
            reports = reports.filter(patient_id=patient_id)
        
        gene_symbol = request.query_params.get('gene_symbol', None)
        if gene_symbol:
            reports = reports.filter(variant__gene__symbol=gene_symbol)
        
        # Convertir Models a DTOs
        report_dtos = [
            PatientVariantReportMapper.to_list_dto(report) 
            for report in reports
        ]
        
        # Serializar DTOs a JSON
        serializer = PatientVariantReportListSerializer(report_dtos, many=True)
        
        return Response({
            'count': len(report_dtos),
            'results': serializer.data
        })
    
    def create(self, request):
        """Crea un nuevo reporte de variante para un paciente"""
        # Validar y deserializar JSON a DTO
        serializer = PatientVariantReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Crear DTO
            report_dto = serializer.save()
            
            # Validar que la variante existe
            try:
                variant = GeneticVariant.objects.select_related('gene').get(
                    pk=report_dto.variant_id
                )
            except GeneticVariant.DoesNotExist:
                return Response(
                    {'error': f'Variante con ID {report_dto.variant_id} no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # TODO: Validar que el paciente existe en Microservicio Clínica
            # clinical_data = self._get_patient_clinical_data(report_dto.patient_id)
            
            # Convertir DTO a Model
            report = PatientVariantReportMapper.to_model(report_dto, variant)
            
            # Guardar en BD
            report.save()
            
            # Obtener datos clínicos (placeholder)
            clinical_data = PatientVariantReportMapper.create_clinical_data_dto(
                report.patient_id
            )
            
            # Convertir Model guardado a DTO completo
            result_dto = PatientVariantReportMapper.to_dto(report, clinical_data)
            
            # Serializar DTO a JSON
            result_serializer = PatientVariantReportSerializer(result_dto)
            
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
                {'error': f'Error al crear el reporte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Obtiene un reporte específico por ID"""
        try:
            report = PatientVariantReport.objects.select_related(
                'variant', 'variant__gene'
            ).get(pk=pk)
            
            # Obtener datos clínicos (placeholder)
            clinical_data = PatientVariantReportMapper.create_clinical_data_dto(
                report.patient_id
            )
            
            # Convertir Model a DTO
            report_dto = PatientVariantReportMapper.to_dto(report, clinical_data)
            
            # Serializar DTO a JSON
            serializer = PatientVariantReportSerializer(report_dto)
            
            return Response(serializer.data)
            
        except PatientVariantReport.DoesNotExist:
            return Response(
                {'error': f'Reporte con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, pk=None):
        """Actualiza un reporte de paciente"""
        try:
            report = PatientVariantReport.objects.select_related(
                'variant', 'variant__gene'
            ).get(pk=pk)
            
            # Validar y deserializar JSON a UpdateDTO
            serializer = PatientVariantReportUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Crear UpdateDTO
            update_dto = serializer.save()
            
            # Actualizar Model desde DTO
            report = PatientVariantReportMapper.update_model_from_dto(report, update_dto)
            report.save()
            
            # Obtener datos clínicos
            clinical_data = PatientVariantReport
            Mapper.create_clinical_data_dto(
                report.patient_id
            )
            
            # Convertir Model actualizado a DTO
            result_dto = PatientVariantReportMapper.to_dto(report, clinical_data)
            
            # Serializar DTO a JSON
            result_serializer = PatientVariantReportSerializer(result_dto)
            
            return Response(result_serializer.data)
            
        except PatientVariantReport.DoesNotExist:
            return Response(
                {'error': f'Reporte con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un reporte"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Elimina un reporte de paciente"""
        try:
            report = PatientVariantReport.objects.get(pk=pk)
            patient_id = report.patient_id
            report.delete()
            
            return Response(
                {'message': f'Reporte del paciente {patient_id} eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except PatientVariantReport.DoesNotExist:
            return Response(
                {'error': f'Reporte con ID {pk} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
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
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def by_patient(self, request, patient_id=None):
        """
        Obtiene todos los reportes de un paciente específico
        Integra información del Microservicio de Clínica
        """
        reports = PatientVariantReport.objects.filter(
            patient_id=patient_id
        ).select_related('variant', 'variant__gene')
        
        if not reports.exists():
            return Response(
                {'error': f'No se encontraron reportes para el paciente {patient_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Convertir a DTOs
        report_dtos = [
            PatientVariantReportMapper.to_list_dto(report) 
            for report in reports
        ]
        
        # Obtener datos clínicos del paciente
        clinical_data = self._get_patient_clinical_data(patient_id)
        
        # Crear DTO de resumen
        summary_dto = PatientReportsSummaryDTO(
            patient_id=patient_id,
            total_variants=len(report_dtos),
            clinical_summary=clinical_data,
            reports=report_dtos
        )
        
        # Serializar
        serializer = PatientVariantReportListSerializer(summary_dto.reports, many=True)
        
        return Response({
            'patient_id': str(summary_dto.patient_id),
            'total_variants': summary_dto.total_variants,
            'clinical_summary': {
                'patient_id': str(clinical_data.patient_id),
                'first_name': clinical_data.first_name,
                'last_name': clinical_data.last_name,
                'birth_date': clinical_data.birth_date.isoformat() if clinical_data.birth_date else None,
                'gender': clinical_data.gender,
                'status': clinical_data.status,
                'integration_status': clinical_data.integration_status,
                'message': clinical_data.message
            },
            'reports': serializer.data
        })
    
    def _get_patient_clinical_data(self, patient_id):
        """
        Obtiene información clínica del paciente desde el Microservicio de Clínica
        TODO: Implementar llamada HTTP real cuando el microservicio esté disponible
        """
        # Placeholder para la integración futura
        # try:
        #     import requests
        #     from django.conf import settings
        #     
        #     clinical_service_url = f"{settings.CLINICAL_SERVICE_URL}/api/patients/{patient_id}"
        #     headers = {'Authorization': f'Bearer {token}'}
        #     response = requests.get(clinical_service_url, headers=headers, timeout=5)
        #     
        #     if response.status_code == 200:
        #         data = response.json()
        #         return PatientVariantReportMapper.create_clinical_data_dto(patient_id, data)
        # except Exception as e:
        #     print(f"Error al obtener datos clínicos: {str(e)}")
        
        return PatientVariantReportMapper.create_clinical_data_dto(patient_id)
    
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
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'])
    def patient_statistics(self, request):
        """Estadísticas de variantes por paciente"""
        patient_id = request.query_params.get('patient_id', '')
        
        if not patient_id:
            return Response(
                {'error': 'Parámetro "patient_id" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reports = PatientVariantReport.objects.filter(patient_id=patient_id)
        
        if not reports.exists():
            return Response(
                {'error': f'No se encontraron reportes para el paciente {patient_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Estadísticas por impacto
        impact_stats = list(
            reports.values('variant__impact').annotate(count=Count('id'))
        )
        
        # Promedio de frecuencia alélica
        avg_vaf = reports.aggregate(avg_vaf=Avg('allele_frequency'))
        
        # Genes más afectados
        top_genes = list(
            reports.values('variant__gene__symbol').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
        )
        
        # Crear DTO de estadísticas
        stats_dto = PatientStatisticsDTO(
            patient_id=patient_id,
            total_variants=reports.count(),
            average_allele_frequency=avg_vaf['avg_vaf'],
            variants_by_impact=impact_stats,
            top_affected_genes=top_genes
        )
        
        return Response({
            'patient_id': str(stats_dto.patient_id),
            'total_variants': stats_dto.total_variants,
            'average_allele_frequency': str(stats_dto.average_allele_frequency) if stats_dto.average_allele_frequency else None,
            'variants_by_impact': stats_dto.variants_by_impact,
            'top_affected_genes': stats_dto.top_affected_genes
        })
    
    @extend_schema(
        summary="Estadísticas generales de reportes",
        description="Obtiene estadísticas globales del sistema de reportes",
        tags=['Reportes de Pacientes']
    )
    @action(detail=False, methods=['get'])
    def general_statistics(self, request):
        """Estadísticas generales del sistema"""
        total_reports = PatientVariantReport.objects.count()
        total_patients = PatientVariantReport.objects.values('patient_id').distinct().count()
        
        # Crear DTO de estadísticas generales
        stats_dto = GeneralReportStatisticsDTO(
            total_reports=total_reports,
            total_patients_with_reports=total_patients,
            average_variants_per_patient=round(total_reports / total_patients, 2) if total_patients > 0 else 0
        )
        
        return Response({
            'total_reports': stats_dto.total_reports,
            'total_patients_with_reports': stats_dto.total_patients_with_reports,
            'average_variants_per_patient': stats_dto.average_variants_per_patient
        })