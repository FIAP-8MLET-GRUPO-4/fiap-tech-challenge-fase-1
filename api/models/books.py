from sqlalchemy import Column, Integer, Float, String, Text, Identity, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from api.core.db import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    books = relationship("Book", back_populates="category")

class Book(Base):
    __tablename__ = 'books' 
    
    id = Column(Integer, primary_key=True, autoincrement=False)
    upc = Column(String(50), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    rating = Column(Integer)
    quantity = Column(Integer)
    availability = Column(Boolean) 
    imagem_url = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="books")