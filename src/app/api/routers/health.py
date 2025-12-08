"""Endpoints de salud y metadatos de la API."""
from __future__ import annotations

from fastapi import APIRouter

from src.config.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
def health_check():
    return {
        "status": "ok",
        "database": settings.db_name,
        "fingerprint_port": settings.fingerprint_port_default,
    }
