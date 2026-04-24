"""
User Preferences router — Story 6.4.

Endpoints:
  GET    /api/me/preferences          — read all preferences (grouped by category)
  PATCH  /api/me/preferences          — partial upsert (transactional)
  DELETE /api/me/preferences/{key}    — reset a preference to its default
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.database import get_db
from common.logger import get_logger
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .schemas import (
    PreferencesResponse,
    PatchPreferencesRequest,
    PatchPreferencesErrorResponse,
)
from .service import (
    get_user_preferences,
    patch_user_preferences,
    reset_user_preference,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/api/me/preferences", tags=["preferences"])


@router.get(
    "",
    response_model=PreferencesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user preferences",
    description=(
        "Returns all active preference keys grouped by category. "
        "Each entry includes the user's effective value (their override if set, "
        "otherwise the catalogue DefaultValue). A brand-new user with no override "
        "rows still sees all catalogue entries with their defaults."
    ),
)
async def get_preferences(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PreferencesResponse:
    logger.debug("get_preferences user_id=%s", current_user.user_id)
    return get_user_preferences(db, current_user.user_id)


@router.patch(
    "",
    response_model=PreferencesResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user preferences",
    description=(
        "Accepts a partial dict of {preferenceKey: value}. "
        "All keys are validated before any writes occur (transactional). "
        "Returns the full updated preferences (same shape as GET)."
    ),
)
async def patch_preferences(
    request: PatchPreferencesRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PreferencesResponse:
    logger.debug(
        "patch_preferences user_id=%s keys=%s",
        current_user.user_id,
        list(request.preferences.keys()),
    )
    updated, errors = patch_user_preferences(db, current_user.user_id, request.preferences)

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "One or more preference keys failed validation. No preferences were written.",
                "errors": [{"key": e.key, "error": e.error} for e in errors],
            },
        )

    return updated


@router.delete(
    "/{preference_key:path}",
    response_model=PreferencesResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset a preference to its default",
    description=(
        "Removes the user's override row for the given preference key. "
        "The next GET will return the catalogue DefaultValue for this key. "
        "Returns the full updated preferences (same shape as GET)."
    ),
)
async def delete_preference(
    preference_key: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PreferencesResponse:
    logger.debug(
        "delete_preference user_id=%s key=%s",
        current_user.user_id,
        preference_key,
    )
    found, updated, error = reset_user_preference(db, current_user.user_id, preference_key)

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error or f"Preference key '{preference_key}' not found",
        )

    return updated
