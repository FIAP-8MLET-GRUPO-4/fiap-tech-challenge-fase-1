"""
Configuração compartilhada de fixtures para testes.
"""
import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from main import app
from api.core.db import Base, get_db
from api.models.users import User
from api.models.books import Book, Category
from api.core.security import hash_password


# Database URL para testes (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """Cria uma engine de banco de dados de teste."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Cria uma sessão de banco de dados para testes."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Cria um cliente de teste do FastAPI."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Cria um usuário de teste no banco de dados."""
    user = User(
        username="testuser",
        password=hash_password("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_category(db_session: Session) -> Category:
    """Cria uma categoria de teste no banco de dados."""
    category = Category(
        id=1,
        name="Fiction"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_book(db_session: Session, test_category: Category) -> Book:
    """Cria um livro de teste no banco de dados."""
    book = Book(
        id=1,
        upc="1234567890123",
        title="Test Book",
        description="A test book description",
        price=29.99,
        rating=4,
        quantity=10,
        availability=True,
        imagem_url="http://example.com/image.jpg",
        category_id=test_category.id
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


@pytest.fixture
def auth_token(client: TestClient, test_user: User) -> str:
    """Obtém um token de autenticação válido."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Retorna headers com autenticação."""
    return {"Authorization": f"Bearer {auth_token}"}
