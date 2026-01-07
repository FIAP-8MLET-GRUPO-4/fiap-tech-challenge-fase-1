# api/routers/book_route.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from api.core.db import get_db
from api.services.book_service import list_books, get_book_by_id, search_books_data
from api.schemas.book_schema import BookResponse, BookDetailResponse

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


@router.get("/search", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = Query(None, description="Título do livro (busca parcial)"),
    category: Optional[str] = Query(None, description="Nome da categoria"),
    db: Session = Depends(get_db)
):
    """
    Busca livros por título ou categoria.
    Exemplo: /search?title=Harry&category=Fiction
    """
    results = search_books_data(db, title=title, category_name=category)
    
    # Mapeamento para o Schema (igual ao list_books)
    response_data = []
    for book in results:
        response_data.append(BookResponse(
            id=book.id,
            title=book.title,
            price=book.price,
            availability=book.availability,
            quantity=book.quantity,
            rating=book.rating,
            upc=book.upc,
            category_name=book.category.name if book.category else "Unknown"
        ))
        
    return response_data


@router.get("/{id}", response_model=BookDetailResponse)
def get_book_details(id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os detalhes de um livro específico.
    """
    book = get_book_by_id(db, id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Mapeamento manual para garantir o category_name e campos extras
    # (O Pydantic faria automático se os nomes fossem idênticos, mas category_name é derivado)
    return BookDetailResponse(
        id=book.id,
        title=book.title,
        price=book.price,
        availability=book.availability,
        quantity=book.quantity,
        rating=book.rating,
        upc=book.upc,
        category_name=book.category.name if book.category else "Unknown",
        # Campos extras do detalhe:
        description=book.description,
        imagem_url=book.imagem_url
    )

