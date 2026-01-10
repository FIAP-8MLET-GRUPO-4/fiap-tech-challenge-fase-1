import argparse
from api.core.db import SessionLocal
from api.services.scraper_service import run_scraper_pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(limit: int | None):
    db = SessionLocal()
    try:
        logger.info(">>> SCRAPER LOCAL INICIADO <<<")
        result = run_scraper_pipeline(db, limit=limit)
        logger.info(f">>> FINALIZADO: {result} <<<")
    except Exception as e:
        logger.error(f"Erro no scraper local: {e}")
    finally:
        db.close()
        logger.info(">>> Sessão DB encerrada <<<")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraper de livros (Books to Scrape)")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite de livros por categoria (0 ou None = todos)"
    )

    args = parser.parse_args()
    main(args.limit)