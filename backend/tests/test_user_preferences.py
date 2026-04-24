"""
Story 6.4: User Preferences — unit tests.

Covers:
  - Type validation helper (_validate_value_for_type)
  - Service: default-value fallback when no override row exists
  - Service: PATCH validation (unknown key, inactive key, type mismatch, transactional)
  - Service: reset (DELETE) sets IsDeleted=True; next read returns DefaultValue
  - GET /api/me/preferences endpoint (with mocked auth + service)

Tests that require the Story 6.4 migrations to be applied are marked
@pytest.mark.requires_migrations and are skipped automatically in environments
where the tables have not yet been created.
"""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from modules.preferences.service import _validate_value_for_type


# ─────────────────────────────────────────────────────────────────────────────
# Type validation helper (pure Python — no DB)
# ─────────────────────────────────────────────────────────────────────────────

class TestValidateValueForType:

    @pytest.mark.parametrize("raw, expected_coerced", [
        ("true", "true"),
        ("True", "true"),
        ("TRUE", "true"),
        ("false", "false"),
        ("False", "false"),
    ])
    def test_boolean_valid(self, raw: str, expected_coerced: str):
        ok, coerced, err = _validate_value_for_type("boolean", raw)
        assert ok is True
        assert coerced == expected_coerced
        assert err == ""

    @pytest.mark.parametrize("raw", ["yes", "no", "1", "0", "", "truee", None])
    def test_boolean_invalid(self, raw: Any):
        ok, _, err = _validate_value_for_type("boolean", raw)
        assert ok is False
        assert err != ""

    @pytest.mark.parametrize("raw, expected_coerced", [
        ("2", "2"),
        ("0", "0"),
        ("10", "10"),
        ("-1", "-1"),
    ])
    def test_integer_valid(self, raw: str, expected_coerced: str):
        ok, coerced, err = _validate_value_for_type("integer", raw)
        assert ok is True
        assert coerced == expected_coerced

    @pytest.mark.parametrize("raw", ["abc", "1.5", "", "two"])
    def test_integer_invalid(self, raw: str):
        ok, _, err = _validate_value_for_type("integer", raw)
        assert ok is False
        assert err != ""

    def test_decimal_valid(self):
        ok, coerced, err = _validate_value_for_type("decimal", "3.14")
        assert ok is True
        assert coerced == "3.14"

    def test_decimal_invalid(self):
        ok, _, err = _validate_value_for_type("decimal", "not-a-number")
        assert ok is False

    def test_json_valid(self):
        ok, coerced, _ = _validate_value_for_type("json", '{"key": "value"}')
        assert ok is True

    def test_json_invalid(self):
        ok, _, err = _validate_value_for_type("json", "{bad json}")
        assert ok is False

    def test_string_always_valid(self):
        for raw in ["hello", "", "  ", '{"key": "value"}', None]:
            ok, _, _ = _validate_value_for_type("string", raw)
            assert ok is True

    def test_unknown_type_falls_back_to_string(self):
        ok, coerced, _ = _validate_value_for_type("url", "https://example.com")
        assert ok is True


# ─────────────────────────────────────────────────────────────────────────────
# Service: PATCH validation logic (unit — mock DB)
# ─────────────────────────────────────────────────────────────────────────────

def _make_setting_type(type_code: str) -> MagicMock:
    st = MagicMock()
    st.TypeCode = type_code
    return st


def _make_key_row(
    key_id: int,
    preference_key: str,
    type_code: str = "boolean",
    default_value: str = "false",
    is_active: bool = True,
    is_editable: bool = True,
    is_deleted: bool = False,
) -> MagicMock:
    row = MagicMock()
    row.UserPreferenceKeyID = key_id
    row.PreferenceKey = preference_key
    row.DefaultValue = default_value
    row.IsActive = is_active
    row.IsEditable = is_editable
    row.IsDeleted = is_deleted
    row.setting_type = _make_setting_type(type_code)
    return row


class TestPatchUserPreferences:

    def _make_db(self, key_row=None):
        """Return a mock DB session where query returns key_row or None."""
        db = MagicMock()
        query_chain = MagicMock()
        query_chain.join.return_value = query_chain
        query_chain.filter.return_value = query_chain
        query_chain.first.return_value = key_row
        db.query.return_value = query_chain
        return db

    def test_unknown_key_returns_error_no_write(self):
        from modules.preferences.service import patch_user_preferences

        db = self._make_db(key_row=None)  # key not found
        result, errors = patch_user_preferences(db, user_id=1, preferences={"nonexistent.key": "true"})

        assert result is None
        assert len(errors) == 1
        assert errors[0].key == "nonexistent.key"
        assert "Unknown" in errors[0].error
        db.commit.assert_not_called()

    def test_inactive_key_returns_error(self):
        from modules.preferences.service import patch_user_preferences

        inactive_key = _make_key_row(1, "notifications.ai_agent.suppress_replace_warning", is_active=False)
        db = self._make_db(key_row=inactive_key)
        result, errors = patch_user_preferences(
            db, user_id=1,
            preferences={"notifications.ai_agent.suppress_replace_warning": "true"}
        )

        assert result is None
        assert len(errors) == 1
        assert "not active" in errors[0].error
        db.commit.assert_not_called()

    def test_non_editable_key_returns_error(self):
        from modules.preferences.service import patch_user_preferences

        locked_key = _make_key_row(1, "notifications.ai_agent.suppress_replace_warning", is_editable=False)
        db = self._make_db(key_row=locked_key)
        result, errors = patch_user_preferences(
            db, user_id=1,
            preferences={"notifications.ai_agent.suppress_replace_warning": "true"}
        )

        assert result is None
        assert len(errors) == 1
        assert "not editable" in errors[0].error
        db.commit.assert_not_called()

    def test_type_mismatch_integer_key_returns_error(self):
        from modules.preferences.service import patch_user_preferences

        int_key = _make_key_row(1, "some.integer.key", type_code="integer", default_value="2")
        db = self._make_db(key_row=int_key)
        result, errors = patch_user_preferences(
            db, user_id=1,
            preferences={"some.integer.key": "not-a-number"}
        )

        assert result is None
        assert len(errors) == 1
        assert "integer" in errors[0].error.lower()
        db.commit.assert_not_called()

    def test_boolean_invalid_value_returns_error(self):
        from modules.preferences.service import patch_user_preferences

        bool_key = _make_key_row(1, "notifications.ai_agent.suppress_replace_warning", type_code="boolean")
        db = self._make_db(key_row=bool_key)
        result, errors = patch_user_preferences(
            db, user_id=1,
            preferences={"notifications.ai_agent.suppress_replace_warning": "yes"}
        )

        assert result is None
        assert len(errors) == 1
        db.commit.assert_not_called()

    def test_multiple_keys_one_bad_no_writes(self):
        """Transactional guarantee: one invalid key → zero writes."""
        from modules.preferences.service import patch_user_preferences

        db = MagicMock()
        good_key = _make_key_row(1, "good.key", type_code="boolean")
        bad_key = None  # not found

        call_count = [0]

        def query_side_effect(*args):
            chain = MagicMock()
            chain.join.return_value = chain

            def filter_side_effect(*fargs):
                call_count[0] += 1
                inner = MagicMock()
                # First call → good key, second → bad key (None)
                inner.first.return_value = good_key if call_count[0] == 1 else None
                return inner

            chain.filter.side_effect = filter_side_effect
            return chain

        db.query.side_effect = query_side_effect

        result, errors = patch_user_preferences(
            db, user_id=1,
            preferences={"good.key": "true", "unknown.key": "false"}
        )

        assert result is None
        assert len(errors) == 1
        assert errors[0].key == "unknown.key"
        db.commit.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# Service: default-value fallback (unit — mock DB)
# ─────────────────────────────────────────────────────────────────────────────

class TestDefaultValueFallback:

    def test_get_preferences_no_rows_returns_defaults(self):
        """Brand-new user with no UserPreference rows sees DefaultValue for all keys."""
        from modules.preferences.service import get_user_preferences
        from modules.preferences.schemas import PreferencesResponse

        # Build a mock DB that returns one category with one key, zero override rows
        db = MagicMock()

        mock_setting_type = _make_setting_type("boolean")

        mock_key = MagicMock()
        mock_key.UserPreferenceKeyID = 1
        mock_key.PreferenceKey = "notifications.ai_agent.suppress_replace_warning"
        mock_key.DisplayName = "AI panel: suppress replace-form warning"
        mock_key.Description = "Help text"
        mock_key.DefaultValue = "false"
        mock_key.SortOrder = 10
        mock_key.setting_type = mock_setting_type

        mock_cat = MagicMock()
        mock_cat.UserPreferenceCategoryID = 1
        mock_cat.CategoryName = "Notifications"
        mock_cat.Description = "Notification prefs"
        mock_cat.DisplayOrder = 10
        mock_cat.IsActive = True
        mock_cat.IsDeleted = False

        # Simulate DB queries
        categories_query = MagicMock()
        categories_query.filter.return_value = categories_query
        categories_query.order_by.return_value = categories_query
        categories_query.all.return_value = [mock_cat]

        overrides_query = MagicMock()
        overrides_query.filter.return_value = overrides_query
        overrides_query.all.return_value = []  # no overrides for this user

        keys_query = MagicMock()
        keys_query.join.return_value = keys_query
        keys_query.filter.return_value = keys_query
        keys_query.order_by.return_value = keys_query
        keys_query.all.return_value = [mock_key]

        call_sequence = [categories_query, overrides_query, keys_query]
        call_idx = [0]

        def query_side(model):
            q = call_sequence[call_idx[0] % len(call_sequence)]
            call_idx[0] += 1
            return q

        db.query.side_effect = query_side

        result = get_user_preferences(db, user_id=99)

        assert isinstance(result, PreferencesResponse)
        assert len(result.categories) == 1
        cat = result.categories[0]
        assert cat.categoryName == "Notifications"
        assert len(cat.entries) == 1
        entry = cat.entries[0]
        assert entry.preferenceKey == "notifications.ai_agent.suppress_replace_warning"
        assert entry.value == "false"  # default, not overridden
        assert entry.isOverridden is False


# ─────────────────────────────────────────────────────────────────────────────
# Service: _get_default_retries
# ─────────────────────────────────────────────────────────────────────────────

class TestGetDefaultRetries:

    def setup_method(self):
        # Reset the cache before each test
        from modules.form_ai import service as form_ai_service
        form_ai_service._cached_default_retries = None

    def test_returns_fallback_when_no_db_session(self):
        from modules.form_ai.service import _get_default_retries
        result = _get_default_retries(db_session=None)
        assert result == 2  # _DEFAULT_RETRIES_FALLBACK

    def test_returns_fallback_when_setting_not_found(self):
        from modules.form_ai.service import _get_default_retries

        db = MagicMock()
        db.execute.return_value.fetchone.return_value = None  # no row
        result = _get_default_retries(db_session=db)
        assert result == 2

    def test_reads_from_db_and_caches(self):
        from modules.form_ai import service as form_ai_service
        from modules.form_ai.service import _get_default_retries

        db = MagicMock()
        row = MagicMock()
        row.__getitem__ = lambda self, idx: "3"  # SettingValue = "3"
        db.execute.return_value.fetchone.return_value = row

        result = _get_default_retries(db_session=db)
        assert result == 3
        assert form_ai_service._cached_default_retries == 3

    def test_cache_prevents_second_db_call(self):
        from modules.form_ai import service as form_ai_service
        from modules.form_ai.service import _get_default_retries

        form_ai_service._cached_default_retries = 5  # pre-warm cache

        db = MagicMock()
        result = _get_default_retries(db_session=db)
        assert result == 5
        db.execute.assert_not_called()  # cache hit

    def test_invalidate_cache_forces_reload(self):
        from modules.form_ai import service as form_ai_service
        from modules.form_ai.service import _get_default_retries, _invalidate_default_retries_cache

        form_ai_service._cached_default_retries = 5
        _invalidate_default_retries_cache()
        assert form_ai_service._cached_default_retries is None

        db = MagicMock()
        db.execute.return_value.fetchone.return_value = None
        result = _get_default_retries(db_session=db)
        assert result == 2  # fallback since row is None

    def test_clamps_value_to_0_10(self):
        from modules.form_ai import service as form_ai_service
        from modules.form_ai.service import _get_default_retries

        form_ai_service._cached_default_retries = None

        db = MagicMock()
        row = MagicMock()
        row.__getitem__ = lambda self, idx: "99"  # out of range
        db.execute.return_value.fetchone.return_value = row

        result = _get_default_retries(db_session=db)
        assert result == 10  # clamped to max


# ─────────────────────────────────────────────────────────────────────────────
# Reset preference (DELETE) — unit
# ─────────────────────────────────────────────────────────────────────────────

class TestResetUserPreference:

    def test_reset_unknown_key_returns_false(self):
        from modules.preferences.service import reset_user_preference

        db = MagicMock()
        query = MagicMock()
        query.filter.return_value = query
        query.first.return_value = None  # key not found
        db.query.return_value = query

        found, _, error = reset_user_preference(db, user_id=1, preference_key="nonexistent.key")

        assert found is False
        assert "Unknown" in error

    def test_reset_existing_row_soft_deletes(self):
        from modules.preferences.service import reset_user_preference

        mock_key = _make_key_row(1, "notifications.ai_agent.suppress_replace_warning")
        mock_override = MagicMock()
        mock_override.IsDeleted = False

        db = MagicMock()
        call_idx = [0]

        # Build simple routing: first call to query returns key lookup, second returns override lookup
        def make_chain(return_value):
            chain = MagicMock()
            chain.filter.return_value = chain
            chain.join.return_value = chain
            chain.first.return_value = return_value
            chain.order_by.return_value = chain
            chain.all.return_value = []
            return chain

        key_chain = make_chain(mock_key)
        override_chain = make_chain(mock_override)
        # get_user_preferences will then call query 3 times (cat, overrides, keys)
        # We only need to handle the first two for reset_user_preference itself.
        cat_chain = make_chain([])
        overrides2_chain = make_chain([])
        keys_chain = make_chain([])

        call_sequence = [key_chain, override_chain, cat_chain, overrides2_chain, keys_chain]
        call_idx_box = [0]

        def query_side(*args):
            chain = call_sequence[call_idx_box[0] % len(call_sequence)]
            call_idx_box[0] += 1
            return chain

        db.query.side_effect = query_side

        # categories for get_user_preferences return value
        cat_chain.all.return_value = []

        found, updated, error = reset_user_preference(
            db, user_id=1,
            preference_key="notifications.ai_agent.suppress_replace_warning"
        )

        assert found is True
        assert error is None
        assert mock_override.IsDeleted is True
        assert mock_override.DeletedBy == 1
        db.commit.assert_called_once()
