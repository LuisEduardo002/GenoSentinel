from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class ImpactType(str, Enum):
    """Enum para tipos de impacto"""
    MISSENSE = 'MISSENSE'
    FRAMESHIFT = 'FRAMESHIFT'
    NONSENSE = 'NONSENSE'
    SILENT = 'SILENT'
    SPLICE_SITE = 'SPLICE_SITE'


@dataclass
class GeneticVariantDTO:
    """DTO completo para Variante Genética"""
    id: UUID
    gene_id: UUID
    gene_symbol: str
    gene_full_name: str
    chromosome: str
    position: int
    reference_base: str
    alternate_base: str
    impact: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validaciones del DTO"""
        if not self.chromosome.startswith('chr'):
            raise ValueError("El cromosoma debe comenzar con 'chr'")
        if self.position <= 0:
            raise ValueError("La posición debe ser un número positivo")
        self._validate_bases()
    
    def _validate_bases(self):
        """Valida que las bases sean correctas"""
        valid_bases = set('ATCG')
        if not set(self.reference_base.upper()).issubset(valid_bases):
            raise ValueError("Base de referencia inválida. Debe contener solo A, T, C, G")
        if not set(self.alternate_base.upper()).issubset(valid_bases):
            raise ValueError("Base alternativa inválida. Debe contener solo A, T, C, G")


@dataclass
class GeneticVariantCreateDTO:
    """DTO para creación de variantes genéticas"""
    gene_id: UUID
    chromosome: str
    position: int
    reference_base: str
    alternate_base: str
    impact: str
    
    def __post_init__(self):
        """Validaciones"""
        if not self.chromosome.startswith('chr'):
            raise ValueError("El cromosoma debe comenzar con 'chr' (ej: chr17)")
        if self.position <= 0:
            raise ValueError("La posición debe ser un número positivo")
        if self.impact not in [e.value for e in ImpactType]:
            raise ValueError(f"Impacto inválido. Debe ser uno de: {[e.value for e in ImpactType]}")
        self._validate_bases()
    
    def _validate_bases(self):
        """Valida que las bases sean correctas"""
        valid_bases = set('ATCG')
        ref = self.reference_base.upper()
        alt = self.alternate_base.upper()
        
        if not set(ref).issubset(valid_bases):
            raise ValueError("Base de referencia inválida. Debe contener solo A, T, C, G")
        if not set(alt).issubset(valid_bases):
            raise ValueError("Base alternativa inválida. Debe contener solo A, T, C, G")
        if not ref or not alt:
            raise ValueError("Las bases de referencia y alternativa son requeridas")


@dataclass
class GeneticVariantUpdateDTO:
    """DTO para actualización de variantes"""
    impact: Optional[str] = None
    reference_base: Optional[str] = None
    alternate_base: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones"""
        if self.impact is not None and self.impact not in [e.value for e in ImpactType]:
            raise ValueError(f"Impacto inválido. Debe ser uno de: {[e.value for e in ImpactType]}")
        
        valid_bases = set('ATCG')
        if self.reference_base is not None:
            if not set(self.reference_base.upper()).issubset(valid_bases):
                raise ValueError("Base de referencia inválida")
        if self.alternate_base is not None:
            if not set(self.alternate_base.upper()).issubset(valid_bases):
                raise ValueError("Base alternativa inválida")


@dataclass
class GeneticVariantListDTO:
    """DTO simplificado para listados"""
    id: UUID
    gene_symbol: str
    chromosome: str
    position: int
    mutation: str  # Formato: "A>G"
    impact: str


@dataclass
class VariantsByGeneDTO:
    """DTO para variantes agrupadas por gen"""
    gene_symbol: str
    gene_name: str
    total_variants: int
    variants: list[GeneticVariantListDTO] = field(default_factory=list)


@dataclass
class VariantsByChromosomeDTO:
    """DTO para variantes por cromosoma"""
    chromosome: str
    total_variants: int
    variants: list[GeneticVariantListDTO] = field(default_factory=list)


@dataclass
class VariantStatisticsDTO:
    """DTO para estadísticas de variantes"""
    total_variants: int
    by_impact: list[dict] = field(default_factory=list)
    top_chromosomes: list[dict] = field(default_factory=list)