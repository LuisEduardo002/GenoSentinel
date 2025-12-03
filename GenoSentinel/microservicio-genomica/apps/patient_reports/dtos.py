from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal

@dataclass
class PatientClinicalDataDTO:
    """DTO para datos clínicos del paciente (del microservicio de clínica)"""
    patient_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None # Cambiado a date para consistencia
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
    
    # Las validaciones de negocio se mueven al Service o se manejan en el Serializer/DTO de entrada.
    # Se mantiene la validación de rango por ser una restricción de dominio.
    def __post_init__(self):
        if self.allele_frequency < Decimal('0') or self.allele_frequency > Decimal('1'):
            raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")


@dataclass
class PatientVariantReportCreateDTO:
    """DTO para creación de reportes de pacientes"""
    patient_id: UUID
    variant_id: UUID
    detection_date: date
    allele_frequency: Decimal
    
    # Las validaciones de negocio se mueven al Service
    pass


@dataclass
class PatientVariantReportUpdateDTO:
    """DTO para actualización de reportes"""
    detection_date: Optional[date] = None
    allele_frequency: Optional[Decimal] = None
    
    # Las validaciones de negocio se mueven al Service
    pass


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
    reports: List[PatientVariantReportListDTO] = field(default_factory=list)


@dataclass
class PatientStatisticsDTO:
    """DTO para estadísticas de un paciente"""
    patient_id: UUID
    total_variants: int
    average_allele_frequency: Optional[Decimal]
    variants_by_impact: List[dict] = field(default_factory=list)
    top_affected_genes: List[dict] = field(default_factory=list)


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
