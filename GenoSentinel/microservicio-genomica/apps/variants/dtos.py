from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ImpactType(str, Enum):
    MISSENSE = 'MISSENSE'
    FRAMESHIFT = 'FRAMESHIFT'
    NONSENSE = 'NONSENSE'
    SILENT = 'SILENT'
    SPLICE_SITE = 'SPLICE_SITE'

@dataclass
class GeneticVariantDTO:
    """DTO completo para GeneticVariant"""
    id: UUID
    gene_id: UUID
    gene_symbol: str
    gene_full_name: str
    chromosome: str
    position: int
    reference_base: str
    alternate_base: str
    impact: ImpactType
    created_at: datetime
    updated_at: datetime

@dataclass
class GeneticVariantCreateDTO:
    """DTO para creación de GeneticVariant"""
    gene_id: UUID
    chromosome: str
    position: int
    reference_base: str
    alternate_base: str
    impact: ImpactType

@dataclass
class GeneticVariantUpdateDTO:
    """DTO para actualización de GeneticVariant"""
    impact: Optional[ImpactType] = None
    reference_base: Optional[str] = None
    alternate_base: Optional[str] = None

@dataclass
class GeneticVariantListDTO:
    """DTO simplificado para listados de GeneticVariant"""
    id: UUID
    gene_symbol: str
    chromosome: str
    position: int
    mutation: str
    impact: ImpactType

@dataclass
class VariantsByGeneDTO:
    """DTO para resultados de variantes por gen"""
    gene_symbol: str
    gene_name: str
    total_variants: int
    variants: List[GeneticVariantListDTO] = field(default_factory=list)

@dataclass
class VariantsByChromosomeDTO:
    """DTO para resultados de variantes por cromosoma"""
    chromosome: str
    total_variants: int
    variants: List[GeneticVariantListDTO] = field(default_factory=list)

@dataclass
class VariantStatisticsDTO:
    """DTO para estadísticas de variantes"""
    total_variants: int
    by_impact: List[dict] = field(default_factory=list)
    top_chromosomes: List[dict] = field(default_factory=list)
