"""cache.AddressSearch read/write (Story 6.5d)."""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session


def _search_ttl_days() -> int:
    return int(os.getenv("GEOSCAPE_CACHE_TTL_SEARCH_DAYS", "1"))


def _resolve_ttl_days() -> int:
    return int(os.getenv("GEOSCAPE_CACHE_TTL_RESOLVE_DAYS", "30"))


def get_cached_search(db: Session, query: str) -> Optional[List[Dict[str, Any]]]:
    key = query.strip().lower()
    rows = db.execute(
        text(
            """
            SELECT [FullResponse]
            FROM [cache].[AddressSearch]
            WHERE [OperationType] = N'Search'
              AND [CacheKey] = :cache_key
              AND [ExpiresAt] > SYSUTCDATETIME()
              AND [IsDeleted] = 0
            ORDER BY [ResultIndex]
            """
        ),
        {"cache_key": key},
    ).fetchall()
    if not rows:
        return None
    merged: List[Dict[str, Any]] = []
    for row in rows:
        merged.extend(json.loads(row.FullResponse))
    return merged


def store_search_cache(db: Session, query: str, results: List[Dict[str, Any]]) -> None:
    key = query.strip().lower()
    expires = datetime.utcnow() + timedelta(days=_search_ttl_days())
    db.execute(
        text(
            """
            DELETE FROM [cache].[AddressSearch]
            WHERE [OperationType] = N'Search' AND [CacheKey] = :cache_key
            """
        ),
        {"cache_key": key},
    )
    for index, item in enumerate(results):
        db.execute(
            text(
                """
                INSERT INTO [cache].[AddressSearch]
                (
                    [OperationType], [CacheKey], [ResultIndex], [FullResponse],
                    [ExpiresAt], [IsDeleted]
                )
                VALUES (N'Search', :cache_key, :result_index, :full_response, :expires_at, 0)
                """
            ),
            {
                "cache_key": key,
                "result_index": index,
                "full_response": json.dumps([item]),
                "expires_at": expires,
            },
        )


def get_cached_resolve(db: Session, psma_id: str) -> Optional[Dict[str, Any]]:
    row = db.execute(
        text(
            """
            SELECT TOP 1 [FullResponse], [Line1], [Line2], [Suburb], [State],
                   [Postcode], [FormattedAddress], [PsmaAddressId]
            FROM [cache].[AddressSearch]
            WHERE [OperationType] = N'Resolve'
              AND [CacheKey] = :cache_key
              AND [ExpiresAt] > SYSUTCDATETIME()
              AND [IsDeleted] = 0
            ORDER BY [ResultIndex]
            """
        ),
        {"cache_key": psma_id},
    ).fetchone()
    if row is None:
        return None
    payload = json.loads(row.FullResponse)
    payload.setdefault("resolvedFields", {
        "line1": row.Line1,
        "line2": row.Line2,
        "suburb": row.Suburb,
        "state": row.State,
        "postcode": row.Postcode,
        "formattedAddress": row.FormattedAddress,
        "psmaAddressId": row.PsmaAddressId or psma_id,
    })
    return payload


def store_resolve_cache(db: Session, psma_id: str, payload: Dict[str, Any]) -> None:
    fields = payload.get("resolvedFields") or payload
    expires = datetime.utcnow() + timedelta(days=_resolve_ttl_days())
    db.execute(
        text(
            """
            DELETE FROM [cache].[AddressSearch]
            WHERE [OperationType] = N'Resolve' AND [CacheKey] = :cache_key
            """
        ),
        {"cache_key": psma_id},
    )
    db.execute(
        text(
            """
            INSERT INTO [cache].[AddressSearch]
            (
                [OperationType], [CacheKey], [ResultIndex],
                [Line1], [Line2], [Suburb], [State], [Postcode],
                [FormattedAddress], [PsmaAddressId], [FullResponse],
                [ExpiresAt], [IsDeleted]
            )
            VALUES (
                N'Resolve', :cache_key, 0,
                :line1, :line2, :suburb, :state, :postcode,
                :formatted, :psma_id, :full_response,
                :expires_at, 0
            )
            """
        ),
        {
            "cache_key": psma_id,
            "line1": fields.get("line1"),
            "line2": fields.get("line2"),
            "suburb": fields.get("suburb"),
            "state": fields.get("state"),
            "postcode": fields.get("postcode"),
            "formatted": fields.get("formattedAddress"),
            "psma_id": fields.get("psmaAddressId") or psma_id,
            "full_response": json.dumps(payload),
            "expires_at": expires,
        },
    )
