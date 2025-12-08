"""Punto de entrada de la API FastAPI."""
from __future__ import annotations

from fastapi import FastAPI

from src.app.api.routers import health, auth
from src.config.settings import settings

app = FastAPI(
    title="Sistema de Dispensación Biométrica - API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/", summary="Bienvenida")
def root():
    return {
        "name": app.title,
        "version": app.version,
        "db": settings.db_name,
        "message": "API lista",
    }


# Conveniencia para ejecución directa: `python -m src.app.api.main`
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("src.app.api.main:app", host="0.0.0.0", port=8000, reload=True)
