# api/routers/stats_route.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from api.core.db import get_db
from api.services.stats_service import get_overview_stats, get_category_stats
from api.schemas.stats_schema import StatsOverviewResponse, CategoryStatsResponse
from api.models.books import Book

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

@router.get("/top-rated", response_model=List[dict])
def get_top_rated_books(
    limit: int = Query(10, description="Number of top-rated books to return"),
    min_rating: float = Query(4.0, description="Minimum rating to consider (1-5)"),
    db: Session = Depends(get_db)
):
    """
    Retorna os livros mais bem avaliados.
    
    Args:
        limit: Número máximo de livros a retornar
        min_rating: Avaliação mínima (1-5) para considerar um livro como bem avaliado
        
    Returns:
        Lista de dicionários contendo informações dos livros mais bem avaliados
    """
    if not 1 <= min_rating <= 5:
        raise HTTPException(status_code=400, detail="A avaliação mínima deve estar entre 1 e 5")
    
    top_books = db.query(Book)\
        .filter(Book.rating >= min_rating)\
        .order_by(Book.rating.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "id": book.id,
            "title": book.title,
            "rating": book.rating,
            "price": book.price,
            "category": book.category.name if book.category else None,   
            "category_id": book.category_id if book.category else None,  
        }
        for book in top_books
    ]

@router.get("/price-range", response_model=List[dict])
def get_books_by_price_range(
    min_price: float = Query(..., description="Preço mínimo"),
    max_price: float = Query(..., description="Preço máximo"),
    limit: int = Query(100, description="Número máximo de livros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Retorna livros dentro de uma faixa de preço específica.
    
    Args:
        min_price: Preço mínimo
        max_price: Preço máximo
        limit: Número máximo de livros a retornar
        
    Returns:
        Lista de dicionários contendo informações dos livros na faixa de preço
    """
    if min_price < 0 or max_price < 0:
        raise HTTPException(status_code=400, detail="Os preços não podem ser negativos")
    
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="O preço mínimo não pode ser maior que o preço máximo")
    
    books_in_range = db.query(Book)\
        .filter(Book.price.between(min_price, max_price))\
        .order_by(Book.price.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "id": book.id,
            "title": book.title,
            "price": book.price,
            "rating": book.rating,
            "category": book.category.name if book.category else None,   
            "category_id": book.category_id if book.category else None, 
        }
        for book in books_in_range
    ]