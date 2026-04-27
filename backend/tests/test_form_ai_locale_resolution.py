import pytest
from pydantic import ValidationError

from modules.form_ai import service
from modules.form_ai.schemas import FormAiGenerateRequest


class _FakeResult:
    def __init__(self, row=None):
        self._row = row

    def fetchone(self):
        return self._row


class _ResolutionSession:
    def __init__(
        self,
        *,
        event_country=None,
        company_country=None,
        user_country=None,
        app_locale="AU",
        company_brand_posture=None,
        company_brand_origin=None,
        app_brand_posture="local",
    ):
        self.event_country = event_country
        self.company_country = company_country
        self.user_country = user_country
        self.app_locale = app_locale
        self.company_brand_posture = company_brand_posture
        self.company_brand_origin = company_brand_origin
        self.app_brand_posture = app_brand_posture

    def execute(self, statement, params=None):
        sql = " ".join(str(statement).split())
        params = params or {}
        if "FROM [dbo].[Form] form_row" in sql:
            return _FakeResult((self.event_country,) if self.event_country else None)
        if "FROM [dbo].[Company] company INNER JOIN [ref].[Country]" in sql:
            return _FakeResult((self.company_country,) if self.company_country else None)
        if "FROM [dbo].[User] user_row" in sql:
            return _FakeResult((self.user_country,) if self.user_country else None)
        if "FROM [config].[AppSetting]" in sql:
            if params.get("key") == "form_ai.default_audience_locale":
                return _FakeResult((self.app_locale,) if self.app_locale else None)
            if params.get("key") == "form_ai.default_brand_posture":
                return _FakeResult((self.app_brand_posture,) if self.app_brand_posture else None)
        if "SELECT TOP 1 [BrandPosture], [BrandHeritageOrigin]" in sql:
            if self.company_brand_posture:
                return _FakeResult((self.company_brand_posture, self.company_brand_origin))
            return _FakeResult(None)
        raise AssertionError(f"Unexpected SQL: {sql}")


def test_resolve_audience_locale_prefers_explicit_request():
    session = _ResolutionSession(event_country="NZ", company_country="US", user_country="CA")

    resolved = service._resolve_audience_locale(
        "AU",
        actor_user_id=1,
        actor_company_id=2,
        runtime_context={"formId": "42"},
        db_session=session,
    )

    assert resolved == {"resolved": "AU", "source": "request.audienceLocale"}


def test_resolve_audience_locale_fallback_chain_event_company_user_setting_fallback():
    assert service._resolve_audience_locale(
        None,
        1,
        2,
        {"formId": "42"},
        _ResolutionSession(event_country="GB"),
    ) == {"resolved": "UK", "source": "Event.CountryID"}

    assert service._resolve_audience_locale(
        None,
        1,
        2,
        {"formId": "42"},
        _ResolutionSession(company_country="NZ"),
    ) == {"resolved": "NZ", "source": "Company.CountryID"}

    assert service._resolve_audience_locale(
        None,
        1,
        2,
        {"formId": "42"},
        _ResolutionSession(user_country="CA"),
    ) == {"resolved": "CA", "source": "User.CountryID"}

    assert service._resolve_audience_locale(
        None,
        1,
        2,
        {"formId": "42"},
        _ResolutionSession(app_locale="IE"),
    ) == {"resolved": "IE", "source": "config.AppSetting"}

    assert service._resolve_audience_locale(None, None, None, None, None) == {
        "resolved": "AU",
        "source": "fallback",
    }


def test_resolve_brand_posture_prefers_explicit_then_company_then_setting():
    assert service._resolve_brand_posture("heritage", "us", 2, _ResolutionSession()) == {
        "resolved": "heritage",
        "heritageOrigin": "US",
        "source": "request.brandPosture",
    }

    assert service._resolve_brand_posture(
        None,
        None,
        2,
        _ResolutionSession(company_brand_posture="neutral", company_brand_origin=None),
    ) == {
        "resolved": "neutral",
        "heritageOrigin": None,
        "source": "Company.BrandPosture",
    }

    assert service._resolve_brand_posture(None, None, 2, _ResolutionSession()) == {
        "resolved": "local",
        "heritageOrigin": None,
        "source": "config.AppSetting",
    }


def test_invalid_locale_enum_rejected_by_request_schema():
    with pytest.raises(ValidationError):
        FormAiGenerateRequest(prompt="Create a form", audienceLocale="XX")
