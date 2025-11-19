import uuid
from django.db import models
from apps.genes.models import Gene

class GeneticVariant(models.Model):
    IMPACT_CHOICES = [
        ('MISSENSE', 'Missense'),
        ('FRAMESHIFT', 'Frameshift'),
        ('NONSENSE', 'Nonsense'),
        ('SILENT', 'Silent'),
        ('SPLICE_SITE', 'Splice Site'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, related_name='variants')
    chromosome = models.CharField(max_length=10, help_text="Cromosoma (ej: chr17)")
    position = models.BigIntegerField(help_text="Posición en el cromosoma")
    reference_base = models.CharField(max_length=100, help_text="Base de referencia (ej: A)")
    alternate_base = models.CharField(max_length=100, help_text="Base alternativa (ej: G)")
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, help_text="Impacto de la variante")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'genetic_variants'
        ordering = ['chromosome', 'position']
        verbose_name = 'Variante Genética'
        verbose_name_plural = 'Variantes Genéticas'
        unique_together = ['gene', 'chromosome', 'position', 'reference_base', 'alternate_base']
    
    def __str__(self):
        return f"{self.gene.symbol} - {self.chromosome}:{self.position} {self.reference_base}>{self.alternate_base}"