# api/schemas/stats_schema.py
from pydantic import BaseModel
from typing import Dict, List

class StatsOverviewResponse(BaseModel):
    total_books: int
    average_price: float
    # Retornaremos um dicionário onde a chave é a nota (1-5) e o valor é a qtd de livros
    # Ex: {5: 120, 4: 85, ...}
    rating_distribution: Dict[int, int]

class CategoryStatsResponse(BaseModel):
    category_name: str
    total_books: int
    average_price: float
    min_price: float
    max_price: float

    class Config:
        from_attributes = True    