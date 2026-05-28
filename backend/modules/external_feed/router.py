"""External data feed proxy routes (Story 6.5d)."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user_optional
from modules.auth.models import CurrentUser
from modules.companies.router import smart_company_search
from modules.companies.schemas import SmartSearchRequest

from . import address_cache_service
from .geoscape_client import GeoScapeClient, geoscape_api_key_configured


router = APIRouter(prefix="/api/external-feed", tags=["External Feed"])


class AddressResolveRequest(BaseModel):
    psmaAddressId: str = Field(..., min_length=1, max_length=100)


def _map_geoscape_resolve(payload: Dict[str, Any], psma_id: str) -> Dict[str, Any]:
    """Map PSMA addressDetails payload to structured lines for the builder."""
    details = payload.get("addressDetails") or payload.get("data") or payload
    if not isinstance(details, dict):
        details = {}

    formatted = str(details.get("formattedAddress") or "").strip()
    street_no = details.get("streetNumber1") or details.get("streetNumber") or ""
    street_name = details.get("streetName") or ""
    street_type = details.get("streetType") or ""
    line1_parts = [str(p).strip() for p in (street_no, street_name, street_type) if p]
    line1 = " ".join(line1_parts)
    if not line1:
        line1 = details.get("line1") or details.get("street") or ""

    unit = details.get("complexUnitIdentifier")
    unit_type = details.get("complexUnitType")
    line2 = details.get("line2") or ""
    if not line2 and unit:
        line2 = f"{unit_type} {unit}".strip() if unit_type else str(unit)

    suburb = (
        details.get("localityName")
        or details.get("suburb")
        or details.get("locality")
        or ""
    )
    state = details.get("stateTerritory") or details.get("state") or ""
    postcode = str(details.get("postcode") or "")

    if not formatted:
        formatted = ", ".join(part for part in (line1, suburb, state, postcode) if part)

    return {
        "psmaAddressId": psma_id,
        "resolvedFields": {
            "line1": line1,
            "line2": line2,
            "suburb": suburb,
            "state": state,
            "postcode": postcode,
            "formattedAddress": formatted,
            "psmaAddressId": psma_id,
        },
        "validationSource": "geoscape",
    }


@router.get("/address-au/status")
async def address_au_status(
    current_user: Optional[CurrentUser] = Depends(get_current_user_optional),
) -> Dict[str, bool]:
    """Non-secret probe for UAT — confirms GEOSCAPE_API_KEY is visible to the API process."""
    _ = current_user
    return {"configured": geoscape_api_key_configured()}


@router.get("/address-au/search")
async def address_au_search(
    q: str = Query(..., min_length=2, max_length=200),
    limit: int = Query(default=8, ge=1, le=20),
    current_user: Optional[CurrentUser] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    _ = current_user
    cached = address_cache_service.get_cached_search(db, q)
    if cached is not None:
        return {"items": cached, "source": "cache"}
    try:
        client = GeoScapeClient()
        items = await client.search(q, limit=limit)
        address_cache_service.store_search_cache(db, q, items)
        db.commit()
        return {"items": items, "source": "api"}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"GeoScape search failed: {exc}") from exc


@router.post("/address-au/resolve")
async def address_au_resolve(
    body: AddressResolveRequest,
    current_user: Optional[CurrentUser] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    _ = current_user
    cached = address_cache_service.get_cached_resolve(db, body.psmaAddressId)
    if cached is not None:
        return {**cached, "source": "cache"}
    try:
        client = GeoScapeClient()
        raw = await client.resolve(body.psmaAddressId)
        mapped = _map_geoscape_resolve(raw, body.psmaAddressId)
        address_cache_service.store_resolve_cache(db, body.psmaAddressId, mapped)
        db.commit()
        return {**mapped, "source": "api"}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"GeoScape resolve failed: {exc}") from exc


@router.post("/company-abr/search")
async def company_abr_search(
    body: SmartSearchRequest,
    current_user: Optional[CurrentUser] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Delegate to existing ABR smart-search (Story 1.10)."""
    response = await smart_company_search(body, current_user=current_user, db=db)
    return response.model_dump()
