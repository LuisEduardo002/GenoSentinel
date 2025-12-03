from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .dtos import (
    GeneticVariantDTO, GeneticVariantCreateDTO, GeneticVariantUpdateDTO, 
    GeneticVariantListDTO, VariantsByGeneDTO, VariantsByChromosomeDTO, 
    VariantStatisticsDTO
)
from .repository import GeneticVariantRepository
from .mappers import GeneticVariantMapper

class GeneticVariantService:
    """
    Contiene la lógica de negocio para la gestión de Variantes Genéticas.
    Utiliza el Repository para el acceso a datos y opera con DTOs.
    """
    
    def __init__(self, repository: GeneticVariantRepository = None):
        self.repository = repository or GeneticVariantRepository()

    def get_all_variants(self, gene_id: Optional[UUID] = None, chromosome: Optional[str] = None, impact: Optional[str] = None) -> List[GeneticVariantListDTO]:
        """Obtiene todas las variantes y las convierte a DTOs de lista."""
        variants = self.repository.get_all(gene_id, chromosome, impact)
        return [GeneticVariantMapper.to_list_dto(v) for v in variants]

    def get_variant_by_id(self, variant_id: UUID) -> GeneticVariantDTO:
        """Obtiene una variante por ID y la convierte a DTO completo."""
        variant = self.repository.get_by_id(variant_id)
        if not variant:
            raise ObjectDoesNotExist(f"Variante con ID {variant_id} no encontrada")
        return GeneticVariantMapper.to_dto(variant)

    def create_variant(self, create_dto: GeneticVariantCreateDTO) -> GeneticVariantDTO:
        """Crea una nueva variante. Incluye validación de existencia de Gene."""
        
        # 1. Validar que el gen existe (lógica de negocio)
        gene = self.repository.get_gene_by_id(create_dto.gene_id)
        if not gene:
            raise ObjectDoesNotExist(f"Gen con ID {create_dto.gene_id} no encontrado")
            
        # 2. Crear la variante
        try:
            variant = self.repository.create(create_dto, gene)
            return GeneticVariantMapper.to_dto(variant)
        except IntegrityError as e:
            # Manejar errores de unicidad (unique_together)
            raise IntegrityError(f"Error de integridad al crear la variante: {e}")
        
    def update_variant(self, variant_id: UUID, update_dto: GeneticVariantUpdateDTO) -> GeneticVariantDTO:
        """Actualiza una variante existente."""
        variant = self.repository.get_by_id(variant_id)
        if not variant:
            raise ObjectDoesNotExist(f"Variante con ID {variant_id} no encontrada")
            
        updated_variant = self.repository.update(variant, update_dto)
        return GeneticVariantMapper.to_dto(updated_variant)

    def delete_variant(self, variant_id: UUID) -> str:
        """Elimina una variante."""
        variant = self.repository.get_by_id(variant_id)
        if not variant:
            raise ObjectDoesNotExist(f"Variante con ID {variant_id} no encontrada")
            
        gene_symbol = variant.gene.symbol
        self.repository.delete(variant)
        return gene_symbol

    def get_variants_by_gene_symbol(self, gene_symbol: str) -> VariantsByGeneDTO:
        """Obtiene variantes por símbolo de gen."""
        gene = self.repository.get_gene_by_symbol(gene_symbol)
        if not gene:
            raise ObjectDoesNotExist(f"No se encontró el gen con símbolo {gene_symbol}")
            
        variants = self.repository.get_variants_by_gene(gene)
        variant_dtos = [GeneticVariantMapper.to_list_dto(v) for v in variants]
        
        return VariantsByGeneDTO(
            gene_symbol=gene.symbol,
            gene_name=gene.full_name,
            total_variants=len(variant_dtos),
            variants=variant_dtos
        )

    def get_variants_by_chromosome(self, chromosome: str) -> VariantsByChromosomeDTO:
        """Obtiene variantes por cromosoma."""
        variants = self.repository.get_variants_by_chromosome(chromosome)
        variant_dtos = [GeneticVariantMapper.to_list_dto(v) for v in variants]
        
        return VariantsByChromosomeDTO(
            chromosome=chromosome,
            total_variants=len(variant_dtos),
            variants=variant_dtos
        )

    def get_statistics(self) -> VariantStatisticsDTO:
        """Obtiene estadísticas de variantes."""
        return self.repository.get_statistics()
