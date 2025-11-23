from fastapi import FastAPI
from api.core.db import init_db

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World"}


if __name__ == "__main__":
    init_db()

