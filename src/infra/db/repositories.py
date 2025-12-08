"""
Repositorios sencillos para MySQL, orientados a la BD SICEFA.
- No amarran a la UI ni a la API; se usan desde servicios o scripts.
- Pensados para evolucionar a SQLAlchemy/SQLModel si se requiere.
"""
from __future__ import annotations

import json
from typing import Iterable, List, Optional, Tuple

from src.config.settings import settings
from src.domain.models import FingerprintTemplate, Person
from src.infra.db.session import get_connection

try:
    import mysql.connector  # type: ignore
except Exception:  # pragma: no cover - import opcional en entornos sin driver
    mysql = None  # type: ignore


def _row_to_person(row: dict) -> Person:
    return Person(
        id=row.get("id") or row.get("person_id"),
        name=row.get("name") or row.get("full_name") or "",
        document=row.get("document"),
        role=row.get("role"),
    )


def _parse_template(raw) -> Optional[list[int]]:
    """Intenta normalizar la plantilla a lista de enteros."""
    if raw is None:
        return None
    if isinstance(raw, list):
        return [int(x) for x in raw]
    if isinstance(raw, (bytes, bytearray)):
        try:
            return list(raw)
        except Exception:
            return None
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [int(x) for x in data]
        except Exception:
            pass
    return None


def fetch_people(connection: Optional[object] = None) -> List[Person]:
    """
    Obtiene personas activas de la tabla `people`.
    Asume columnas: id, name, document, role, deleted_at (suave).
    Retorna [] si hay problemas de conexión o esquema.
    """
    conn = connection or get_connection()
    close_conn = connection is None
    people: List[Person] = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, document, role FROM people WHERE deleted_at IS NULL")
        for row in cursor.fetchall():
            people.append(_row_to_person(row))
        cursor.close()
    except Exception:
        return []
    finally:
        if close_conn:
            try:
                conn.close()
            except Exception:
                pass
    return people


def fetch_fingerprint_templates(connection: Optional[object] = None) -> List[FingerprintTemplate]:
    """
    Obtiene plantillas de huellas de la tabla `people` si existe la columna fingerprint_template.
    Retorna [] si no existe la columna o ante error.
    """
    conn = connection or get_connection()
    close_conn = connection is None
    templates: List[FingerprintTemplate] = []
    try:
        cursor = conn.cursor(dictionary=True)
        # Si la columna no existe, MySQL lanzará error y devolvemos []
        cursor.execute(
            "SELECT id as person_id, fingerprint_template FROM people WHERE deleted_at IS NULL"
        )
        for row in cursor.fetchall():
            tpl = _parse_template(row.get("fingerprint_template"))
            if tpl:
                templates.append(FingerprintTemplate(person_id=row["person_id"], template=tpl))
        cursor.close()
    except Exception:
        return []
    finally:
        if close_conn:
            try:
                conn.close()
            except Exception:
                pass
    return templates


def fetch_people_and_templates(
    connection: Optional[object] = None,
) -> Tuple[List[Person], List[FingerprintTemplate]]:
    """
    Obtiene personas y plantillas en una sola conexión.
    Retorna tuplas (people, templates); ambas listas pueden ser vacías.
    """
    conn = connection or get_connection()
    close_conn = connection is None
    try:
        people = fetch_people(conn)
        templates = fetch_fingerprint_templates(conn)
        return people, templates
    finally:
        if close_conn:
            try:
                conn.close()
            except Exception:
                pass


__all__ = [
    "fetch_people",
    "fetch_fingerprint_templates",
]
