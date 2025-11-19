import uuid
from django.db import models
from apps.variants.models import GeneticVariant

class PatientVariantReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.UUIDField(help_text="ID del paciente (del microservicio de clínica)")
    variant = models.ForeignKey(GeneticVariant, on_delete=models.CASCADE, related_name='patient_reports')
    detection_date = models.DateField(help_text="Fecha de detección de la variante")
    allele_frequency = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        help_text="Frecuencia alélica (VAF) entre 0 y 1"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patient_variant_reports'
        ordering = ['-detection_date']
        verbose_name = 'Reporte de Variante del Paciente'
        verbose_name_plural = 'Reportes de Variantes de Pacientes'
        unique_together = ['patient_id', 'variant', 'detection_date']
    
    def __str__(self):
        return f"Reporte {self.patient_id} - {self.variant.gene.symbol}"