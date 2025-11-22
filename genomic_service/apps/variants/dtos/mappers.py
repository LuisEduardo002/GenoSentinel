from typing import List
from apps.variants.models import GeneticVariant
from .variant_dto import (
    GeneticVariantDTO, GeneticVariantCreateDTO, GeneticVariantUpdateDTO,
    GeneticVariantListDTO
)

class GeneticVariantMapper:
    """Mapper para convertir entre Models y DTOs de variantes"""
    
    @staticmethod
    def to_dto(variant: GeneticVariant) -> GeneticVariantDTO:
        """Convierte Model a DTO completo"""
        return GeneticVariantDTO(
            id=variant.id,
            gene_id=variant.gene.id,
            gene_symbol=variant.gene.symbol,
            gene_full_name=variant.gene.full_name,
            chromosome=variant.chromosome,
            position=variant.position,
            reference_base=variant.reference_base,
            alternate_base=variant.alternate_base,
            impact=variant.impact,
            created_at=variant.created_at,
            updated_at=variant.updated_at
        )
    
    @staticmethod
    def to_list_dto(variant: GeneticVariant) -> GeneticVariantListDTO:
        """Convierte Model a DTO de lista"""
        return GeneticVariantListDTO(
            id=variant.id,
            gene_symbol=variant.gene.symbol,
            chromosome=variant.chromosome,
            position=variant.position,
            mutation=f"{variant.reference_base}>{variant.alternate_base}",
            impact=variant.impact
        )
    
    @staticmethod
    def to_model(dto: GeneticVariantCreateDTO, gene) -> GeneticVariant:
        """Convierte CreateDTO a Model (sin guardar)"""
        return GeneticVariant(
            gene=gene,
            chromosome=dto.chromosome,
            position=dto.position,
            reference_base=dto.reference_base.upper(),
            alternate_base=dto.alternate_base.upper(),
            impact=dto.impact
        )
    
    @staticmethod
    def update_model_from_dto(variant: GeneticVariant, dto: GeneticVariantUpdateDTO) -> GeneticVariant:
        """Actualiza un Model existente desde un UpdateDTO"""
        if dto.impact is not None:
            variant.impact = dto.impact
        if dto.reference_base is not None:
            variant.reference_base = dto.reference_base.upper()
        if dto.alternate_base is not None:
            variant.alternate_base = dto.alternate_base.upper()
        return variant
    
    @staticmethod
    def to_dto_list(variants: List[GeneticVariant]) -> List[GeneticVariantDTO]:
        """Convierte lista de Models a lista de DTOs"""
        return [GeneticVariantMapper.to_dto(variant) for variant in variants]