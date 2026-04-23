from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .schemas import (
    FormAiGenerateRequest,
    FormAiGenerateResponse,
    FormAiRemeasureRequest,
    FormAiRemeasureResponse,
)
from .service import generate_form_definition, remeasure_form_definition

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
    db: Session = Depends(get_db),
) -> FormAiGenerateResponse:
    # Keep dependency to enforce authenticated use in Builder flows.
    runtime_context = body.runtimeContext.model_dump() if body.runtimeContext else None
    return generate_form_definition(
        body.prompt,
        runtime_context=runtime_context,
        openai_transport=body.openaiTransport,
        max_system_correction_attempts=body.maxSystemCorrectionAttempts,
        system_prompt_addendum=body.systemPromptAddendum,
        db_session=db,
        actor_user_id=current_user.user_id,
        actor_company_id=current_user.company_id,
    )


@router.post(
    "/remeasure",
    response_model=FormAiRemeasureResponse,
    summary=(
        "Story 6.3.1 UAT round 5 — render-then-measure second pass"
    ),
    description=(
        "Recompile a previous /generate run using DOM-measured component "
        "heights from the frontend. Returns a refined DefinitionJSON whose "
        "row spacing matches the actually-rendered chrome instead of the "
        "compiler's per-type estimate. The original run's first-pass "
        "definition is left untouched in the DB; this endpoint persists "
        "remeasure-input + remeasure-output artifacts on the same run "
        "so the trace explains the layout difference."
    ),
)
async def remeasure_form_with_ai(
    body: FormAiRemeasureRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FormAiRemeasureResponse:
    # The frontend re-sends the same runtime context it used for /generate
    # (canvas dims, footprints, theme) on the body so the second pass sees
    # identical surroundings. Falling back to None is fine because the
    # compiler tolerates a missing runtime_context and the canvas defaults
    # will be used.
    runtime_context_dict = (
        body.runtimeContext.model_dump() if body.runtimeContext is not None else None
    )
    return remeasure_form_definition(
        body,
        runtime_context=runtime_context_dict,
        db_session=db,
        actor_user_id=current_user.user_id,
    )
