import requests
from django.conf import settings
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class ClinicalMicroserviceClient:
    """
    Cliente para comunicación con el Microservicio de Clínica
    Maneja las llamadas HTTP y transformación de datos
    """
    
    def __init__(self):
        self.base_url = "http://localhost:3007"
        self.timeout = settings.MICROSERVICE_REQUEST_TIMEOUT
    
    def get_patient(self, patient_id: str, token: Optional[str] = None) -> Optional[Dict]:
        """
        Obtiene información de un paciente desde el microservicio de clínica
        
        Args:
            patient_id: UUID del paciente
            token: JWT token para autenticación (opcional por ahora)
        
        Returns:
            Dict con información del paciente o None si hay error
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
    
    def validate_patient_exists(self, patient_id: str, token: Optional[str] = None) -> bool:
        """
        Valida que un paciente exista en el microservicio de clínica
        
        Args:
            patient_id: UUID del paciente
            token: JWT token para autenticación
        
        Returns:
            True si el paciente existe, False en caso contrario
        """
        patient_data = self.get_patient(patient_id, token)
        return patient_data is not None
    
    def get_patient_clinical_records(self, patient_id: str, token: Optional[str] = None) -> Optional[list]:
        """
        Obtiene las historias clínicas de un paciente
        
        Args:
            patient_id: UUID del paciente
            token: JWT token para autenticación
        
        Returns:
            Lista de historias clínicas o None si hay error
        """
        try:
            url = f"{self.base_url}/clinical-records/patient/{patient_id}"
            headers = {}
            
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"No se pudieron obtener historias clínicas del paciente {patient_id}"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error al obtener historias clínicas: {str(e)}")
            return None


# Instancia global del cliente
clinical_client = ClinicalMicroserviceClient()