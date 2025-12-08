"""Entidades de dominio básicas (sin dependencias de infraestructura)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    id: int
    name: str
    document: Optional[str] = None
    role: Optional[str] = None


@dataclass
class FingerprintTemplate:
    person_id: int
    template: list[int]
    score: Optional[int] = None
