# api/services/book_service.py
from sqlalchemy.orm import Session
from api.models.books import Book, Category

def list_books(db: Session, offset: int = 0, limit: int = 100):
    """
    Busca livros com paginação.
    :param offset: (int): A partir de qual registro começar, padrão 0
    :param limit (int): Quantos registros retornar (padrão 100)
    """
    
    books = db.query(Book).offset(offset).limit(limit).all()
    
    return books