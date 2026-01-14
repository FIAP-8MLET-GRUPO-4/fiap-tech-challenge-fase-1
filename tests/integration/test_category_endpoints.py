"""
Testes de integração para os endpoints de categorias.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.models.books import Category


@pytest.mark.integration
class TestGetAllCategories:
    """Testes para o endpoint GET /api/v1/categories/."""

    def test_get_all_categories_success(self, client: TestClient, test_category: Category):
        """Testa listagem de todas as categorias."""
        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == test_category.id
        assert data[0]["name"] == test_category.name

    def test_get_all_categories_ordered(self, client: TestClient, db_session: Session):
        """Testa que categorias são retornadas em ordem alfabética."""
        # Cria categorias em ordem não alfabética
        categories = [
            Category(id=1, name="Zebra"),
            Category(id=2, name="Apple"),
            Category(id=3, name="Mango")
        ]
        for cat in categories:
            db_session.add(cat)
        db_session.commit()

        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Apple"
        assert data[1]["name"] == "Mango"
        assert data[2]["name"] == "Zebra"

    def test_get_all_categories_empty(self, client: TestClient):
        """Testa listagem quando não há categorias."""
        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        assert response.json() == []
