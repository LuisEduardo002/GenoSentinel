from typing import List, Optional
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .dtos import (
    GeneDTO, GeneCreateDTO, GeneUpdateDTO, GeneListDTO, 
    GeneSearchResultDTO, GeneStatisticsDTO
)
from .repository import GeneRepository
from .mappers import GeneMapper

class GeneService:
    """
    Contiene la lógica de negocio para la gestión de Genes.
    Utiliza el Repository para el acceso a datos y opera con DTOs.
    """
    
    def __init__(self, repository: GeneRepository = None):
        self.repository = repository or GeneRepository()

    def get_all_genes(self, search_query: Optional[str] = None) -> GeneSearchResultDTO:
        """Obtiene todos los genes y los convierte a DTOs de lista."""
        genes = self.repository.get_all(search_query)
        
        # Para el conteo de variantes, se necesita lógica de la app variants.
        # Por ahora, se usa el campo variants_count=0 en el DTO de lista.
        # En un entorno real, se haría una consulta optimizada o se usaría un servicio de coordinación.
        gene_dtos = [GeneMapper.to_list_dto(g) for g in genes]
        
        return GeneSearchResultDTO(
            query=search_query or "",
            count=len(gene_dtos),
            results=gene_dtos
        )

    def get_gene_by_id(self, gene_id: UUID) -> GeneDTO:
        """Obtiene un gen por ID y lo convierte a DTO completo."""
        gene = self.repository.get_by_id(gene_id)
        if not gene:
            raise ObjectDoesNotExist(f"Gen con ID {gene_id} no encontrado")
        return GeneMapper.to_dto(gene)

    def create_gene(self, create_dto: GeneCreateDTO) -> GeneDTO:
        """Crea un nuevo gen. Incluye validación de unicidad de símbolo."""
        # La validación de campos ya se hizo en el Serializer/DTO
        
        # Lógica de negocio: asegurar unicidad del símbolo
        if self.repository.get_by_symbol(create_dto.symbol):
            raise IntegrityError(f"El símbolo de gen '{create_dto.symbol}' ya existe.")
            
        try:
            gene = self.repository.create(create_dto)
            return GeneMapper.to_dto(gene)
        except IntegrityError as e:
            # Re-lanzar si hay otro error de integridad (ej. DB)
            raise IntegrityError(f"Error de integridad al crear el gen: {e}")
        
    def update_gene(self, gene_id: UUID, update_dto: GeneUpdateDTO) -> GeneDTO:
        """Actualiza un gen existente."""
        gene = self.repository.get_by_id(gene_id)
        if not gene:
            raise ObjectDoesNotExist(f"Gen con ID {gene_id} no encontrado")
            
        updated_gene = self.repository.update(gene, update_dto)
        return GeneMapper.to_dto(updated_gene)

    def delete_gene(self, gene_id: UUID) -> str:
        """Elimina un gen."""
        gene = self.repository.get_by_id(gene_id)
        if not gene:
            raise ObjectDoesNotExist(f"Gen con ID {gene_id} no encontrado")
            
        gene_symbol = gene.symbol
        self.repository.delete(gene)
        return gene_symbol

    def get_statistics(self) -> GeneStatisticsDTO:
        """Obtiene estadísticas de genes."""
        return self.repository.get_statistics()
