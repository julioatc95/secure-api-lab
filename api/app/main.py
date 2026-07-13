import logging
import time
from fastapi import FastAPI, Request
from datetime import datetime
from app.db import check_db_connection
from fastapi.responses import JSONResponse


# 1. Configurar logging PRIMERO
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("secure-api-lab")

# 2. Crear la instancia de FastAPI ANTES de usar "app" en cualquier decorador
app = FastAPI(title="Secure API Lab", version="0.1.0")

# 3. @app.middleware, @app.get, etc.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration}ms")
    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"ValueError en {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "detail": str(exc),
            "path": request.url.path
        }
    )
@app.get("/")
def root():
    return {"message": "Secure API Lab running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health/db")
def health_db():
    result = check_db_connection()
    if result is True:
        return {"database": "connected"}
    return {"database": "error", "detail": result}

@app.get("/boom")
def boom():
    raise ValueError("Error simulado para practicar logs")