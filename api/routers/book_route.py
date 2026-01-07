# api/routers/book_route.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from api.core.db import get_db
from api.services.book_service import list_books
from api.schemas.book_schema import BookResponse

# O prefixo será definido no main.py para ficar flexível
router = APIRouter()

@router.get("/", response_model=List[BookResponse])
def get_all_books(
    offset: int = Query(0, description="Registros para pular (paginação)"),
    limit: int = Query(100, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de livros disponíveis na base de dados.
    """
    books = list_books(db, offset=offset, limit=limit)
    
    results = []
    for book in books:
        # Cria o objeto de resposta preenchendo o nome da categoria
        book_resp = BookResponse(
            id=book.id,
            title=book.title,
            price=book.price,
            availability=book.availability,
            quantity=book.quantity,
            rating=book.rating,
            upc=book.upc,
            # Se a relação estiver carregada:
            category_name=book.category.name if book.category else "Unknown"
        )
        results.append(book_resp)
        
    return results