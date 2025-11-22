from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from uuid import UUID

@dataclass
class GeneDTO:
    """DTO completo para Gene - Representa el objeto de dominio"""
    id: UUID
    symbol: str
    full_name: str
    function_summary: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validaciones del DTO"""
        if not self.symbol.isupper():
            raise ValueError("El símbolo del gen debe estar en mayúsculas")
        if len(self.symbol) == 0 or len(self.symbol) > 50:
            raise ValueError("El símbolo debe tener entre 1 y 50 caracteres")


@dataclass
class GeneCreateDTO:
    """DTO para creación de genes"""
    symbol: str
    full_name: str
    function_summary: str
    
    def __post_init__(self):
        """Validaciones"""
        if not self.symbol.isupper():
            raise ValueError("El símbolo del gen debe estar en mayúsculas")
        if not self.symbol or len(self.symbol) > 50:
            raise ValueError("El símbolo es requerido y debe tener máximo 50 caracteres")
        if not self.full_name or len(self.full_name) > 255:
            raise ValueError("El nombre completo es requerido y debe tener máximo 255 caracteres")
        if not self.function_summary:
            raise ValueError("El resumen de función es requerido")


@dataclass
class GeneUpdateDTO:
    """DTO para actualización de genes"""
    full_name: Optional[str] = None
    function_summary: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones"""
        if self.full_name is not None and (not self.full_name or len(self.full_name) > 255):
            raise ValueError("El nombre completo debe tener entre 1 y 255 caracteres")
        if self.function_summary is not None and not self.function_summary:
            raise ValueError("El resumen de función no puede estar vacío")


@dataclass
class GeneListDTO:
    """DTO simplificado para listados"""
    id: UUID
    symbol: str
    full_name: str
    variants_count: int = 0


@dataclass
class GeneSearchResultDTO:
    """DTO para resultados de búsqueda"""
    query: str
    count: int
    results: list[GeneListDTO] = field(default_factory=list)


@dataclass
class GeneStatisticsDTO:
    """DTO para estadísticas de genes"""
    total_genes: int
    genes_with_variants: int
    genes_without_variants: int