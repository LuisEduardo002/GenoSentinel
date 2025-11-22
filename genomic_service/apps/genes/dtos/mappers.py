from typing import List
from apps.genes.models import Gene
from .gene_dto import (
    GeneDTO, GeneCreateDTO, GeneUpdateDTO, GeneListDTO
)

class GeneMapper:
    """Mapper para convertir entre Models y DTOs"""
    
    @staticmethod
    def to_dto(gene: Gene) -> GeneDTO:
        """Convierte Model a DTO completo"""
        return GeneDTO(
            id=gene.id,
            symbol=gene.symbol,
            full_name=gene.full_name,
            function_summary=gene.function_summary,
            created_at=gene.created_at,
            updated_at=gene.updated_at
        )
    
    @staticmethod
    def to_list_dto(gene: Gene, variants_count: int = 0) -> GeneListDTO:
        """Convierte Model a DTO de lista"""
        return GeneListDTO(
            id=gene.id,
            symbol=gene.symbol,
            full_name=gene.full_name,
            variants_count=variants_count
        )
    
    @staticmethod
    def to_model(dto: GeneCreateDTO) -> Gene:
        """Convierte CreateDTO a Model (sin guardar)"""
        return Gene(
            symbol=dto.symbol,
            full_name=dto.full_name,
            function_summary=dto.function_summary
        )
    
    @staticmethod
    def update_model_from_dto(gene: Gene, dto: GeneUpdateDTO) -> Gene:
        """Actualiza un Model existente desde un UpdateDTO"""
        if dto.full_name is not None:
            gene.full_name = dto.full_name
        if dto.function_summary is not None:
            gene.function_summary = dto.function_summary
        return gene
    
    @staticmethod
    def to_dto_list(genes: List[Gene]) -> List[GeneDTO]:
        """Convierte lista de Models a lista de DTOs"""
        return [GeneMapper.to_dto(gene) for gene in genes]