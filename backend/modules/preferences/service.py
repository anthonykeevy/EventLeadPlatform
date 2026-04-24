"""
User Preferences service — Story 6.4.

Implements read / write / reset logic against the User Preferences architecture:
  - ref.UserPreferenceCategory
  - ref.UserPreferenceKey  (reuses ref.SettingType for type coercion)
  - dbo.UserPreference     (per-user override rows; defaults via catalogue fallback)

Key design principles:
  - Default-value fallback: when no UserPreference row exists for user × key,
    the catalogue's DefaultValue is returned — no backfill required.
  - Transactional writes: PATCH validates ALL keys before writing ANY row.
  - Type validation mirrors AppSetting coercion (boolean/integer/decimal/json/string).
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from models.ref.user_preference_category import UserPreferenceCategory
from models.ref.user_preference_key import UserPreferenceKey
from models.ref.setting_type import SettingType
from models.user_preference import UserPreference

from .schemas import (
    PreferenceCategoryResponse,
    PreferenceEntry,
    PreferencesResponse,
    PatchPreferencesError,
)


# ─────────────────────────────────────────────────────────────────────────────
# Type validation helpers
# ─────────────────────────────────────────────────────────────────────────────

def _validate_value_for_type(type_code: str, raw_value: Any) -> Tuple[bool, str, str]:
    """
    Validate that ``raw_value`` can be coerced to the declared ``type_code``.

    Returns:
        (is_valid: bool, coerced_string: str, error_message: str)

    Values stored in UserPreference.PreferenceValue are always strings.
    """
    str_val = str(raw_value).strip() if raw_value is not None else ""

    tc = type_code.lower()

    if tc == "boolean":
        if str_val.lower() not in ("true", "false"):
            return False, "", f"Expected 'true' or 'false' for boolean type, got '{str_val}'"
        return True, str_val.lower(), ""

    if tc == "integer":
        try:
            int(str_val)
        except (ValueError, TypeError):
            return False, "", f"Expected an integer value, got '{str_val}'"
        return True, str_val, ""

    if tc == "decimal":
        try:
            float(str_val)
        except (ValueError, TypeError):
            return False, "", f"Expected a decimal value, got '{str_val}'"
        return True, str_val, ""

    if tc == "json":
        try:
            json.loads(str_val)
        except (json.JSONDecodeError, TypeError):
            return False, "", f"Expected a valid JSON value, got '{str_val}'"
        return True, str_val, ""

    # string (and any unknown type) — accept as-is
    return True, str_val, ""


# ─────────────────────────────────────────────────────────────────────────────
# Read — GET /api/me/preferences
# ─────────────────────────────────────────────────────────────────────────────

def get_user_preferences(db: Session, user_id: int) -> PreferencesResponse:
    """
    Return all active preference keys grouped by category, with effective values.

    For keys where the user has no override row, DefaultValue is returned
    (no UserPreference row is written; defaults are catalogue-driven).
    """
    categories = (
        db.query(UserPreferenceCategory)
        .filter(
            UserPreferenceCategory.IsActive == True,
            UserPreferenceCategory.IsDeleted == False,
        )
        .order_by(UserPreferenceCategory.DisplayOrder)
        .all()
    )

    # Load all override rows for this user in one query
    user_overrides: Dict[int, str] = {}
    overrides = (
        db.query(UserPreference)
        .filter(
            UserPreference.UserID == user_id,
            UserPreference.IsDeleted == False,
        )
        .all()
    )
    for row in overrides:
        user_overrides[row.PreferenceKeyID] = row.PreferenceValue

    result: List[PreferenceCategoryResponse] = []
    for cat in categories:
        keys = (
            db.query(UserPreferenceKey)
            .join(SettingType, UserPreferenceKey.SettingTypeID == SettingType.SettingTypeID)
            .filter(
                UserPreferenceKey.PreferenceCategoryID == cat.UserPreferenceCategoryID,
                UserPreferenceKey.IsActive == True,
                UserPreferenceKey.IsDeleted == False,
            )
            .order_by(UserPreferenceKey.SortOrder)
            .all()
        )

        entries: List[PreferenceEntry] = []
        for key in keys:
            is_overridden = key.UserPreferenceKeyID in user_overrides
            effective_value = (
                user_overrides[key.UserPreferenceKeyID]
                if is_overridden
                else key.DefaultValue
            )
            entries.append(
                PreferenceEntry(
                    preferenceKeyId=key.UserPreferenceKeyID,
                    preferenceKey=key.PreferenceKey,
                    displayName=key.DisplayName,
                    description=key.Description or "",
                    settingType=key.setting_type.TypeCode,
                    defaultValue=key.DefaultValue,
                    sortOrder=key.SortOrder,
                    value=effective_value,
                    isOverridden=is_overridden,
                )
            )

        result.append(
            PreferenceCategoryResponse(
                categoryId=cat.UserPreferenceCategoryID,
                categoryName=cat.CategoryName,
                description=cat.Description or "",
                displayOrder=cat.DisplayOrder,
                entries=entries,
            )
        )

    return PreferencesResponse(categories=result)


# ─────────────────────────────────────────────────────────────────────────────
# Write — PATCH /api/me/preferences
# ─────────────────────────────────────────────────────────────────────────────

def patch_user_preferences(
    db: Session,
    user_id: int,
    preferences: Dict[str, Any],
) -> Tuple[Optional[PreferencesResponse], List[PatchPreferencesError]]:
    """
    Upsert user preference overrides.

    Validates ALL keys before writing ANY row (transactional guarantee).

    Returns:
        (updated_prefs, errors) — if errors is non-empty, no writes occurred.
    """
    errors: List[PatchPreferencesError] = []
    validated: List[Tuple[UserPreferenceKey, str]] = []  # (key_row, coerced_value)

    for pref_key, raw_value in preferences.items():
        # Validate key exists and is active
        key_row = (
            db.query(UserPreferenceKey)
            .join(SettingType, UserPreferenceKey.SettingTypeID == SettingType.SettingTypeID)
            .filter(
                UserPreferenceKey.PreferenceKey == pref_key,
                UserPreferenceKey.IsDeleted == False,
            )
            .first()
        )

        if key_row is None:
            errors.append(PatchPreferencesError(key=pref_key, error=f"Unknown preference key '{pref_key}'"))
            continue

        if not key_row.IsActive:
            errors.append(PatchPreferencesError(key=pref_key, error=f"Preference key '{pref_key}' is not active"))
            continue

        if not key_row.IsEditable:
            errors.append(PatchPreferencesError(key=pref_key, error=f"Preference key '{pref_key}' is not editable"))
            continue

        type_code = key_row.setting_type.TypeCode
        is_valid, coerced, err_msg = _validate_value_for_type(type_code, raw_value)
        if not is_valid:
            errors.append(PatchPreferencesError(key=pref_key, error=err_msg))
            continue

        validated.append((key_row, coerced))

    if errors:
        return None, errors

    # All keys valid — upsert
    for key_row, coerced_value in validated:
        existing = (
            db.query(UserPreference)
            .filter(
                UserPreference.UserID == user_id,
                UserPreference.PreferenceKeyID == key_row.UserPreferenceKeyID,
                UserPreference.IsDeleted == False,
            )
            .first()
        )

        if existing:
            existing.PreferenceValue = coerced_value
        else:
            new_row = UserPreference(
                UserID=user_id,
                PreferenceKeyID=key_row.UserPreferenceKeyID,
                PreferenceValue=coerced_value,
                CreatedBy=user_id,
                UpdatedBy=user_id,
            )
            db.add(new_row)

    db.commit()

    return get_user_preferences(db, user_id), []


# ─────────────────────────────────────────────────────────────────────────────
# Reset — DELETE /api/me/preferences/{preferenceKey}
# ─────────────────────────────────────────────────────────────────────────────

def reset_user_preference(
    db: Session,
    user_id: int,
    preference_key: str,
) -> Tuple[bool, Optional[PreferencesResponse], Optional[str]]:
    """
    Remove the user's override row for ``preference_key``.

    The next read will return ref.UserPreferenceKey.DefaultValue.

    Returns:
        (found: bool, updated_prefs, error_message)
    """
    key_row = (
        db.query(UserPreferenceKey)
        .filter(
            UserPreferenceKey.PreferenceKey == preference_key,
            UserPreferenceKey.IsDeleted == False,
        )
        .first()
    )

    if key_row is None:
        return False, None, f"Unknown preference key '{preference_key}'"

    existing = (
        db.query(UserPreference)
        .filter(
            UserPreference.UserID == user_id,
            UserPreference.PreferenceKeyID == key_row.UserPreferenceKeyID,
            UserPreference.IsDeleted == False,
        )
        .first()
    )

    if existing:
        existing.IsDeleted = True
        existing.DeletedBy = user_id
        db.commit()

    # Return the updated catalogue (key now shows DefaultValue)
    return True, get_user_preferences(db, user_id), None
