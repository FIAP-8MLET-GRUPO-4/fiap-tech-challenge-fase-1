# api/services/health_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
import psutil
import logging

logger = logging.getLogger(__name__)

def check_system_health(db: Session):
    """
    Verifica conectividade com DB e uso de recursos.
    """
    # 1. Verificar Banco de Dados
    db_status = "offline"
    status_code = 503 # Service Unavailable (padrão HTTP se algo estiver quebrado)
    
    try:
        # Tenta executar o comando mais leve possível
        db.execute(text("SELECT 1"))
        db_status = "online"
        status_code = 200 # OK
    except Exception as e:
        logger.error(f"Health Check Falhou no Banco: {e}")
        db_status = "offline"

    # 2. Verificar Sistema (CPU/RAM)
    # interval=None faz a leitura ser não-bloqueante (pega o último valor instantâneo)
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent

    return {
        "status_code": status_code,
        "payload": {
            "status": "ok" if db_status == "online" else "error",
            "database": db_status,
            "system": {
                "cpu_usage": cpu,
                "memory_usage": memory
            }
        }
    }