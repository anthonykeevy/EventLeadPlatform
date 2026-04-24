"""
Pydantic schemas for the User Preferences API.

GET /api/me/preferences  — PreferencesResponse
PATCH /api/me/preferences — PatchPreferencesRequest → PreferencesResponse
DELETE /api/me/preferences/{key} — (no body) → PreferencesResponse
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class PreferenceEntry(BaseModel):
    """One preference key with its effective value for the requesting user."""
    preferenceKeyId: int
    preferenceKey: str
    displayName: str
    description: str
    settingType: str          # TypeCode from ref.SettingType (e.g. 'boolean', 'integer')
    defaultValue: str
    sortOrder: int
    value: str                # Effective value: user override OR defaultValue
    isOverridden: bool        # True if a UserPreference row exists for this user × key


class PreferenceCategoryResponse(BaseModel):
    """A category with its preference entries."""
    categoryId: int
    categoryName: str
    description: str
    displayOrder: int
    entries: List[PreferenceEntry]


class PreferencesResponse(BaseModel):
    """Full response for GET /api/me/preferences."""
    categories: List[PreferenceCategoryResponse]


class PatchPreferencesRequest(BaseModel):
    """
    Partial update request for PATCH /api/me/preferences.
    Dict of {preferenceKey: value} — all values are strings (type-validated server-side).
    """
    preferences: Dict[str, Any]


class PatchPreferencesError(BaseModel):
    """Per-key error detail returned when PATCH fails."""
    key: str
    error: str


class PatchPreferencesErrorResponse(BaseModel):
    """Structured error response when one or more keys fail validation."""
    detail: str
    errors: List[PatchPreferencesError]
