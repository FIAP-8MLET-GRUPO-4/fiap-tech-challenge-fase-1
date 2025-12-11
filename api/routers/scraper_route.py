# api/routers/scraper_route.py
from fastapi import APIRouter, BackgroundTasks, Query
from api.core.db import SessionLocal 
from api.services.scraper_service import run_scraper_pipeline
import logging
import sys
from typing import Optional

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def scraper_background_task(limit: Optional[int]):
    db = SessionLocal() 
    try:
        logger.info(f">>> JOB INICIADO (Limite solicitado: {limit}) <<<")
        run_scraper_pipeline(db, limit=limit)
        logger.info(">>> JOB FINALIZADO: Scraper completado com sucesso <<<")
    except Exception as e:
        logger.error(f"Erro na task do scraper: {e}")
    finally:
        db.close()
        logger.info(">>> Sessão do Scraper fechada <<<")

@router.post("/run")
def trigger_scraper(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = Query(None, description="Limite de livros por categoria. Use 0 para todos.")
):
    """
    Inicia o processo de Scraper em segundo plano.
    - **limit**: (Opcional) Sobrescreve a configuração padrão. Ex: ?limit=1 para teste rápido.
    """
    background_tasks.add_task(scraper_background_task, limit)
    
    return {
        "message": "O processo de scraping foi iniciado em segundo plano.",
        "config": f"Limite aplicado: {limit if limit is not None else 'Padrão do Ambiente'}",
        "note": "Verifique os logs do console para acompanhar o progresso."
    }