"""
Testes de integração para os endpoints de livros.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.models.books import Book, Category


@pytest.mark.integration
class TestGetAllBooks:
    """Testes para o endpoint GET /api/v1/books/."""

    def test_get_all_books_success(self, client: TestClient, test_book: Book):
        """Testa listagem de todos os livros."""
        response = client.get("/api/v1/books/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == test_book.id
        assert data[0]["title"] == test_book.title
        assert data[0]["price"] == test_book.price
        assert data[0]["category_name"] == "Fiction"

    def test_get_all_books_with_pagination(self, client: TestClient, db_session: Session, test_category: Category):
        """Testa listagem de livros com paginação."""
        # Cria múltiplos livros
        for i in range(5):
            book = Book(
                id=i + 1,
                upc=f"123456789012{i}",
                title=f"Book {i}",
                price=10.0 + i,
                category_id=test_category.id
            )
            db_session.add(book)
        db_session.commit()

        # Testa paginação
        response = client.get("/api/v1/books/?offset=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Book 1"
        assert data[1]["title"] == "Book 2"

    def test_get_all_books_empty(self, client: TestClient):
        """Testa listagem quando não há livros."""
        response = client.get("/api/v1/books/")

        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.integration
class TestSearchBooks:
    """Testes para o endpoint GET /api/v1/books/search."""

    def test_search_by_title(self, client: TestClient, test_book: Book):
        """Testa busca de livros por título."""
        response = client.get("/api/v1/books/search?title=Test")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_book.title

    def test_search_by_category(self, client: TestClient, test_book: Book):
        """Testa busca de livros por categoria."""
        response = client.get("/api/v1/books/search?category=Fiction")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_name"] == "Fiction"

    def test_search_by_title_and_category(self, client: TestClient, test_book: Book):
        """Testa busca de livros por título e categoria."""
        response = client.get("/api/v1/books/search?title=Test&category=Fiction")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_book.title

    def test_search_no_results(self, client: TestClient, test_book: Book):
        """Testa busca sem resultados."""
        response = client.get("/api/v1/books/search?title=NonExistent")

        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.integration
class TestGetBookDetails:
    """Testes para o endpoint GET /api/v1/books/{id}."""

    def test_get_book_details_success(self, client: TestClient, test_book: Book):
        """Testa busca de detalhes de um livro existente."""
        response = client.get(f"/api/v1/books/{test_book.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_book.id
        assert data["title"] == test_book.title
        assert data["description"] == test_book.description
        assert data["price"] == test_book.price
        assert data["category_name"] == "Fiction"
        assert data["imagem_url"] == test_book.imagem_url

    def test_get_book_details_not_found(self, client: TestClient):
        """Testa busca de livro inexistente."""
        response = client.get("/api/v1/books/999")

        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]
