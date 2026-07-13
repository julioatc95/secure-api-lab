from fastapi import FastAPI
from datetime import datetime
from app.db import check_db_connection


app = FastAPI(title="Secure API Lab", version="0.1.0")

@app.get("/")
def root():
    return {
        "message": "Secure API Lab running",
        "status": "ok"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query": q
    }

@app.get("/health/db")
def health_db():
    result = check_db_connection()
    if result is True:
        return {"database": "connected"}
    return {"database": "error", "detail": result}