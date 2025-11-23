from sqlalchemy import Column, Integer, Float, String, Identity
from api.core.db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(
        Integer,
        Identity(always=False),
        primary_key=True,
    )
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    availability = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(255), nullable=False)