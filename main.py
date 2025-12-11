from fastapi import FastAPI
from api.core.db import init_db
from api.routers import scraper_route

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("Startup: Criando tabelas no banco de dados...")
    init_db()
    print("Startup: Tabelas criadas com sucesso!")

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

app.include_router(scraper_route.router, prefix="/scraper", tags=["Scraper"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)