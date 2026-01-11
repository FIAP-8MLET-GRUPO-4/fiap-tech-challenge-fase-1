"""
Testes unitários para o book_service.
"""
import pytest
from sqlalchemy.orm import Session

from api.services import book_service
from api.models.books import Book, Category


@pytest.mark.unit
class TestListBooks:
    """Testes para a função list_books."""

    def test_list_books_default_pagination(self, db_session: Session, test_book: Book):
        """Testa listagem de livros com paginação padrão."""
        books = book_service.list_books(db_session)

        assert len(books) == 1
        assert books[0].id == test_book.id
        assert books[0].title == test_book.title

    def test_list_books_with_offset(self, db_session: Session, test_category: Category):
        """Testa listagem de livros com offset."""
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

        books = book_service.list_books(db_session, offset=2, limit=2)

        assert len(books) == 2
        assert books[0].title == "Book 2"
        assert books[1].title == "Book 3"

    def test_list_books_empty_database(self, db_session: Session):
        """Testa listagem quando não há livros."""
        books = book_service.list_books(db_session)
        assert len(books) == 0


@pytest.mark.unit
class TestGetBookById:
    """Testes para a função get_book_by_id."""

    def test_get_existing_book(self, db_session: Session, test_book: Book):
        """Testa busca de livro existente."""
        book = book_service.get_book_by_id(db_session, test_book.id)

        assert book is not None
        assert book.id == test_book.id
        assert book.title == test_book.title

    def test_get_non_existing_book(self, db_session: Session):
        """Testa busca de livro inexistente."""
        book = book_service.get_book_by_id(db_session, 999)
        assert book is None


@pytest.mark.unit
class TestSearchBooksData:
    """Testes para a função search_books_data."""

    def test_search_by_title(self, db_session: Session, test_book: Book):
        """Testa busca por título."""
        books = book_service.search_books_data(db_session, title="Test")

        assert len(books) == 1
        assert books[0].title == test_book.title

    def test_search_by_title_case_insensitive(self, db_session: Session, test_book: Book):
        """Testa busca por título com case insensitive."""
        books = book_service.search_books_data(db_session, title="test")

        assert len(books) == 1
        assert books[0].title == test_book.title

    def test_search_by_category(self, db_session: Session, test_book: Book):
        """Testa busca por categoria."""
        books = book_service.search_books_data(db_session, category_name="Fiction")

        assert len(books) == 1
        assert books[0].category.name == "Fiction"

    def test_search_by_title_and_category(self, db_session: Session, test_book: Book):
        """Testa busca por título e categoria."""
        books = book_service.search_books_data(
            db_session,
            title="Test",
            category_name="Fiction"
        )

        assert len(books) == 1
        assert books[0].title == test_book.title
        assert books[0].category.name == "Fiction"

    def test_search_no_results(self, db_session: Session, test_book: Book):
        """Testa busca sem resultados."""
        books = book_service.search_books_data(db_session, title="NonExistent")
        assert len(books) == 0
