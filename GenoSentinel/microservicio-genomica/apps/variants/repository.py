from typing import List, Optional
from uuid import UUID
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

from apps.genes.models import Gene
from .models import GeneticVariant
from .dtos import GeneticVariantCreateDTO, GeneticVariantUpdateDTO, VariantStatisticsDTO
from .mappers import GeneticVariantMapper

class GeneticVariantRepository:
    """
    Encapsula el acceso a la base de datos para el modelo GeneticVariant.
    Retorna Models o DTOs según sea necesario para la capa de Service.
    """
    
    def get_all(self, gene_id: Optional[UUID] = None, chromosome: Optional[str] = None, impact: Optional[str] = None) -> List[GeneticVariant]:
        """Obtiene todas las variantes, con filtros opcionales."""
        queryset = GeneticVariant.objects.select_related('gene').all()
        
        if gene_id:
            queryset = queryset.filter(gene_id=gene_id)
        if chromosome:
            queryset = queryset.filter(chromosome=chromosome)
        if impact:
            queryset = queryset.filter(impact=impact)
            
        return list(queryset)

    def get_by_id(self, variant_id: UUID) -> Optional[GeneticVariant]:
        """Obtiene una variante por su ID."""
        try:
            return GeneticVariant.objects.select_related('gene').get(pk=variant_id)
        except GeneticVariant.DoesNotExist:
            return None

    def get_gene_by_id(self, gene_id: UUID) -> Optional[Gene]:
        """Obtiene un gen por su ID (para validación de FK)."""
        try:
            return Gene.objects.get(pk=gene_id)
        except Gene.DoesNotExist:
            return None

    def get_gene_by_symbol(self, symbol: str) -> Optional[Gene]:
        """Obtiene un gen por su símbolo (para consultas)."""
        try:
            return Gene.objects.get(symbol__iexact=symbol)
        except Gene.DoesNotExist:
            return None

    def create(self, create_dto: GeneticVariantCreateDTO, gene: Gene) -> GeneticVariant:
        """Crea y guarda una nueva variante a partir de un DTO y un objeto Gene."""
        variant = GeneticVariantMapper.to_model(create_dto, gene)
        variant.save()
        return variant

    def update(self, variant: GeneticVariant, update_dto: GeneticVariantUpdateDTO) -> GeneticVariant:
        """Actualiza una variante existente a partir de un DTO."""
        variant = GeneticVariantMapper.update_model_from_dto(variant, update_dto)
        variant.save()
        return variant

    def delete(self, variant: GeneticVariant) -> None:
        """Elimina una variante."""
        variant.delete()

    def get_variants_by_gene(self, gene: Gene) -> List[GeneticVariant]:
        """Obtiene todas las variantes asociadas a un gen."""
        return list(GeneticVariant.objects.filter(gene=gene).select_related('gene'))

    def get_variants_by_chromosome(self, chromosome: str) -> List[GeneticVariant]:
        """Obtiene todas las variantes en un cromosoma."""
        return list(GeneticVariant.objects.filter(chromosome=chromosome).select_related('gene'))

    def get_statistics(self) -> VariantStatisticsDTO:
        """Calcula y retorna estadísticas de variantes."""
        total_variants = GeneticVariant.objects.count()
        
        impact_stats = list(
            GeneticVariant.objects.values('impact').annotate(count=Count('id'))
        )
        
        chromosome_stats = list(
            GeneticVariant.objects.values('chromosome').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
        )
        
        return VariantStatisticsDTO(
            total_variants=total_variants,
            by_impact=impact_stats,
            top_chromosomes=chromosome_stats
        )
