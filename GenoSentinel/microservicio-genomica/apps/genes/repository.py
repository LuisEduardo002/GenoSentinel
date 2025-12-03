from typing import List, Optional
from uuid import UUID
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Gene
from .dtos import GeneCreateDTO, GeneUpdateDTO, GeneStatisticsDTO
from .mappers import GeneMapper

class GeneRepository:
    """
    Encapsula el acceso a la base de datos para el modelo Gene.
    Retorna Models o DTOs según sea necesario para la capa de Service.
    """
    
    def get_all(self, search_query: Optional[str] = None) -> List[Gene]:
        """Obtiene todos los genes, con búsqueda opcional."""
        queryset = Gene.objects.all()
        
        if search_query:
            queryset = queryset.filter(
                Q(symbol__icontains=search_query) |
                Q(full_name__icontains=search_query)
            )
            
        return list(queryset)

    def get_by_id(self, gene_id: UUID) -> Optional[Gene]:
        """Obtiene un gen por su ID."""
        try:
            return Gene.objects.get(pk=gene_id)
        except Gene.DoesNotExist:
            return None

    def get_by_symbol(self, symbol: str) -> Optional[Gene]:
        """Obtiene un gen por su símbolo."""
        try:
            return Gene.objects.get(symbol__iexact=symbol)
        except Gene.DoesNotExist:
            return None

    def create(self, create_dto: GeneCreateDTO) -> Gene:
        """Crea y guarda un nuevo gen a partir de un DTO."""
        gene = GeneMapper.to_model(create_dto)
        gene.save()
        return gene

    def update(self, gene: Gene, update_dto: GeneUpdateDTO) -> Gene:
        """Actualiza un gen existente a partir de un DTO."""
        gene = GeneMapper.update_model_from_dto(gene, update_dto)
        gene.save()
        return gene

    def delete(self, gene: Gene) -> None:
        """Elimina un gen."""
        gene.delete()

    def get_statistics(self) -> GeneStatisticsDTO:
        """Calcula y retorna estadísticas de genes."""
        total_genes = Gene.objects.count()
        
        # Se asume que el modelo GeneticVariant está disponible para contar variantes
        # Si no lo está, esta parte debe ser manejada por un servicio que coordine ambas apps.
        # Por ahora, se asume que se puede acceder a GeneticVariant para el conteo.
        # Si GeneticVariant no está en esta app, se debe ajustar la importación.
        # Para el propósito de esta refactorización, se simula el conteo.
        
        # Nota: Para un diseño más limpio, el conteo de variantes debería ser
        # responsabilidad de un servicio de la app 'variants' o un servicio de coordinación.
        # Sin embargo, para mantener la funcionalidad original, se simula.
        
        # Simulación de conteo (se asume que GeneticVariant está en apps.variants.models)
        try:
            from apps.variants.models import GeneticVariant
            genes_with_variants_count = Gene.objects.filter(variants__isnull=False).distinct().count()
        except (ImportError, ObjectDoesNotExist):
            # Si la app variants no existe o el modelo no está disponible, se asume 0
            genes_with_variants_count = 0
            
        genes_without_variants_count = total_genes - genes_with_variants_count
        
        return GeneStatisticsDTO(
            total_genes=total_genes,
            genes_with_variants=genes_with_variants_count,
            genes_without_variants=genes_without_variants_count
        )
