from typing import Any, Dict

from fastapi import APIRouter

from .schemas import FormValidationResponse
from .service import validate_definition_payload

router = APIRouter(prefix="/api", tags=["form-validation"])


@router.post(
    "/form-validate",
    response_model=FormValidationResponse,
    summary="Validate DefinitionJSON statically",
    description="Validate schema, boundary constraints, and collisions in a deterministic way",
)
async def validate_form_definition(payload: Dict[str, Any]) -> FormValidationResponse:
    return validate_definition_payload(payload)
