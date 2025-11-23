from sqlalchemy import Column, Integer, Float, String, Identity
from api.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        Identity(always=False),
        primary_key=True,
    )
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)