# api/services/stats_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.books import Book, Category

def get_overview_stats(db: Session):
    """
    Calcula estatísticas gerais da coleção.
    """
    # 1. Total de Livros
    total_books = db.query(Book).count()
    
    # 2. Preço Médio (func.avg)
    # O scalar() pega o valor único do resultado. Se não tiver livros, retorna None, então tratamos com 'or 0.0'
    avg_price = db.query(func.avg(Book.price)).scalar() or 0.0
    
    # 3. Distribuição de Ratings (Group By)
    # SQL equivalente: SELECT rating, COUNT(*) FROM books GROUP BY rating;
    rating_query = db.query(Book.rating, func.count(Book.id)).group_by(Book.rating).all()
    
    # Transforma a lista de tuplas [(5, 10), (4, 2)] em um dicionário {5: 10, 4: 2}
    # Filtramos ratings nulos caso existam
    rating_dist = {r: count for r, count in rating_query if r is not None}
    
    # Garante que notas de 1 a 5 apareçam mesmo se estiverem zeradas
    for star in range(1, 6):
        if star not in rating_dist:
            rating_dist[star] = 0
            
    return {
        "total_books": total_books,
        "average_price": round(avg_price, 2), 
        "rating_distribution": rating_dist
    }


def get_category_stats(db: Session):
    """
    Calcula estatísticas agrupadas por categoria.
    SQL equivalente:
    SELECT c.name, COUNT(b.id), AVG(b.price), MIN(b.price), MAX(b.price)
    FROM categories c
    JOIN books b ON c.id = b.category_id
    GROUP BY c.id
    ORDER BY c.name;
    """
    results = db.query(
        Category.name,
        func.count(Book.id).label("total_books"),
        func.avg(Book.price).label("avg_price"),
        func.min(Book.price).label("min_price"),
        func.max(Book.price).label("max_price")
    ).join(Book).group_by(Category.id).order_by(Category.name).all()
    
    # O SQLAlchemy retorna uma lista de tuplas (Row objects).
    # Vamos converter para uma lista de dicionários para o Pydantic entender.
    formatted_results = []
    
    for row in results:
        # row é tipo: ('Fiction', 10, 45.50, 10.00, 99.00)
        formatted_results.append({
            "category_name": row[0],
            "total_books": row[1],
            "average_price": round(row[2], 2) if row[2] else 0.0,
            "min_price": row[3] or 0.0,
            "max_price": row[4] or 0.0
        })
        
    return formatted_results