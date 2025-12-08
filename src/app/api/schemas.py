from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class FingerprintAuthRequest(BaseModel):
    template: List[int] = Field(..., description="Plantilla de huella (lista de enteros)")
    requested_role: Optional[str] = Field(None, description="Rol requerido para el acceso")
    threshold: int = Field(50, description="Umbral de coincidencia")
    topn: int = Field(5, description="Cantidad de mejores coincidencias a considerar")


class PersonOut(BaseModel):
    id: int
    name: str
    role: Optional[str] = None


class FingerprintAuthResponse(BaseModel):
    ok: bool
    score: int = 0
    reason: Optional[str] = None
    person: Optional[PersonOut] = None
