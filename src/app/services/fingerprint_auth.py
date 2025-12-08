"""
Servicio de aplicación para autenticación por huella.
Coordina infraestructura (repositorios + matcher hardware) y dominio (auth service).
No depende de UI ni frameworks web.
"""
from __future__ import annotations

from typing import Optional, Tuple, List

from src.domain.models import FingerprintTemplate, Person
from src.domain.services import FingerprintAuthService, FingerprintMatcher
from src.infra.db.repositories import fetch_people_and_templates


class FingerprintAuthAppService:
    """
    Orquesta carga de personas/plantillas desde DB y delega el match
    a un FingerprintMatcher (hardware o simulador).
    """

    def __init__(self, matcher: FingerprintMatcher):
        self.matcher = matcher
        self.auth = FingerprintAuthService(matcher)

    def load_people_and_templates(self) -> Tuple[List[Person], List[FingerprintTemplate]]:
        return fetch_people_and_templates()

    def authenticate(
        self,
        captured_template: FingerprintTemplate,
        requested_role: Optional[str],
        threshold: int,
        topn: int,
        people: List[Person],
        templates: List[FingerprintTemplate],
    ):
        return self.auth.authenticate(
            captured_template=captured_template,
            candidates=templates,
            people=people,
            threshold=threshold,
            topn=topn,
            requested_role=requested_role,
        )
