from typing import List
from decimal import Decimal
from apps.patient_reports.models import PatientVariantReport
from .report_dto import (
    PatientVariantReportDTO, PatientVariantReportCreateDTO,
    PatientVariantReportUpdateDTO, PatientVariantReportListDTO,
    PatientClinicalDataDTO
)

class PatientVariantReportMapper:
    """Mapper para convertir entre Models y DTOs de reportes"""
    
    @staticmethod
    def to_dto(report: PatientVariantReport, clinical_data: PatientClinicalDataDTO = None) -> PatientVariantReportDTO:
        """Convierte Model a DTO completo"""
        return PatientVariantReportDTO(
            id=report.id,
            patient_id=report.patient_id,
            variant_id=report.variant.id,
            gene_symbol=report.variant.gene.symbol,
            gene_full_name=report.variant.gene.full_name,
            chromosome=report.variant.chromosome,
            position=report.variant.position,
            reference_base=report.variant.reference_base,
            alternate_base=report.variant.alternate_base,
            impact=report.variant.impact,
            detection_date=report.detection_date,
            allele_frequency=report.allele_frequency,
            created_at=report.created_at,
            updated_at=report.updated_at,
            clinical_data=clinical_data
        )
    
    @staticmethod
    def to_list_dto(report: PatientVariantReport) -> PatientVariantReportListDTO:
        """Convierte Model a DTO de lista"""
        return PatientVariantReportListDTO(
            id=report.id,
            patient_id=report.patient_id,
            gene_symbol=report.variant.gene.symbol,
            chromosome=report.variant.chromosome,
            impact=report.variant.impact,
            detection_date=report.detection_date,
            allele_frequency=report.allele_frequency
        )
    
    @staticmethod
    def to_model(dto: PatientVariantReportCreateDTO, variant) -> PatientVariantReport:
        """Convierte CreateDTO a Model (sin guardar)"""
        return PatientVariantReport(
            patient_id=dto.patient_id,
            variant=variant,
            detection_date=dto.detection_date,
            allele_frequency=dto.allele_frequency
        )
    
    @staticmethod
    def update_model_from_dto(report: PatientVariantReport, dto: PatientVariantReportUpdateDTO) -> PatientVariantReport:
        """Actualiza un Model existente desde un UpdateDTO"""
        if dto.detection_date is not None:
            report.detection_date = dto.detection_date
        if dto.allele_frequency is not None:
            report.allele_frequency = dto.allele_frequency
        return report
    
    @staticmethod
    def to_dto_list(reports: List[PatientVariantReport]) -> List[PatientVariantReportDTO]:
        """Convierte lista de Models a lista de DTOs"""
        return [PatientVariantReportMapper.to_dto(report) for report in reports]
    
    @staticmethod
    def create_clinical_data_dto(patient_id, data: dict = None) -> PatientClinicalDataDTO:
        """Crea un DTO de datos clínicos desde respuesta del microservicio"""
        if data is None:
            return PatientClinicalDataDTO(
                patient_id=patient_id,
                integration_status='pending',
                message='Integración con microservicio de clínica pendiente'
            )
        
        return PatientClinicalDataDTO(
            patient_id=patient_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            status=data.get('status'),
            integration_status='success',
            message=None
        )