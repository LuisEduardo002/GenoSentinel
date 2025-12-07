from dataclasses import dataclass, field
from typing import Optional, List
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

@dataclass
class GeneCreateDTO:
    """DTO para creación de genes"""
    symbol: str
    full_name: str
    function_summary: str

@dataclass
class GeneUpdateDTO:
    """DTO para actualización de genes"""
    symbol: Optional[str] = None
    full_name: Optional[str] = None
    function_summary: Optional[str] = None

@dataclass
class GeneListDTO:
    """DTO simplificado para listados"""
    id: UUID
    symbol: str
    full_name: str
    variants_count: int = 0 # Se asume que esta información se puede obtener en el service/repository

@dataclass
class GeneSearchResultDTO:
    """DTO para resultados de búsqueda"""
    query: str
    count: int
    results: List[GeneListDTO] = field(default_factory=list)

@dataclass
class GeneStatisticsDTO:
    """DTO para estadísticas de genes"""
    total_genes: int
    genes_with_variants: int
    genes_without_variants: int
