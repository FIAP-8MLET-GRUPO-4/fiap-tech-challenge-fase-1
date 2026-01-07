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


def get_book_by_id(db: Session, book_id: int):
    """
    Busca um livro pelo ID. Retorna None se não encontrar.
    """
    return db.query(Book).filter(Book.id == book_id).first()


def search_books_data(db: Session, title: str = None, category_name: str = None):
    """
    Busca livros filtrando por título e/ou nome da categoria.
    """
    # Inicia a query base
    # Fazemos o .join(Category) para permitir filtrar pelo nome da categoria
    query = db.query(Book).join(Category)
    
    # Se o usuário enviou um título, filtra (LIKE %termo%)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
        
    # Se enviou categoria, filtra pelo nome da categoria
    if category_name:
        query = query.filter(Category.name.ilike(f"%{category_name}%"))
        
    # Executa e retorna todos os resgistros
    return query.all()