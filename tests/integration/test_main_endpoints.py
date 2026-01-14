"""
Testes de integração para endpoints principais da aplicação.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestRootEndpoint:
    """Testes para o endpoint raiz."""

    def test_hello_world(self, client: TestClient):
        """Testa endpoint raiz GET /."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
