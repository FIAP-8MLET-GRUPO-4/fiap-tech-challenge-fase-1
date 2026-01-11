"""
Testes unitários para o stats_service.
"""
import pytest
from sqlalchemy.orm import Session

from api.services import stats_service
from api.models.books import Book, Category


@pytest.mark.unit
class TestGetOverviewStats:
    """Testes para a função get_overview_stats."""

    def test_overview_stats_with_books(self, db_session: Session, test_category: Category):
        """Testa estatísticas gerais com livros."""
        # Cria livros com diferentes ratings e preços
        books_data = [
            {"id": 1, "title": "Book 1", "price": 10.0, "rating": 5},
            {"id": 2, "title": "Book 2", "price": 20.0, "rating": 5},
            {"id": 3, "title": "Book 3", "price": 30.0, "rating": 4},
            {"id": 4, "title": "Book 4", "price": 40.0, "rating": 3},
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

        stats = stats_service.get_overview_stats(db_session)

        assert stats["total_books"] == 4
        assert stats["average_price"] == 25.0  # (10+20+30+40)/4
        assert stats["rating_distribution"][5] == 2
        assert stats["rating_distribution"][4] == 1
        assert stats["rating_distribution"][3] == 1
        assert stats["rating_distribution"][2] == 0
        assert stats["rating_distribution"][1] == 0

    def test_overview_stats_empty_database(self, db_session: Session):
        """Testa estatísticas gerais com banco vazio."""
        stats = stats_service.get_overview_stats(db_session)

        assert stats["total_books"] == 0
        assert stats["average_price"] == 0.0
        assert all(stats["rating_distribution"][i] == 0 for i in range(1, 6))


@pytest.mark.unit
class TestGetCategoryStats:
    """Testes para a função get_category_stats."""

    def test_category_stats_with_books(self, db_session: Session):
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

        stats = stats_service.get_category_stats(db_session)

        assert len(stats) == 2

        # Verifica estatísticas de Fiction (primeiro por ordem alfabética)
        fiction_stats = stats[0]
        assert fiction_stats["category_name"] == "Fiction"
        assert fiction_stats["total_books"] == 2
        assert fiction_stats["average_price"] == 15.0
        assert fiction_stats["min_price"] == 10.0
        assert fiction_stats["max_price"] == 20.0

        # Verifica estatísticas de Science
        science_stats = stats[1]
        assert science_stats["category_name"] == "Science"
        assert science_stats["total_books"] == 1
        assert science_stats["average_price"] == 30.0
        assert science_stats["min_price"] == 30.0
        assert science_stats["max_price"] == 30.0

    def test_category_stats_empty_database(self, db_session: Session):
        """Testa estatísticas por categoria com banco vazio."""
        stats = stats_service.get_category_stats(db_session)
        assert len(stats) == 0
