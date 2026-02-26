"""
Pre-Epic-6 guardrail preflight checks.

These checks are intended to fail fast when required reference/config
rows are missing in the active test database.
"""
from sqlalchemy import select

from models.config.app_setting import AppSetting
from models.ref.country import Country
from models.ref.joined_via import JoinedVia
from models.ref.setting_category import SettingCategory
from models.ref.setting_type import SettingType
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.user_status import UserStatus


def test_seed_and_config_parity_preflight(db_session):
    """
    Verify required ref/config rows used by integration suites.

    This is deterministic and should be runnable locally and in CI:
    - Local: pytest backend/tests/test_preflight_seed_config_parity.py -q
    - CI: same command as a hard gate step
    """
    checks = [
        ("ref.UserStatus.StatusCode=active", lambda db: db.execute(
            select(UserStatus).where(UserStatus.StatusCode == "active")
        ).scalar_one_or_none()),
        ("ref.Country.CountryCode=AU", lambda db: db.execute(
            select(Country).where(Country.CountryCode == "AU")
        ).scalar_one_or_none()),
        ("ref.UserCompanyRole.RoleCode=company_admin", lambda db: db.execute(
            select(UserCompanyRole).where(UserCompanyRole.RoleCode == "company_admin")
        ).scalar_one_or_none()),
        ("ref.UserCompanyRole.RoleCode=company_user", lambda db: db.execute(
            select(UserCompanyRole).where(UserCompanyRole.RoleCode == "company_user")
        ).scalar_one_or_none()),
        ("ref.UserCompanyStatus.StatusCode=active", lambda db: db.execute(
            select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == "active")
        ).scalar_one_or_none()),
        ("ref.JoinedVia.MethodCode=signup", lambda db: db.execute(
            select(JoinedVia).where(JoinedVia.MethodCode == "signup")
        ).scalar_one_or_none()),
        ("ref.UserInvitationStatus.StatusCode=pending", lambda db: db.execute(
            select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "pending")
        ).scalar_one_or_none()),
        ("ref.SettingCategory.CategoryCode=authentication", lambda db: db.execute(
            select(SettingCategory).where(SettingCategory.CategoryCode == "authentication")
        ).scalar_one_or_none()),
        ("ref.SettingType.TypeCode=integer", lambda db: db.execute(
            select(SettingType).where(SettingType.TypeCode == "integer")
        ).scalar_one_or_none()),
        ("config.AppSetting.SettingKey=ACCESS_TOKEN_EXPIRY_MINUTES", lambda db: db.execute(
            select(AppSetting).where(
                AppSetting.SettingKey == "ACCESS_TOKEN_EXPIRY_MINUTES",
                AppSetting.IsActive == True,
                AppSetting.IsDeleted == False,
            )
        ).scalar_one_or_none()),
        ("config.AppSetting.SettingKey=REFRESH_TOKEN_EXPIRY_DAYS", lambda db: db.execute(
            select(AppSetting).where(
                AppSetting.SettingKey == "REFRESH_TOKEN_EXPIRY_DAYS",
                AppSetting.IsActive == True,
                AppSetting.IsDeleted == False,
            )
        ).scalar_one_or_none()),
    ]

    missing = [name for name, query in checks if query(db_session) is None]
    assert not missing, (
        "Seed/config parity preflight failed. Missing required rows: "
        + ", ".join(missing)
        + ". Ensure reference/config seed data is loaded before running integration suites."
    )
