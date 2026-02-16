"""
Form Schema API Router (Story 5.3)
GET /api/form-schema/{version} - Returns DefinitionJSON JSON Schema from DB
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from common.database import get_db
from models.ref.form_defaults_schema_version import FormDefaultsSchemaVersion


router = APIRouter(prefix="/api/form-schema", tags=["Form Schema"])


def _normalize_version(version: str) -> str:
    """Map '1' -> '1.0' for API convenience."""
    if version == "1":
        return "1.0"
    return version


@router.get(
    "/{version}",
    summary="Get DefinitionJSON schema",
    description="Returns JSON Schema for DefinitionJSON from ref.FormDefaultsSchemaVersion.SchemaDocument",
)
async def get_form_schema(
    version: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    GET /api/form-schema/{version}
    version: "1.0" or "1" (maps to 1.0)
    Returns 200 + JSON Schema body, or 404 for unknown version.
    """
    ver = _normalize_version(version)
    # Prefer SchemaVersionString (Story 5.3); fallback to SchemaVersion INT
    stmt = select(FormDefaultsSchemaVersion).where(
        FormDefaultsSchemaVersion.IsActive == True,
    )
    rows = db.execute(stmt).scalars().all()
    row = None
    for r in rows:
        if r.SchemaVersionString == ver:
            row = r
            break
    if not row and ver == "1.0":
        for r in rows:
            if r.SchemaVersion == 1:
                row = r
                break
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schema version '{version}' not found",
        )
    if not row.SchemaDocument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schema document not populated for version '{version}'",
        )
    try:
        return json.loads(row.SchemaDocument)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Schema document is invalid JSON",
        )
