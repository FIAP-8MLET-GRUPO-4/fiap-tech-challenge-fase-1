"""
Testes de integração para os endpoints de health.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestHealthCheck:
    """Testes para o endpoint GET /api/v1/health/."""

    def test_health_check_success(self, client: TestClient):
        """Testa health check com sistema funcionando."""
        response = client.get("/api/v1/health/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "online"
        assert "system" in data
        assert "cpu_usage" in data["system"]
        assert "memory_usage" in data["system"]
