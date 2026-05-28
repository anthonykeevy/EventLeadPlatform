"""Story 6.5d: EDF schema (RequiresNetwork, offline flag, AddressSearch cache) + AU components.

Revision ID: 088
Revises: 087
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "088"
down_revision = "087"
branch_labels = None
depends_on = None


def _esc(s: str) -> str:
    s = s.replace(":true", ": true").replace(":false", ": false")
    for i in range(10):
        s = s.replace(f":{i}", f": {i}")
    return s.replace("'", "''")


_ADDRESS_PROPS = _esc(
    '{"fields":[{"key":"label","type":"string","title":"Label"},'
    '{"key":"exportName","type":"string","default":"address","title":"Export name"},'
    '{"key":"deliveryMode","type":"string","default":"decomposed","title":"Delivery mode"},'
    '{"key":"concatenationTemplate","type":"string",'
    '"default":"{{line1}}, {{suburb}} {{state}} {{postcode}}","title":"Concatenation template"},'
    '{"key":"enabledOutputFields","type":"array",'
    '"default":["line1","suburb","state","postcode"],"title":"Enabled output fields"},'
    '{"key":"allowManualFallback","type":"boolean","default":true,"title":"Allow manual address entry"},'
    '{"key":"requireValidatedAddress","type":"boolean","default":false,'
    '"title":"Require validated address (PSMA)"},'
    '{"key":"editableAfterResolve","type":"boolean","default":true,'
    '"title":"Allow editing after autocomplete"},'
    '{"key":"showUnitField","type":"boolean","default":true,"title":"Show unit / line 2"},'
    '{"key":"allowDeliveryInstructions","type":"boolean","default":false,'
    '"title":"Show delivery instructions field"},'
    '{"key":"requireDeliveryInstructions","type":"boolean","default":false,'
    '"title":"Require delivery instructions"},'
    '{"key":"required","type":"boolean","default":false}]}'
)

_COMPANY_PROPS = _esc(
    '{"fields":[{"key":"label","type":"string","title":"Label"},'
    '{"key":"exportName","type":"string","default":"company","title":"Export name"},'
    '{"key":"deliveryMode","type":"string","default":"decomposed","title":"Delivery mode"},'
    '{"key":"enabledOutputFields","type":"array",'
    '"default":["legalEntityName","abn","entityType"],"title":"Enabled output fields"},'
    '{"key":"allowManualFallback","type":"boolean","default":true,"title":"Allow manual company entry"},'
    '{"key":"requireAbn","type":"boolean","default":false,"title":"Require ABN on submission"},'
    '{"key":"requireAbnWhenManual","type":"boolean","default":false,'
    '"title":"Require ABN when entering manually"},'
    '{"key":"autoSelectSingleResult","type":"boolean","default":true,'
    '"title":"Auto-select single search result"},'
    '{"key":"allowTradingAs","type":"boolean","default":true,"title":"Show Trading as field"},'
    '{"key":"warnOnInactiveAbn","type":"boolean","default":true,"title":"Warn when ABN is not Active"},'
    '{"key":"blockOnInactiveAbn","type":"boolean","default":false,'
    '"title":"Block submission for inactive ABN"},'
    '{"key":"required","type":"boolean","default":false}]}'
)

_STD_STRUCTURE = _esc(
    '{"objects":[{"id":"label","type":"label","required":true,"order":1},'
    '{"id":"input","type":"input","required":true,"order":2},'
    '{"id":"validation","type":"validation","required":false,"order":3,'
    '"conditional":{"type":"validation"}}],"defaultLayout":"vertical"}'
)
_LAYOUT = _esc('{"rows":3,"columns":1,"cellAssignments":{"0-0":"label","1-0":"input","2-0":"validation"}}')


def upgrade() -> None:
    op.execute(
        """
        IF COL_LENGTH('ref.ComponentType', 'RequiresNetwork') IS NULL
        ALTER TABLE [ref].[ComponentType]
        ADD [RequiresNetwork] BIT NOT NULL
            CONSTRAINT [DF_ComponentType_RequiresNetwork] DEFAULT 0;

        IF COL_LENGTH('ref.ComponentType', 'FallbackComponentCode') IS NULL
        ALTER TABLE [ref].[ComponentType]
        ADD [FallbackComponentCode] NVARCHAR(50) NULL;
        """
    )

    op.execute(
        """
        IF COL_LENGTH('dbo.Form', 'RequiresOfflineCapable') IS NULL
        ALTER TABLE [dbo].[Form]
        ADD [RequiresOfflineCapable] BIT NOT NULL
            CONSTRAINT [DF_Form_RequiresOfflineCapable] DEFAULT 0;
        """
    )

    op.create_table(
        "AddressSearch",
        sa.Column("OperationType", mssql.NVARCHAR(length=20), nullable=False),
        sa.Column("CacheKey", mssql.NVARCHAR(length=255), nullable=False),
        sa.Column("ResultIndex", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("Line1", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("Line2", mssql.NVARCHAR(length=200), nullable=True),
        sa.Column("Suburb", mssql.NVARCHAR(length=100), nullable=True),
        sa.Column("State", mssql.NVARCHAR(length=20), nullable=True),
        sa.Column("Postcode", mssql.NVARCHAR(length=20), nullable=True),
        sa.Column("FormattedAddress", mssql.NVARCHAR(length=500), nullable=True),
        sa.Column("PsmaAddressId", mssql.NVARCHAR(length=100), nullable=True),
        sa.Column("FullResponse", mssql.NVARCHAR(length=None), nullable=False),
        sa.Column("SearchDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("ExpiresAt", mssql.DATETIME2(), nullable=False),
        sa.Column("HitCount", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("LastHitAt", mssql.DATETIME2(), nullable=True),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("CompanyID", sa.BigInteger(), nullable=True),
        sa.Column("UserID", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint(
            "OperationType",
            "CacheKey",
            "ResultIndex",
            name="PK_AddressSearch",
        ),
        schema="cache",
    )
    op.create_index(
        "IX_AddressSearch_ExpiresAt",
        "AddressSearch",
        ["ExpiresAt"],
        unique=False,
        schema="cache",
    )

    for code, display, category, sort_order, requires_network, fallback in [
        ("address-lookup-au", "Address Lookup (AU)", "input", 200, 1, "address"),
        ("company-lookup-abr", "Company Lookup (ABR)", "input", 210, 1, "text"),
    ]:
        op.execute(
            f"""
            IF NOT EXISTS (
                SELECT 1 FROM [ref].[ComponentType]
                WHERE [ComponentTypeCode] = N'{code}'
            )
            INSERT INTO [ref].[ComponentType]
                ([ComponentTypeCode], [DisplayName], [Category], [SortOrder],
                 [IsActive], [RequiresNetwork], [FallbackComponentCode])
            VALUES (N'{code}', N'{display}', N'{category}', {sort_order}, 1,
                    {requires_network}, N'{fallback}');
            ELSE
            UPDATE [ref].[ComponentType]
            SET [RequiresNetwork] = {requires_network},
                [FallbackComponentCode] = N'{fallback}',
                [DisplayName] = N'{display}'
            WHERE [ComponentTypeCode] = N'{code}';
            """
        )

    op.execute(
        f"""
        DECLARE @AuCountryId BIGINT;
        DECLARE @CountryScopeId BIGINT;
        SELECT @AuCountryId = [CountryID]
        FROM [ref].[Country]
        WHERE [CountryCode] = N'AU' AND [IsDeleted] = 0;
        SELECT @CountryScopeId = [ComponentScopeID]
        FROM [ref].[ComponentScope]
        WHERE [ScopeCode] = N'Country';

        IF @AuCountryId IS NOT NULL AND @CountryScopeId IS NOT NULL
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM [dbo].[FormBuilderComponent] fbc
                INNER JOIN [ref].[ComponentType] ct ON fbc.ComponentTypeID = ct.ComponentTypeID
                WHERE ct.ComponentTypeCode = N'address-lookup-au'
                  AND fbc.CountryID = @AuCountryId AND fbc.IsDeleted = 0
            )
            INSERT INTO [dbo].[FormBuilderComponent] (
                ComponentTypeID, ComponentScopeID, CountryID, ComponentCode, DisplayName,
                SortOrder, PropertiesSchemaJSON, StructureJSON,
                DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON
            )
            SELECT ct.ComponentTypeID, @CountryScopeId, @AuCountryId,
                N'address-lookup-au', N'Address Lookup (AU)', 200,
                N'{_ADDRESS_PROPS}', N'{_STD_STRUCTURE}',
                N'{_LAYOUT}', N'{_LAYOUT}'
            FROM [ref].[ComponentType] ct
            WHERE ct.ComponentTypeCode = N'address-lookup-au';

            IF NOT EXISTS (
                SELECT 1 FROM [dbo].[FormBuilderComponent] fbc
                INNER JOIN [ref].[ComponentType] ct ON fbc.ComponentTypeID = ct.ComponentTypeID
                WHERE ct.ComponentTypeCode = N'company-lookup-abr'
                  AND fbc.CountryID = @AuCountryId AND fbc.IsDeleted = 0
            )
            INSERT INTO [dbo].[FormBuilderComponent] (
                ComponentTypeID, ComponentScopeID, CountryID, ComponentCode, DisplayName,
                SortOrder, PropertiesSchemaJSON, StructureJSON,
                DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON
            )
            SELECT ct.ComponentTypeID, @CountryScopeId, @AuCountryId,
                N'company-lookup-abr', N'Company Lookup (ABR)', 210,
                N'{_COMPANY_PROPS}', N'{_STD_STRUCTURE}',
                N'{_LAYOUT}', N'{_LAYOUT}'
            FROM [ref].[ComponentType] ct
            WHERE ct.ComponentTypeCode = N'company-lookup-abr';
        END
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE fbc
        FROM [dbo].[FormBuilderComponent] fbc
        INNER JOIN [ref].[ComponentType] ct ON fbc.ComponentTypeID = ct.ComponentTypeID
        WHERE ct.ComponentTypeCode IN (N'address-lookup-au', N'company-lookup-abr');
        """
    )
    op.execute(
        """
        DELETE FROM [ref].[ComponentType]
        WHERE ComponentTypeCode IN (N'address-lookup-au', N'company-lookup-abr');
        """
    )
    op.drop_index("IX_AddressSearch_ExpiresAt", table_name="AddressSearch", schema="cache")
    op.drop_table("AddressSearch", schema="cache")
    op.execute(
        """
        IF EXISTS (SELECT 1 FROM sys.default_constraints
                   WHERE name = 'DF_Form_RequiresOfflineCapable')
        ALTER TABLE [dbo].[Form] DROP CONSTRAINT [DF_Form_RequiresOfflineCapable];
        IF COL_LENGTH('dbo.Form', 'RequiresOfflineCapable') IS NOT NULL
        ALTER TABLE [dbo].[Form] DROP COLUMN [RequiresOfflineCapable];

        IF EXISTS (SELECT 1 FROM sys.default_constraints
                   WHERE name = 'DF_ComponentType_RequiresNetwork')
        ALTER TABLE [ref].[ComponentType] DROP CONSTRAINT [DF_ComponentType_RequiresNetwork];
        IF COL_LENGTH('ref.ComponentType', 'RequiresNetwork') IS NOT NULL
        ALTER TABLE [ref].[ComponentType] DROP COLUMN [RequiresNetwork];
        IF COL_LENGTH('ref.ComponentType', 'FallbackComponentCode') IS NOT NULL
        ALTER TABLE [ref].[ComponentType] DROP COLUMN [FallbackComponentCode];
        """
    )
