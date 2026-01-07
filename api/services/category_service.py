# api/services/category_service.py
from sqlalchemy.orm import Session
from api.models.books import Category

def list_all_categories(db: Session):
    """
    Retorna todas as categorias cadastradas, ordenadas alfabeticamente.
    """
    return db.query(Category).order_by(Category.name).all()