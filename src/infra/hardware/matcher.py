"""
Matcher basado en el sensor PyFingerprint.
- Usa la característica capturada ya cargada en el buffer1 (F1) del sensor.
- Para cada candidato, sube la plantilla al buffer2 y usa compareCharacteristics().
"""
from __future__ import annotations

from typing import Iterable, List, Tuple

from src.domain.models import FingerprintTemplate
from src.domain.services import FingerprintMatcher


class PyFingerprintHardwareMatcher(FingerprintMatcher):
    def __init__(self, sensor):
        self.sensor = sensor

    def match(
        self,
        captured: FingerprintTemplate,
        candidates: Iterable[FingerprintTemplate],
        threshold: int,
        topn: int,
    ) -> List[Tuple[int, int]]:
        scored: List[Tuple[int, int]] = []
        for tpl in candidates:
            if not tpl.template:
                continue
            try:
                # Cargar candidato en buffer2 (F2)
                self.sensor.uploadCharacteristics(0x02, tpl.template)
                score = self.sensor.compareCharacteristics()
                if score >= threshold:
                    scored.append((tpl.person_id, score))
            except Exception:
                # Ignorar plantillas corruptas o fallas puntuales
                continue
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[: max(1, topn)]
