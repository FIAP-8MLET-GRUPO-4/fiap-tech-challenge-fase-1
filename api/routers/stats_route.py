# api/routers/stats_route.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.core.db import get_db
from api.services.stats_service import get_overview_stats, get_category_stats
from api.schemas.stats_schema import StatsOverviewResponse, CategoryStatsResponse

router = APIRouter()

@router.get("/overview", response_model=StatsOverviewResponse)
def get_stats_overview(db: Session = Depends(get_db)):
    """
    Retorna um panorama geral da base de dados:
    - Total de livros
    - Preço médio
    - Distribuição de avaliações (estrelas)
    """
    stats = get_overview_stats(db)
    return stats

@router.get("/categories", response_model=List[CategoryStatsResponse])
def get_stats_by_category(db: Session = Depends(get_db)):
    """
    Retorna estatísticas detalhadas por categoria:
    - Nome da Categoria
    - Quantidade de Livros
    - Preço Médio, Mínimo e Máximo
    """
    stats = get_category_stats(db)
    return stats