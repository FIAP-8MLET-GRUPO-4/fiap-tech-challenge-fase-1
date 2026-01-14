"""
Testes unitários para o category_service.
"""
import pytest
from sqlalchemy.orm import Session

from api.services import category_service
from api.models.books import Category


@pytest.mark.unit
class TestListAllCategories:
    """Testes para a função list_all_categories."""

    def test_list_categories(self, db_session: Session, test_category: Category):
        """Testa listagem de categorias."""
        categories = category_service.list_all_categories(db_session)

        assert len(categories) == 1
        assert categories[0].name == test_category.name

    def test_list_categories_ordered_alphabetically(self, db_session: Session):
        """Testa que categorias são retornadas em ordem alfabética."""
        # Cria categorias em ordem não alfabética
        cat_c = Category(id=1, name="Comedy")
        cat_a = Category(id=2, name="Action")
        cat_b = Category(id=3, name="Biography")

        db_session.add_all([cat_c, cat_a, cat_b])
        db_session.commit()

        categories = category_service.list_all_categories(db_session)

        assert len(categories) == 3
        assert categories[0].name == "Action"
        assert categories[1].name == "Biography"
        assert categories[2].name == "Comedy"

    def test_list_categories_empty_database(self, db_session: Session):
        """Testa listagem quando não há categorias."""
        categories = category_service.list_all_categories(db_session)
        assert len(categories) == 0
