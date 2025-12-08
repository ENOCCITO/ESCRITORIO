"""
Servicios de dominio (casos de uso) sin dependencias de UI ni frameworks.
Actualmente es un esqueleto para migrar la lógica de huellas y roles desde main.py.
"""
from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

from src.domain.models import FingerprintTemplate, Person


class FingerprintMatcher:
    """
    Ejemplo de interfaz de comparación de huellas.
    La implementación concreta (hardware o simulador) debe proveerse en infraestructura.
    """

    def match(
        self,
        captured: FingerprintTemplate,
        candidates: Iterable[FingerprintTemplate],
        threshold: int,
        topn: int,
    ) -> List[Tuple[int, int]]:
        """
        Devuelve pares (person_id, score) ordenados por score desc.
        """
        raise NotImplementedError


class RoleValidatorService:
    """
    Encapsula la lógica de validación de roles.
    Se puede adaptar para usar repositorios o caché en futuras versiones.
    """

    def validate(self, person: Person, requested_role: Optional[str]) -> bool:
        if requested_role is None:
            return True
        if person.role is None:
            return False
        return person.role.lower() == requested_role.lower()


class SimpleThresholdMatcher(FingerprintMatcher):
    """
    Implementación simple que compara longitud y coincidencias exactas.
    Nota: es un placeholder para desacoplar la UI de la lógica de match.
    """

    def __init__(self):
        pass

    def match(
        self,
        captured: FingerprintTemplate,
        candidates: Iterable[FingerprintTemplate],
        threshold: int,
        topn: int,
    ) -> List[Tuple[int, int]]:
        scored: List[Tuple[int, int]] = []
        cap_tpl = captured.template or []
        for tpl in candidates:
            cand_tpl = tpl.template or []
            # similitud simple: cuenta de posiciones iguales, como proxy
            score = sum(1 for a, b in zip(cap_tpl, cand_tpl) if a == b)
            if score >= threshold:
                scored.append((tpl.person_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[: max(1, topn)]


class FingerprintAuthResult:
    def __init__(self, ok: bool, person: Optional[Person], score: int = 0, reason: str = ""):
        self.ok = ok
        self.person = person
        self.score = score
        self.reason = reason


class FingerprintAuthService:
    """
    Servicio de autenticación por huella que usa un matcher y repositorios.
    No depende de UI ni frameworks; puede usarse desde GUI y API.
    """

    def __init__(self, matcher: FingerprintMatcher):
        self.matcher = matcher

    def authenticate(
        self,
        captured_template: FingerprintTemplate,
        candidates: Iterable[FingerprintTemplate],
        people: Iterable[Person],
        threshold: int,
        topn: int,
        requested_role: Optional[str] = None,
    ) -> FingerprintAuthResult:
        people_map = {p.id: p for p in people}
        matches = self.matcher.match(captured_template, candidates, threshold, topn)
        if not matches:
            return FingerprintAuthResult(False, None, 0, "no_match")
        best_id, best_score = matches[0]
        person = people_map.get(best_id)
        if not person:
            return FingerprintAuthResult(False, None, best_score, "person_not_found")
        if requested_role:
            if not person.role or person.role.lower() != requested_role.lower():
                return FingerprintAuthResult(False, person, best_score, "role_denied")
        return FingerprintAuthResult(True, person, best_score, "")
