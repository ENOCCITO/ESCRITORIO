"""
Pequeño wrapper para abrir conexiones MySQL reutilizando settings.
Pensado para ser usado tanto por scripts como por futuras APIs.
"""
from __future__ import annotations

from typing import Optional

from src.config.settings import settings


def get_connection():
    """Devuelve una conexión mysql-connector ya configurada."""
    try:
        import mysql.connector  # type: ignore
    except Exception as exc:  # pragma: no cover - fallo de import en runtime
        raise RuntimeError(f"No se pudo importar mysql-connector: {exc}") from exc

    return mysql.connector.connect(**settings.db_config)


def get_connection_safe() -> Optional[object]:
    """
    Variante que atrapa excepciones y devuelve None en lugar de elevar.
    Útil en scripts de diagnóstico donde no queremos romper el flujo.
    """
    try:
        return get_connection()
    except Exception:
        return None
