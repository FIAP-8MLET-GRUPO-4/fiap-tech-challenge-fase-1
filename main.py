import os
from fastapi import FastAPI
from api.core.db import init_db
from api.routers import scraper_route, book_route, insights_route, ml_route, category_route, health_route, auth_route, ml_route_books
from api.core.logging_config import setup_logging
from api.middlewares.request_logging import RequestLoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

setup_logging(os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.on_event("startup")
def on_startup():
    print("Startup: Criando tabelas no banco de dados...")
    init_db()
    print("Startup: Tabelas criadas com sucesso!")

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

# Post /scraper/run: Rota para fazer o Scrapping dos Livros
app.include_router(scraper_route.router, prefix="/scraper", tags=["Scraper"])

# GET /api/v1/books: Rota para listar todos os livros disponíveis na base de dados.
app.include_router(book_route.router, prefix="/api/v1/books", tags=["Books"])

# GET /api/v1/stats/overview: Rota sobre estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings).
app.include_router(insights_route.router, prefix="/api/v1/stats", tags=["Insights"])

# GET /api/v1/ml: Rotas sobre endpoints pensados para consumo de modelos ML
app.include_router(ml_route.router, prefix="/api/v1/ml", tags=["Machine Learning"])

# GET /api/v1/categories: Rota para lista todas as categorias de livros disponíveis
app.include_router(category_route.router, prefix="/api/v1/categories", tags=["Categories"])

# GET /api/v1/health: Rota para verificar status da API e conectividade com os dados
app.include_router(health_route.router, prefix="/api/v1/health", tags=["System"])

# POST /api/v1/auth: Cria as Rotas de login e refresh para obter e renovar token
app.include_router(auth_route.router, prefix="/api/v1/auth", tags=["Authentication"])

# GET /api/v1/ml/books: Rotas sobre endpoints pensados para consumo de modelos ML para livros
app.include_router(ml_route_books.router, prefix="/api/v1/ml/books", tags=["Machine Learning Books"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)