# api/routers/health_route.py
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from api.core.db import get_db
from api.services.health_service import check_system_health
from api.schemas.health_schema import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health_check(response: Response, db: Session = Depends(get_db)):
    """
    Verifica a saúde da aplicação.
    Checa conexão com banco de dados e uso de recursos.
    Retorna 503 se o banco estiver indisponível.
    """
    result = check_system_health(db)
    
    # Define o status code HTTP (200 ou 503)
    response.status_code = result["status_code"]
    
    return result["payload"]