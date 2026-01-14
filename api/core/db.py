from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Verifica modo de teste ANTES de usar DATABASE_URL do ambiente
if os.getenv("TESTING") == "true":
    # Para testes, usa SQLite em memória (será sobrescrito pelo conftest.py)
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL não definido no arquivo .env")

engine = create_engine(
    DATABASE_URL,
    echo=False,  # echo=False para testes mais limpos
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

from api.models import users, books, prediction_log

def init_db():
    #from api.models import users, books
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Cria uma sessão de banco de dados para cada requisição
    e garante que ela seja fechada ao final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

