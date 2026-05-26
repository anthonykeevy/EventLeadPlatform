"""GeoScape/PSMA HTTP client (Story 6.5d address-lookup-au)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

try:
    from dotenv import load_dotenv

    _BACKEND_ROOT = Path(__file__).resolve().parents[2]
    load_dotenv(_BACKEND_ROOT / ".env")
except ImportError:
    pass

GEOSCAPE_BASE_URL = "https://api.psma.com.au"
DEFAULT_TIMEOUT = float(os.getenv("GEOSCAPE_API_TIMEOUT", "10"))


def geoscape_api_key_configured() -> bool:
    """True when GEOSCAPE_API_KEY is present in the environment (value not logged)."""
    return bool(os.getenv("GEOSCAPE_API_KEY", "").strip())


def _normalize_suggestion(item: Any) -> Dict[str, Any]:
    """Map PSMA predictive items to { id, label } for the builder UI."""
    if isinstance(item, str):
        text = item.strip()
        psma_id = ""
        label = text
        if "," in text:
            head, rest = text.split(",", 1)
            head = head.strip()
            if head:
                psma_id = head
                label = rest.strip() or text
        return {"id": psma_id, "label": label, "raw": text}
    if isinstance(item, dict):
        psma_id = (
            item.get("id")
            or item.get("psmaAddressId")
            or item.get("property_id")
            or item.get("propertyId")
            or ""
        )
        label = (
            item.get("label")
            or item.get("address")
            or item.get("formattedAddress")
            or item.get("formatted_address")
            or str(psma_id)
        )
        return {"id": str(psma_id), "label": str(label), "raw": item}
    return {"id": "", "label": str(item), "raw": item}


class GeoScapeClient:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("GEOSCAPE_API_KEY", "").strip()
        if not self.api_key:
            raise RuntimeError(
                "GEOSCAPE_API_KEY is not configured. Set the Application Setting / environment "
                "variable GEOSCAPE_API_KEY on the API host (local: backend/.env then restart "
                "uvicorn; Azure Test: App Service Configuration → restart the app). "
                "Changing .env on your PC does not affect the Test slot."
            )

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": self.api_key}

    async def search(self, query: str, *, limit: int = 8) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(
                f"{GEOSCAPE_BASE_URL}/v1/predictive/address",
                params={"query": query, "limit": limit},
                headers=self._headers(),
            )
            response.raise_for_status()
            payload = response.json()
        suggestions = payload.get("suggest") or payload.get("suggestions") or []
        results: List[Dict[str, Any]] = []
        for item in suggestions:
            normalized = _normalize_suggestion(item)
            if normalized.get("id") or normalized.get("label"):
                results.append(normalized)
        return results

    async def resolve(self, psma_address_id: str) -> Dict[str, Any]:
        """Fetch address summary + addressDetails (formatted lines for UI/storage)."""
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            headers = self._headers()
            summary_resp = await client.get(
                f"{GEOSCAPE_BASE_URL}/v1/addresses/{psma_address_id}",
                headers=headers,
            )
            summary_resp.raise_for_status()
            summary = summary_resp.json()

            links = summary.get("links") if isinstance(summary.get("links"), dict) else {}
            details_path = links.get("addressDetails") or f"/v1/addresses/{psma_address_id}/addressDetails/"
            details_url = (
                f"{GEOSCAPE_BASE_URL}{details_path}"
                if str(details_path).startswith("/")
                else str(details_path)
            )

            details_resp = await client.get(details_url, headers=headers)
            details_resp.raise_for_status()
            details_body = details_resp.json()
            address_details = details_body.get("addressDetails") or details_body

            return {
                "addressId": summary.get("addressId") or psma_address_id,
                "addressDetails": address_details,
            }
