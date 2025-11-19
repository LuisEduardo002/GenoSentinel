import uuid
from django.db import models

class Gene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symbol = models.CharField(max_length=50, unique=True, help_text="Símbolo del gen (ej: BRCA1)")
    full_name = models.CharField(max_length=255, help_text="Nombre completo del gen")
    function_summary = models.TextField(help_text="Resumen de la función del gen")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'genes'
        ordering = ['symbol']
        verbose_name = 'Gen'
        verbose_name_plural = 'Genes'
    
    def __str__(self):
        return f"{self.symbol} - {self.full_name}"