"""Story 6.5d: ref.AudienceLocale + §11.1 seeds.

Revision ID: 089
Revises: 088
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "089"
down_revision = "088"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "AudienceLocale",
        sa.Column("AudienceLocaleID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Code", mssql.NVARCHAR(length=30), nullable=False),
        sa.Column("DisplayName", mssql.NVARCHAR(length=28), nullable=False),
        sa.Column("FlagEmoji", mssql.NVARCHAR(length=10), nullable=True),
        sa.Column("Description", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("ClarificationSummary", mssql.NVARCHAR(length=500), nullable=False),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.PrimaryKeyConstraint("AudienceLocaleID", name="PK_AudienceLocale"),
        sa.UniqueConstraint("Code", name="UQ_AudienceLocale_Code"),
        schema="ref",
    )

    op.execute(
        """
        INSERT INTO [ref].[AudienceLocale]
            ([Code], [DisplayName], [FlagEmoji], [Description], [ClarificationSummary], [SortOrder], [IsActive])
        VALUES
        (N'AU', N'Australia', N'🇦🇺', N'dd/mm/yyyy, AUD, Privacy Act',
         N'Audience Locale: Australia (AU) – use dd/mm/yyyy dates, AUD currency, and Australian Privacy Act expectations.', 10, 1),
        (N'NZ', N'New Zealand', N'🇳🇿', N'Similar to AU, minor legal differences',
         N'Audience Locale: New Zealand (NZ) – use dd/mm/yyyy dates, NZD, and local privacy expectations.', 20, 1),
        (N'UK', N'United Kingdom', N'🇬🇧', N'GDPR, dd/mm/yyyy, £',
         N'Audience Locale: United Kingdom (UK) – use dd/mm/yyyy dates, GBP, and GDPR-aligned wording.', 30, 1),
        (N'US', N'United States', N'🇺🇸', N'mm/dd/yyyy, USD, CCPA',
         N'Audience Locale: United States (US) – use mm/dd/yyyy dates, USD, and CCPA-aware privacy language.', 40, 1),
        (N'CA', N'Canada', N'🇨🇦', N'Bilingual potential, CAD',
         N'Audience Locale: Canada (CA) – use appropriate date format for Canadian respondents, CAD, and bilingual-friendly tone where relevant.', 50, 1),
        (N'IE', N'Ireland', N'🇮🇪', N'GDPR, dd/mm/yyyy, €',
         N'Audience Locale: Ireland (IE) – use dd/mm/yyyy dates, EUR, and GDPR-aligned wording.', 60, 1),
        (N'DE', N'Germany', N'🇩🇪', N'GDPR, formal tone',
         N'Audience Locale: Germany (DE) – use formal register, GDPR-aligned consent language, and European date conventions.', 70, 1),
        (N'INTL_ONLINE', N'International (Online)', N'🌐', N'Neutral formats, English default',
         N'Audience Locale: International (Online) – use neutral formats and globally understandable English.', 80, 1),
        (N'APAC', N'Asia-Pacific', N'🌏', N'Regional online events',
         N'Audience Locale: Asia-Pacific (APAC) – use region-appropriate tone and neutral international formats for online events.', 90, 1),
        (N'EU', N'European Union', N'🇪🇺', N'GDPR emphasis',
         N'Audience Locale: European Union (EU) – emphasise GDPR rights, consent, and data minimisation.', 100, 1),
        (N'NEUTRAL', N'Neutral / Global', N'🌍', N'Fallback locale',
         N'Audience Locale: Neutral / Global – use clear, globally neutral language and widely understood formats.', 110, 1);
        """
    )


def downgrade() -> None:
    op.drop_table("AudienceLocale", schema="ref")
