"""
Testes de integração para os endpoints de estatísticas.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.models.books import Book, Category


@pytest.mark.integration
class TestGetOverviewStats:
    """Testes para o endpoint GET /api/v1/stats/overview."""

    def test_overview_stats_with_books(self, client: TestClient, db_session: Session, test_category: Category):
        """Testa estatísticas gerais com livros."""
        # Cria livros com diferentes ratings
        books_data = [
            {"id": 1, "title": "Book 1", "price": 10.0, "rating": 5},
            {"id": 2, "title": "Book 2", "price": 20.0, "rating": 5},
            {"id": 3, "title": "Book 3", "price": 30.0, "rating": 4},
        ]

        for data in books_data:
            book = Book(
                id=data["id"],
                upc=f"upc{data['id']}",
                title=data["title"],
                price=data["price"],
                rating=data["rating"],
                category_id=test_category.id
            )
            db_session.add(book)
        db_session.commit()

        response = client.get("/api/v1/stats/overview")

        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 3
        assert data["average_price"] == 20.0
        assert data["rating_distribution"]["5"] == 2
        assert data["rating_distribution"]["4"] == 1

    def test_overview_stats_empty(self, client: TestClient):
        """Testa estatísticas gerais com banco vazio."""
        response = client.get("/api/v1/stats/overview")

        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 0
        assert data["average_price"] == 0.0


@pytest.mark.integration
class TestGetCategoryStats:
    """Testes para o endpoint GET /api/v1/stats/by-category."""

    def test_category_stats_with_books(self, client: TestClient, db_session: Session):
        """Testa estatísticas por categoria."""
        # Cria categorias
        cat1 = Category(id=1, name="Fiction")
        cat2 = Category(id=2, name="Science")
        db_session.add_all([cat1, cat2])
        db_session.commit()

        # Cria livros em diferentes categorias
        books_data = [
            {"id": 1, "title": "Fiction Book 1", "price": 10.0, "category_id": 1},
            {"id": 2, "title": "Fiction Book 2", "price": 20.0, "category_id": 1},
            {"id": 3, "title": "Science Book 1", "price": 30.0, "category_id": 2},
        ]

        for data in books_data:
            book = Book(
                id=data["id"],
                upc=f"upc{data['id']}",
                title=data["title"],
                price=data["price"],
                category_id=data["category_id"]
            )
            db_session.add(book)
        db_session.commit()

        response = client.get("/api/v1/stats/by-category")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Verifica estatísticas de Fiction
        fiction_stats = data[0]
        assert fiction_stats["category_name"] == "Fiction"
        assert fiction_stats["total_books"] == 2
        assert fiction_stats["average_price"] == 15.0

        # Verifica estatísticas de Science
        science_stats = data[1]
        assert science_stats["category_name"] == "Science"
        assert science_stats["total_books"] == 1
        assert science_stats["average_price"] == 30.0

    def test_category_stats_empty(self, client: TestClient):
        """Testa estatísticas por categoria com banco vazio."""
        response = client.get("/api/v1/stats/by-category")

        assert response.status_code == 200
        assert response.json() == []
