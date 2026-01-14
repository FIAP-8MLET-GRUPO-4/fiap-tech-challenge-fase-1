"""
Testes unitários para o health_service.
"""
import pytest
from sqlalchemy.orm import Session

from api.services import health_service


@pytest.mark.unit
class TestCheckSystemHealth:
    """Testes para a função check_system_health."""

    def test_system_health_database_online(self, db_session: Session):
        """Testa health check com banco de dados online."""
        result = health_service.check_system_health(db_session)

        assert result["status_code"] == 200
        assert result["payload"]["status"] == "ok"
        assert result["payload"]["database"] == "online"
        assert "cpu_usage" in result["payload"]["system"]
        assert "memory_usage" in result["payload"]["system"]
        assert isinstance(result["payload"]["system"]["cpu_usage"], float)
        assert isinstance(result["payload"]["system"]["memory_usage"], float)
