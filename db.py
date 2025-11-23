from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql+psycopg2://fiap:0J74m%24c5W3vb@localhost:5432/bookstore"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# cria tabelas
Base.metadata.create_all(engine)
