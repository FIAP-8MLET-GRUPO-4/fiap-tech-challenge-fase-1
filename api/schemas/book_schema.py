# api/schemas/book_schema.py
from pydantic import BaseModel
from typing import Optional

# Define como o dado será apresentado no JSON de resposta
class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    availability: bool
    quantity: int
    rating: int
    upc: str
    category_name: Optional[str] = None # Podemos retornar o nome da categoria para facilitar
    
    # Configuração necessária para o Pydantic ler objetos do SQLAlchemy (ORM)
    class Config:
        from_attributes = True
