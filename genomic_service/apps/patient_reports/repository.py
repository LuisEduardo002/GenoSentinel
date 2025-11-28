from typing import List, Optional
from uuid import UUID
from django.db.models import Count, Avg
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Trunc
from django.db import models

from apps.variants.models import GeneticVariant
from .models import PatientVariantReport
from .dtos import PatientVariantReportCreateDTO, PatientVariantReportUpdateDTO, PatientStatisticsDTO, GeneralReportStatisticsDTO
from .mappers import PatientVariantReportMapper

class PatientVariantReportRepository:
    """
    Encapsula el acceso a la base de datos para el modelo PatientVariantReport.
    """
    
    def get_all(self, patient_id: Optional[UUID] = None, gene_symbol: Optional[str] = None) -> List[PatientVariantReport]:
        """Obtiene todos los reportes, con filtros opcionales."""
        queryset = PatientVariantReport.objects.select_related(
            'variant', 'variant__gene'
        ).all()
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if gene_symbol:
            queryset = queryset.filter(variant__gene__symbol__iexact=gene_symbol)
            
        return list(queryset)

    def get_by_id(self, report_id: UUID) -> Optional[PatientVariantReport]:
        """Obtiene un reporte por su ID."""
        try:
            return PatientVariantReport.objects.select_related(
                'variant', 'variant__gene'
            ).get(pk=report_id)
        except PatientVariantReport.DoesNotExist:
            return None

    def get_variant_by_id(self, variant_id: UUID) -> Optional[GeneticVariant]:
        """Obtiene una variante por su ID (para validación de FK)."""
        try:
            return GeneticVariant.objects.select_related('gene').get(pk=variant_id)
        except GeneticVariant.DoesNotExist:
            return None

    def create(self, create_dto: PatientVariantReportCreateDTO, variant: GeneticVariant) -> PatientVariantReport:
        """Crea y guarda un nuevo reporte a partir de un DTO y un objeto GeneticVariant."""
        report = PatientVariantReportMapper.to_model(create_dto, variant)
        report.save()
        return report

    def update(self, report: PatientVariantReport, update_dto: PatientVariantReportUpdateDTO) -> PatientVariantReport:
        """Actualiza un reporte existente a partir de un DTO."""
        report = PatientVariantReportMapper.update_model_from_dto(report, update_dto)
        report.save()
        return report

    def delete(self, report: PatientVariantReport) -> None:
        """Elimina un reporte."""
        report.delete()

    def get_patient_reports(self, patient_id: UUID) -> List[PatientVariantReport]:
        """Obtiene todos los reportes de un paciente."""
        return list(PatientVariantReport.objects.filter(
            patient_id=patient_id
        ).select_related('variant', 'variant__gene'))

    def get_patient_statistics(self, patient_id: UUID) -> Optional[PatientStatisticsDTO]:
        """Calcula y retorna estadísticas de reportes para un paciente."""
        reports = PatientVariantReport.objects.filter(patient_id=patient_id)
        
        if not reports.exists():
            return None
            
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
        
        return PatientStatisticsDTO(
            patient_id=patient_id,
            total_variants=reports.count(),
            average_allele_frequency=avg_vaf['avg_vaf'],
            variants_by_impact=impact_stats,
            top_affected_genes=top_genes
        )

    def get_general_statistics(self) -> GeneralReportStatisticsDTO:
        """Calcula y retorna estadísticas generales del sistema."""
        total_reports = PatientVariantReport.objects.count()
        total_patients = PatientVariantReport.objects.values('patient_id').distinct().count()
        
        avg_variants = round(total_reports / total_patients, 2) if total_patients > 0 else 0.0
        
        return GeneralReportStatisticsDTO(
            total_reports=total_reports,
            total_patients_with_reports=total_patients,
            average_variants_per_patient=avg_variants
        )
