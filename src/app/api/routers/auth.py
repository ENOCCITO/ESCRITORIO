from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.app.api.schemas import (
    FingerprintAuthRequest,
    FingerprintAuthResponse,
    PersonOut,
)
from src.domain.models import FingerprintTemplate
from src.domain.services import FingerprintAuthService, SimpleThresholdMatcher
from src.infra.db.repositories import fetch_people_and_templates

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/fingerprint", response_model=FingerprintAuthResponse, summary="Autenticación por huella (offline)")
def fingerprint_auth(payload: FingerprintAuthRequest):
    """
    Autenticación por huella usando el matcher simple (offline, sin hardware).
    Se utiliza para API y pruebas sin sensor. El matcher de hardware vive en GUI.
    """
    try:
        people, templates = fetch_people_and_templates()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Error al consultar BD: {exc}")

    candidate_templates = [
        FingerprintTemplate(person_id=tpl.person_id, template=tpl.template) for tpl in templates
    ]

    matcher = SimpleThresholdMatcher()
    service = FingerprintAuthService(matcher)
    captured = FingerprintTemplate(person_id=-1, template=payload.template)
    result = service.authenticate(
        captured_template=captured,
        candidates=candidate_templates,
        people=people,
        threshold=payload.threshold,
        topn=payload.topn,
        requested_role=payload.requested_role,
    )

    if not result.ok:
        return FingerprintAuthResponse(ok=False, score=result.score, reason=result.reason)

    person = result.person
    return FingerprintAuthResponse(
        ok=True,
        score=result.score,
        person=PersonOut(id=person.id, name=person.name, role=person.role) if person else None,
    )
