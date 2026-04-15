from fastapi import APIRouter, Depends

from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .schemas import FormAiGenerateRequest, FormAiGenerateResponse
from .service import generate_form_definition

router = APIRouter(prefix="/api/form-ai", tags=["Form AI"])


@router.post(
    "/generate",
    response_model=FormAiGenerateResponse,
    summary="Generate DefinitionJSON with validator retry loop",
    description=(
        "Runs Story 6.2 deterministic AI generation with context pack, "
        "validation, and max 3 correction retries."
    ),
)
async def generate_form_with_ai(
    body: FormAiGenerateRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> FormAiGenerateResponse:
    # Keep dependency to enforce authenticated use in Builder flows.
    _ = current_user
    runtime_context = body.runtimeContext.model_dump() if body.runtimeContext else None
    return generate_form_definition(
        body.prompt,
        runtime_context=runtime_context,
        max_system_correction_attempts=body.maxSystemCorrectionAttempts,
    )
