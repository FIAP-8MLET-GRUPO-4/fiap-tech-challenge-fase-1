# api/routers/category_route.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api.core.db import get_db
from api.services.category_service import list_all_categories
from api.schemas.category_schema import CategoryResponse

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Lista todas as categorias de livros disponíveis.
    """
    return list_all_categories(db)