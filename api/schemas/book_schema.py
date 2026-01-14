# api/schemas/book_schema.py
from pydantic import BaseModel
from typing import Optional

# Define como o dado será apresentado no JSON de resposta
class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    availability: Optional[bool] = None
    quantity: Optional[int] = None
    rating: Optional[int] = None
    upc: str
    category_name: Optional[str] = None # Podemos retornar o nome da categoria para facilitar
    
    # Configuração necessária para o Pydantic ler objetos do SQLAlchemy (ORM)
    class Config:
        from_attributes = True

# Herda de BookResponse, então já tem todos os campos acima
class BookDetailResponse(BookResponse):
    description: Optional[str] = None
    imagem_url: Optional[str] = None