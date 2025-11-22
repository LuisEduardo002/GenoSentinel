from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal

@dataclass
class PatientClinicalDataDTO:
    """DTO para datos clínicos del paciente (del microservicio de clínica)"""
    patient_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    status: Optional[str] = None
    integration_status: str = 'pending'
    message: Optional[str] = None


@dataclass
class PatientVariantReportDTO:
    """DTO completo para Reporte de Variante de Paciente"""
    id: UUID
    patient_id: UUID
    variant_id: UUID
    gene_symbol: str
    gene_full_name: str
    chromosome: str
    position: int
    reference_base: str
    alternate_base: str
    impact: str
    detection_date: date
    allele_frequency: Decimal
    created_at: datetime
    updated_at: datetime
    clinical_data: Optional[PatientClinicalDataDTO] = None
    
    def __post_init__(self):
        """Validaciones del DTO"""
        if self.allele_frequency < Decimal('0') or self.allele_frequency > Decimal('1'):
            raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")


@dataclass
class PatientVariantReportCreateDTO:
    """DTO para creación de reportes de pacientes"""
    patient_id: UUID
    variant_id: UUID
    detection_date: date
    allele_frequency: Decimal
    
    def __post_init__(self):
        """Validaciones"""
        if not self.patient_id:
            raise ValueError("El ID del paciente es requerido")
        if not self.variant_id:
            raise ValueError("El ID de la variante es requerido")
        if not self.detection_date:
            raise ValueError("La fecha de detección es requerida")
        if self.allele_frequency < Decimal('0') or self.allele_frequency > Decimal('1'):
            raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")
        if self.detection_date > date.today():
            raise ValueError("La fecha de detección no puede ser futura")


@dataclass
class PatientVariantReportUpdateDTO:
    """DTO para actualización de reportes"""
    detection_date: Optional[date] = None
    allele_frequency: Optional[Decimal] = None
    
    def __post_init__(self):
        """Validaciones"""
        if self.allele_frequency is not None:
            if self.allele_frequency < Decimal('0') or self.allele_frequency > Decimal('1'):
                raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")
        if self.detection_date is not None:
            if self.detection_date > date.today():
                raise ValueError("La fecha de detección no puede ser futura")


@dataclass
class PatientVariantReportListDTO:
    """DTO simplificado para listados"""
    id: UUID
    patient_id: UUID
    gene_symbol: str
    chromosome: str
    impact: str
    detection_date: date
    allele_frequency: Decimal


@dataclass
class PatientReportsSummaryDTO:
    """DTO para resumen de reportes de un paciente"""
    patient_id: UUID
    total_variants: int
    clinical_summary: PatientClinicalDataDTO
    reports: list[PatientVariantReportListDTO] = field(default_factory=list)


@dataclass
class PatientStatisticsDTO:
    """DTO para estadísticas de un paciente"""
    patient_id: UUID
    total_variants: int
    average_allele_frequency: Optional[Decimal]
    variants_by_impact: list[dict] = field(default_factory=list)
    top_affected_genes: list[dict] = field(default_factory=list)


@dataclass
class GeneralReportStatisticsDTO:
    """DTO para estadísticas generales del sistema"""
    total_reports: int
    total_patients_with_reports: int
    average_variants_per_patient: float


@dataclass
class ImpactDistributionDTO:
    """DTO para distribución de impactos"""
    impact: str
    count: int
    percentage: float


@dataclass
class GeneFrequencyDTO:
    """DTO para frecuencia de genes afectados"""
    gene_symbol: str
    variant_count: int