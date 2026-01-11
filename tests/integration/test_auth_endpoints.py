"""
Testes de integração para os endpoints de autenticação.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.models.users import User


@pytest.mark.integration
class TestAuthLogin:
    """Testes para o endpoint POST /api/v1/auth/login."""

    def test_login_success(self, client: TestClient, test_user: User):
        """Testa login com credenciais válidas."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Testa login com senha incorreta."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "Username ou senha incorretos" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient):
        """Testa login com usuário inexistente."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "password123"
            }
        )

        assert response.status_code == 401


@pytest.mark.integration
class TestAuthRefresh:
    """Testes para o endpoint POST /api/v1/auth/refresh."""

    def test_refresh_token_success(self, client: TestClient, test_user: User):
        """Testa refresh de token com refresh_token válido."""
        # Primeiro faz login para obter tokens
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]

        # Usa o refresh_token para obter novos tokens
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client: TestClient):
        """Testa refresh com token inválido."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )

        assert response.status_code == 401


@pytest.mark.integration
class TestAuthRegisterAdmin:
    """Testes para o endpoint POST /api/v1/auth/register-admin."""

    def test_register_admin_success(self, client: TestClient):
        """Testa criação de usuário admin."""
        response = client.post(
            "/api/v1/auth/register-admin",
            json={
                "username": "newadmin",
                "password": "adminpass123"
            }
        )

        assert response.status_code == 200
        assert response.json()["msg"] == "Admin criado com sucesso"

    def test_register_admin_duplicate(self, client: TestClient, test_user: User):
        """Testa criação de usuário admin duplicado."""
        response = client.post(
            "/api/v1/auth/register-admin",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
