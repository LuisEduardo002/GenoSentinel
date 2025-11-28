from typing import List, Optional, Dict
from uuid import UUID
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from decimal import Decimal

from .dtos import (
    PatientVariantReportDTO, PatientVariantReportCreateDTO, PatientVariantReportUpdateDTO, 
    PatientVariantReportListDTO, PatientReportsSummaryDTO, PatientStatisticsDTO, 
    GeneralReportStatisticsDTO, PatientClinicalDataDTO
)
from .repository import PatientVariantReportRepository
from .mappers import PatientVariantReportMapper

# Cliente para el microservicio de clínica (se asume que existe en el entorno)
# Se debe crear un archivo clinical_client.py o similar para esta clase
# Por ahora, se incluye la clase aquí para la refactorización
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ClinicalMicroserviceClient:
    """
    Cliente para comunicación con el Microservicio de Clínica
    Maneja las llamadas HTTP y transformación de datos
    """
    
    def __init__(self):
        # Se asume que settings.MICROSERVICE_REQUEST_TIMEOUT está configurado
        self.base_url = "http://localhost:3007"
        self.timeout = 5 # Valor por defecto si no hay settings
        try:
            self.timeout = settings.MICROSERVICE_REQUEST_TIMEOUT
        except:
            pass
    
    def get_patient(self, patient_id: str, token: Optional[str] = None) -> Optional[Dict]:
        """
        Obtiene información de un paciente desde el microservicio de clínica
        """
        try:
            url = f"{self.base_url}/patients/{patient_id}"
            headers = {}
            
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"Paciente {patient_id} no encontrado en microservicio clínica")
                return None
            else:
                logger.error(
                    f"Error al obtener paciente {patient_id}: "
                    f"Status {response.status_code}"
                )
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al conectar con microservicio clínica para paciente {patient_id}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión con microservicio clínica")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al obtener paciente {patient_id}: {str(e)}")
            return None

clinical_client = ClinicalMicroserviceClient()


class PatientVariantReportService:
    """
    Contiene la lógica de negocio para la gestión de Reportes de Variantes de Pacientes.
    """
    
    def __init__(self, repository: PatientVariantReportRepository = None):
        self.repository = repository or PatientVariantReportRepository()

    def _get_patient_clinical_data(self, patient_id: UUID) -> PatientClinicalDataDTO:
        """
        Lógica para obtener y mapear datos clínicos del microservicio.
        """
        patient_id_str = str(patient_id)
        clinical_data_raw = clinical_client.get_patient(patient_id_str)
        
        return PatientVariantReportMapper.create_clinical_data_dto(
            patient_id, 
            clinical_data_raw
        )

    def get_all_reports(self, patient_id: Optional[UUID] = None, gene_symbol: Optional[str] = None) -> List[PatientVariantReportListDTO]:
        """Obtiene todos los reportes y los convierte a DTOs de lista."""
        reports = self.repository.get_all(patient_id, gene_symbol)
        return [PatientVariantReportMapper.to_list_dto(r) for r in reports]

    def get_report_by_id(self, report_id: UUID) -> PatientVariantReportDTO:
        """Obtiene un reporte por ID y lo convierte a DTO completo con datos clínicos."""
        report = self.repository.get_by_id(report_id)
        if not report:
            raise ObjectDoesNotExist(f"Reporte con ID {report_id} no encontrado")
            
        clinical_data = self._get_patient_clinical_data(report.patient_id)
        
        return PatientVariantReportMapper.to_dto(report, clinical_data)

    def create_report(self, create_dto: PatientVariantReportCreateDTO) -> PatientVariantReportDTO:
        """Crea un nuevo reporte. Incluye validaciones de negocio."""
        
        # 1. Validaciones de negocio (ej. fecha no futura, VAF en rango)
        if create_dto.detection_date > date.today():
            raise ValueError("La fecha de detección no puede ser futura")
        if create_dto.allele_frequency < Decimal('0') or create_dto.allele_frequency > Decimal('1'):
            raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")
            
        # 2. Validar que la variante existe (FK)
        variant = self.repository.get_variant_by_id(create_dto.variant_id)
        if not variant:
            raise ObjectDoesNotExist(f"Variante con ID {create_dto.variant_id} no encontrada")
            
        # 3. Validar que el paciente existe en Microservicio Clínica (Lógica de negocio)
        # Se asume que el microservicio de clínica es la fuente de verdad para la existencia del paciente
        clinical_data = clinical_client.get_patient(str(create_dto.patient_id))
        if not clinical_data:
            raise ObjectDoesNotExist(f"Paciente con ID {create_dto.patient_id} no encontrado en sistema clínico")
            
        # 4. Crear el reporte
        try:
            report = self.repository.create(create_dto, variant)
            
            # 5. Obtener datos clínicos para el DTO de respuesta
            clinical_data_dto = PatientVariantReportMapper.create_clinical_data_dto(
                report.patient_id, clinical_data
            )
            
            return PatientVariantReportMapper.to_dto(report, clinical_data_dto)
        except IntegrityError as e:
            # Manejar errores de unicidad (unique_together)
            raise IntegrityError(f"Error de integridad al crear el reporte: {e}")
        
    def update_report(self, report_id: UUID, update_dto: PatientVariantReportUpdateDTO) -> PatientVariantReportDTO:
        """Actualiza un reporte existente."""
        report = self.repository.get_by_id(report_id)
        if not report:
            raise ObjectDoesNotExist(f"Reporte con ID {report_id} no encontrado")
            
        # Validaciones de negocio
        if update_dto.detection_date and update_dto.detection_date > date.today():
            raise ValueError("La fecha de detección no puede ser futura")
        if update_dto.allele_frequency is not None and (update_dto.allele_frequency < Decimal('0') or update_dto.allele_frequency > Decimal('1')):
            raise ValueError("La frecuencia alélica (VAF) debe estar entre 0 y 1")
            
        updated_report = self.repository.update(report, update_dto)
        
        clinical_data = self._get_patient_clinical_data(updated_report.patient_id)
        
        return PatientVariantReportMapper.to_dto(updated_report, clinical_data)

    def delete_report(self, report_id: UUID) -> UUID:
        """Elimina un reporte."""
        report = self.repository.get_by_id(report_id)
        if not report:
            raise ObjectDoesNotExist(f"Reporte con ID {report_id} no encontrado")
            
        patient_id = report.patient_id
        self.repository.delete(report)
        return patient_id

    def get_reports_by_patient(self, patient_id: UUID) -> PatientReportsSummaryDTO:
        """Obtiene todos los reportes de un paciente y su resumen clínico."""
        reports = self.repository.get_patient_reports(patient_id)
        
        if not reports:
            # Se podría lanzar una excepción o retornar un DTO vacío, 
            # pero el ViewSet original retornaba 404 si no había reportes.
            raise ObjectDoesNotExist(f"No se encontraron reportes para el paciente {patient_id}")
            
        report_dtos = [PatientVariantReportMapper.to_list_dto(r) for r in reports]
        clinical_data = self._get_patient_clinical_data(patient_id)
        
        return PatientReportsSummaryDTO(
            patient_id=patient_id,
            total_variants=len(report_dtos),
            clinical_summary=clinical_data,
            reports=report_dtos
        )

    def get_patient_statistics(self, patient_id: UUID) -> PatientStatisticsDTO:
        """Obtiene estadísticas de variantes por paciente."""
        stats_dto = self.repository.get_patient_statistics(patient_id)
        
        if not stats_dto:
            raise ObjectDoesNotExist(f"No se encontraron reportes para el paciente {patient_id}")
            
        return stats_dto

    def get_general_statistics(self) -> GeneralReportStatisticsDTO:
        """Obtiene estadísticas generales del sistema."""
        return self.repository.get_general_statistics()
