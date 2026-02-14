"""Form Defaults + Component Catalog (Story 5.2 T01)

Revision ID: 039
Revises: 038
Create Date: 2026-02-14

Story: 5.2 - Company Form Defaults (Brand System)
Task: T01 - Database Form Defaults + Component Catalog
Purpose:
- ref.FormDefaultsSchemaVersion + seed (SchemaVersion=1)
- dbo.GlobalFormDefaults, dbo.GlobalFormDefaultsVersion
- dbo.CompanyFormDefaults, dbo.CompanyFormDefaultsVersion
- Seed GlobalFormDefaults (theme, globalStyles, defaultGridLayoutsByComponent, canvasSettings)
- ref.ComponentScope + seed (Global, Country, Company)
- ref.ComponentType + seed (MVP types)
- dbo.FormBuilderComponent + seed (global-scoped MVP components)

References: docs/stories/STORY-5.2-DATA-SCHEMA.md, docs/stories/COMPONENT-CATALOG-SCHEMA-DESIGN.md
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql


revision = "039"
down_revision = "038"
branch_labels = None
depends_on = None

# DefaultsJSON for GlobalFormDefaults seed (Schema Version 1)
DEFAULTS_JSON = """{
  "schemaVersion": "1.0",
  "theme": {
    "primaryColor": "#0055FF",
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter"
  },
  "globalStyles": {
    "fontFamily": "Inter",
    "fontSize": 14,
    "fontWeight": 400,
    "labelFontFamily": "Inter",
    "defaultLayout": "vertical",
    "defaultObjectLayout": "vertical",
    "defaultGridLayoutsByComponent": {
      "text": {
        "vertical": {"rows": 3, "columns": 1, "cellAssignments": {"0-0": "label", "1-0": "input", "2-0": "validation"}},
        "horizontal": {"rows": 2, "columns": 3, "cellAssignments": {"0-0": "label", "0-1": "input", "0-2": "validation"}}
      },
      "number": {
        "vertical": {"rows": 3, "columns": 1, "cellAssignments": {"0-0": "label", "1-0": "input", "2-0": "validation"}},
        "horizontal": {"rows": 2, "columns": 3, "cellAssignments": {"0-0": "label", "0-1": "input", "0-2": "validation"}}
      },
      "email": {
        "vertical": {"rows": 3, "columns": 1, "cellAssignments": {"0-0": "label", "1-0": "input", "2-0": "validation"}},
        "horizontal": {"rows": 2, "columns": 3, "cellAssignments": {"0-0": "label", "0-1": "input", "0-2": "validation"}}
      }
    }
  },
  "canvasSettings": {
    "width": 1920,
    "height": 980,
    "gridSize": 8
  },
  "background": {"asset": {}, "placement": {}}
}"""


def upgrade() -> None:
    op.execute(
        "IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA [ref]')"
    )

    # ---------------------------------------------------------------------
    # ref.FormDefaultsSchemaVersion
    # ---------------------------------------------------------------------
    op.create_table(
        "FormDefaultsSchemaVersion",
        sa.Column("FormDefaultsSchemaVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("SchemaVersion", sa.Integer(), nullable=False),
        sa.Column("SchemaName", sa.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("SchemaDocument", sa.Text(), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("FormDefaultsSchemaVersionID", name="PK_FormDefaultsSchemaVersion_FormDefaultsSchemaVersionID"),
        sa.UniqueConstraint("SchemaVersion", name="UQ_FormDefaultsSchemaVersion_SchemaVersion"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_FormDefaultsSchemaVersion_User_CreatedBy"),
        schema="ref",
    )
    op.create_index(
        "IX_FormDefaultsSchemaVersion_IsActive",
        "FormDefaultsSchemaVersion",
        ["IsActive"],
        unique=False,
        schema="ref",
    )

    # Seed FormDefaultsSchemaVersion (SchemaVersion = 1)
    op.execute(
        """
        INSERT INTO [ref].[FormDefaultsSchemaVersion] (SchemaVersion, SchemaName, Description, IsActive)
        VALUES (1, 'Form Defaults v1', 'MVP schema for theme, globalStyles, defaultGridLayoutsByComponent, canvasSettings', 1);
        """
    )

    # ---------------------------------------------------------------------
    # dbo.GlobalFormDefaults
    # ---------------------------------------------------------------------
    op.create_table(
        "GlobalFormDefaults",
        sa.Column("GlobalFormDefaultsID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormDefaultsSchemaVersionID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("DefaultsJSON", sa.Text(), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("GlobalFormDefaultsID", name="PK_GlobalFormDefaults_GlobalFormDefaultsID"),
        sa.ForeignKeyConstraint(
            ["FormDefaultsSchemaVersionID"],
            ["ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"],
            name="FK_GlobalFormDefaults_FormDefaultsSchemaVersion",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_GlobalFormDefaults_User_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_GlobalFormDefaults_User_UpdatedBy"),
        schema="dbo",
    )
    op.create_index(
        "IX_GlobalFormDefaults_IsActive",
        "GlobalFormDefaults",
        ["IsActive"],
        unique=True,
        schema="dbo",
        mssql_where="IsActive = 1",
    )

    # ---------------------------------------------------------------------
    # dbo.GlobalFormDefaultsVersion
    # ---------------------------------------------------------------------
    op.create_table(
        "GlobalFormDefaultsVersion",
        sa.Column("GlobalFormDefaultsVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("FormDefaultsSchemaVersionID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("DefaultsJSON", sa.Text(), nullable=False),
        sa.Column("ChangeSummary", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("GlobalFormDefaultsVersionID", name="PK_GlobalFormDefaultsVersion_GlobalFormDefaultsVersionID"),
        sa.ForeignKeyConstraint(
            ["FormDefaultsSchemaVersionID"],
            ["ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"],
            name="FK_GlobalFormDefaultsVersion_FormDefaultsSchemaVersion",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_GlobalFormDefaultsVersion_User_CreatedBy"),
        schema="dbo",
    )
    op.create_index(
        "IX_GlobalFormDefaultsVersion_VersionNumber",
        "GlobalFormDefaultsVersion",
        ["VersionNumber"],
        unique=False,
        schema="dbo",
    )

    # ---------------------------------------------------------------------
    # dbo.CompanyFormDefaults
    # ---------------------------------------------------------------------
    op.create_table(
        "CompanyFormDefaults",
        sa.Column("CompanyFormDefaultsID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("FormDefaultsSchemaVersionID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("DefaultsJSON", sa.Text(), nullable=False),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("CompanyFormDefaultsID", name="PK_CompanyFormDefaults_CompanyFormDefaultsID"),
        sa.UniqueConstraint("CompanyID", name="UQ_CompanyFormDefaults_CompanyID"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_CompanyFormDefaults_Company_CompanyID"),
        sa.ForeignKeyConstraint(
            ["FormDefaultsSchemaVersionID"],
            ["ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"],
            name="FK_CompanyFormDefaults_FormDefaultsSchemaVersion",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_CompanyFormDefaults_User_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_CompanyFormDefaults_User_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_CompanyFormDefaults_User_DeletedBy"),
        schema="dbo",
    )
    op.create_index(
        "IX_CompanyFormDefaults_CompanyID",
        "CompanyFormDefaults",
        ["CompanyID"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_CompanyFormDefaults_IsActive_IsDeleted",
        "CompanyFormDefaults",
        ["IsActive", "IsDeleted"],
        unique=False,
        schema="dbo",
    )

    # ---------------------------------------------------------------------
    # dbo.CompanyFormDefaultsVersion
    # ---------------------------------------------------------------------
    op.create_table(
        "CompanyFormDefaultsVersion",
        sa.Column("CompanyFormDefaultsVersionID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("CompanyID", sa.BigInteger(), nullable=False),
        sa.Column("FormDefaultsSchemaVersionID", sa.BigInteger(), nullable=False),
        sa.Column("VersionNumber", sa.Integer(), nullable=False),
        sa.Column("DefaultsJSON", sa.Text(), nullable=False),
        sa.Column("ChangeSummary", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("CompanyFormDefaultsVersionID", name="PK_CompanyFormDefaultsVersion_CompanyFormDefaultsVersionID"),
        sa.ForeignKeyConstraint(["CompanyID"], ["dbo.Company.CompanyID"], name="FK_CompanyFormDefaultsVersion_Company_CompanyID"),
        sa.ForeignKeyConstraint(
            ["FormDefaultsSchemaVersionID"],
            ["ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"],
            name="FK_CompanyFormDefaultsVersion_FormDefaultsSchemaVersion",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_CompanyFormDefaultsVersion_User_CreatedBy"),
        schema="dbo",
    )
    op.create_index(
        "IX_CompanyFormDefaultsVersion_CompanyID_VersionNumber",
        "CompanyFormDefaultsVersion",
        ["CompanyID", "VersionNumber"],
        unique=False,
        schema="dbo",
    )

    # Seed GlobalFormDefaults (one row, IsActive=1)
    escaped_defaults = DEFAULTS_JSON.replace("'", "''")
    op.execute(
        f"""
        DECLARE @SchemaVersionID BIGINT;
        SELECT @SchemaVersionID = FormDefaultsSchemaVersionID FROM [ref].[FormDefaultsSchemaVersion] WHERE SchemaVersion = 1;
        INSERT INTO [dbo].[GlobalFormDefaults] (FormDefaultsSchemaVersionID, VersionNumber, DefaultsJSON, IsActive)
        VALUES (@SchemaVersionID, 1, N'{escaped_defaults}', 1);
        """
    )

    # ---------------------------------------------------------------------
    # ref.ComponentScope
    # ---------------------------------------------------------------------
    op.create_table(
        "ComponentScope",
        sa.Column("ComponentScopeID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ScopeCode", sa.NVARCHAR(length=20), nullable=False),
        sa.Column("ScopeName", sa.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.PrimaryKeyConstraint("ComponentScopeID", name="PK_ComponentScope_ComponentScopeID"),
        sa.UniqueConstraint("ScopeCode", name="UQ_ComponentScope_ScopeCode"),
        schema="ref",
    )

    op.execute(
        """
        INSERT INTO [ref].[ComponentScope] (ScopeCode, ScopeName, Description, IsActive) VALUES
        ('Global', 'Global', 'Platform-wide; all forms, all countries, all companies', 1),
        ('Country', 'Country', 'Scoped to a specific country', 1),
        ('Company', 'Company', 'Scoped to a specific company', 1);
        """
    )

    # ---------------------------------------------------------------------
    # ref.ComponentType
    # ---------------------------------------------------------------------
    op.create_table(
        "ComponentType",
        sa.Column("ComponentTypeID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ComponentTypeCode", sa.NVARCHAR(length=50), nullable=False),
        sa.Column("DisplayName", sa.NVARCHAR(length=100), nullable=False),
        sa.Column("Description", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("Category", sa.NVARCHAR(length=50), nullable=True),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("ComponentTypeID", name="PK_ComponentType_ComponentTypeID"),
        sa.UniqueConstraint("ComponentTypeCode", name="UQ_ComponentType_ComponentTypeCode"),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_ComponentType_User_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_ComponentType_User_UpdatedBy"),
        schema="ref",
    )
    op.create_index(
        "IX_ComponentType_ComponentTypeCode",
        "ComponentType",
        ["ComponentTypeCode"],
        unique=False,
        schema="ref",
    )
    op.create_index(
        "IX_ComponentType_IsActive_SortOrder",
        "ComponentType",
        ["IsActive", "SortOrder"],
        unique=False,
        schema="ref",
    )

    # Seed ComponentType (MVP types)
    op.execute(
        """
        INSERT INTO [ref].[ComponentType] (ComponentTypeCode, DisplayName, Category, SortOrder) VALUES
        ('text', 'Text Input', 'input', 10),
        ('number', 'Number', 'input', 20),
        ('email', 'Email', 'input', 30),
        ('phone', 'Phone', 'input', 40),
        ('first-name', 'First Name', 'input', 50),
        ('date', 'Date', 'input', 60),
        ('checkbox', 'Checkbox', 'input', 70),
        ('radio', 'Radio', 'input', 80),
        ('textarea', 'Text Area', 'input', 90),
        ('dropdown', 'Dropdown', 'input', 100),
        ('terms', 'Terms & Conditions', 'input', 110),
        ('submit-button', 'Submit Button', 'input', 120),
        ('header', 'Header', 'display', 130),
        ('divider', 'Divider', 'display', 140);
        """
    )

    # ---------------------------------------------------------------------
    # dbo.FormBuilderComponent
    # ---------------------------------------------------------------------
    op.create_table(
        "FormBuilderComponent",
        sa.Column("FormBuilderComponentID", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ComponentTypeID", sa.BigInteger(), nullable=False),
        sa.Column("ComponentScopeID", sa.BigInteger(), nullable=False),
        sa.Column("CountryID", sa.BigInteger(), nullable=True),
        sa.Column("CompanyID", sa.BigInteger(), nullable=True),
        sa.Column("ComponentCode", sa.NVARCHAR(length=100), nullable=False),
        sa.Column("DisplayName", sa.NVARCHAR(length=200), nullable=False),
        sa.Column("Description", sa.NVARCHAR(length=500), nullable=True),
        sa.Column("SortOrder", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("PropertiesSchemaJSON", sa.Text(), nullable=True),
        sa.Column("StructureJSON", sa.Text(), nullable=True),
        sa.Column("DefaultGridLayoutVerticalJSON", sa.Text(), nullable=True),
        sa.Column("DefaultGridLayoutHorizontalJSON", sa.Text(), nullable=True),
        sa.Column("ValidationConfigJSON", sa.Text(), nullable=True),
        sa.Column("GlobalStylesRelevantKeys", sa.Text(), nullable=True),
        sa.Column("IsActive", mssql.BIT(), nullable=False, server_default=sa.text("1")),
        sa.Column("IsDeleted", mssql.BIT(), nullable=False, server_default=sa.text("0")),
        sa.Column("CreatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("CreatedBy", sa.BigInteger(), nullable=True),
        sa.Column("UpdatedDate", mssql.DATETIME2(), nullable=False, server_default=sa.func.getutcdate()),
        sa.Column("UpdatedBy", sa.BigInteger(), nullable=True),
        sa.Column("DeletedDate", mssql.DATETIME2(), nullable=True),
        sa.Column("DeletedBy", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("FormBuilderComponentID", name="PK_FormBuilderComponent_FormBuilderComponentID"),
        sa.ForeignKeyConstraint(
            ["ComponentTypeID"],
            ["ref.ComponentType.ComponentTypeID"],
            name="FK_FormBuilderComponent_ComponentType",
        ),
        sa.ForeignKeyConstraint(
            ["ComponentScopeID"],
            ["ref.ComponentScope.ComponentScopeID"],
            name="FK_FormBuilderComponent_ComponentScope",
        ),
        sa.ForeignKeyConstraint(
            ["CountryID"],
            ["ref.Country.CountryID"],
            name="FK_FormBuilderComponent_Country",
        ),
        sa.ForeignKeyConstraint(
            ["CompanyID"],
            ["dbo.Company.CompanyID"],
            name="FK_FormBuilderComponent_Company",
        ),
        sa.ForeignKeyConstraint(["CreatedBy"], ["dbo.User.UserID"], name="FK_FormBuilderComponent_User_CreatedBy"),
        sa.ForeignKeyConstraint(["UpdatedBy"], ["dbo.User.UserID"], name="FK_FormBuilderComponent_User_UpdatedBy"),
        sa.ForeignKeyConstraint(["DeletedBy"], ["dbo.User.UserID"], name="FK_FormBuilderComponent_User_DeletedBy"),
        schema="dbo",
    )
    op.create_index(
        "IX_FormBuilderComponent_ComponentTypeID",
        "FormBuilderComponent",
        ["ComponentTypeID"],
        unique=False,
        schema="dbo",
    )
    op.create_index(
        "IX_FormBuilderComponent_Scope_Country",
        "FormBuilderComponent",
        ["ComponentScopeID", "CountryID"],
        unique=False,
        schema="dbo",
        mssql_where="CountryID IS NOT NULL",
    )
    op.create_index(
        "IX_FormBuilderComponent_Scope_Company",
        "FormBuilderComponent",
        ["ComponentScopeID", "CompanyID"],
        unique=False,
        schema="dbo",
        mssql_where="CompanyID IS NOT NULL",
    )
    op.create_index(
        "IX_FormBuilderComponent_ScopeGlobal",
        "FormBuilderComponent",
        ["ComponentScopeID"],
        unique=False,
        schema="dbo",
        mssql_where="CountryID IS NULL AND CompanyID IS NULL",
    )
    op.create_index(
        "IX_FormBuilderComponent_IsActive_IsDeleted",
        "FormBuilderComponent",
        ["IsActive", "IsDeleted"],
        unique=False,
        schema="dbo",
    )

    # Seed FormBuilderComponent (global-scoped MVP components)
    _seed_form_builder_components(op)


def _escape_json_for_sqlalchemy(s: str) -> str:
    """Escape JSON so SQLAlchemy does not treat :true, :false, :1, etc. as bind parameters."""
    s = s.replace(":true", ": true").replace(":false", ": false")
    # Escape :N (numeric) - e.g. "order":1, "rows":3
    for i in range(10):
        s = s.replace(f":{i}", f": {i}")
    return s


def _esc_json(s: str) -> str:
    """Escape JSON for SQL: single quotes + SQLAlchemy bind param avoidance."""
    return _escape_json_for_sqlalchemy(s.replace("'", "''"))


def _seed_form_builder_components(op) -> None:
    """Insert global-scoped MVP components with schemas and layouts."""
    scope_global_id = "SELECT ComponentScopeID FROM [ref].[ComponentScope] WHERE ScopeCode = 'Global'"
    # Standard structure for field components (label, input, validation)
    std_structure = '{"objects":[{"id":"label","type":"label","archetype":"PrimaryLabel","required":true,"order":1},{"id":"input","type":"input","archetype":"InputControl","required":true,"order":2},{"id":"validation","type":"validation","archetype":"HelperText","required":false,"order":3,"conditional":{"type":"validation"}}],"defaultLayout":"vertical"}'
    layout_vertical = '{"rows":3,"columns":1,"cellAssignments":{"0-0":"label","1-0":"input","2-0":"validation"}}'
    layout_horizontal = '{"rows":2,"columns":3,"cellAssignments":{"0-0":"label","0-1":"input","0-2":"validation"}}'
    props_schema = '{"fields":[{"key":"label","type":"string"},{"key":"placeholder","type":"string"},{"key":"required","type":"boolean"},{"key":"validation","type":"object"},{"key":"styleOverrides","type":"object"}]}'
    terms_structure = '{"objects":[{"id":"checkbox","type":"input","required":true,"order":1},{"id":"label","type":"label","required":true,"order":2},{"id":"validation","type":"validation","required":false,"order":3,"conditional":{"type":"validation"}}],"defaultLayout":"horizontal"}'
    terms_layout_v = '{"rows":2,"columns":1,"cellAssignments":{"0-0":"checkbox","1-0":"label"}}'
    terms_layout_h = '{"rows":1,"columns":3,"cellAssignments":{"0-0":"checkbox","0-1":"label","0-2":"validation"}}'
    submit_structure = '{"objects":[{"id":"button","type":"action","required":true,"order":1},{"id":"loading","type":"status","required":false,"order":2,"conditional":{"type":"prop","prop":"showLoadingState"}},{"id":"validation","type":"validation","required":false,"order":3,"conditional":{"type":"validation"}}],"defaultLayout":"vertical"}'
    submit_layout_v = '{"rows":2,"columns":1,"cellAssignments":{"0-0":"button","1-0":"validation"}}'
    submit_layout_h = '{"rows":1,"columns":2,"cellAssignments":{"0-0":"button","0-1":"validation"}}'
    display_structure = '{"objects":[{"id":"content","type":"custom","required":true,"order":1}],"defaultLayout":"vertical"}'
    display_layout = '{"rows":1,"columns":1,"cellAssignments":{"0-0":"content"}}'

    components = [
        ("text", "Text Input", std_structure, layout_vertical, layout_horizontal, props_schema, 10),
        ("number", "Number", std_structure, layout_vertical, layout_horizontal, props_schema, 20),
        ("email", "Email", std_structure, layout_vertical, layout_horizontal, props_schema, 30),
        ("phone", "Phone", std_structure, layout_vertical, layout_horizontal, props_schema, 40),
        ("first-name", "First Name", std_structure, layout_vertical, layout_horizontal, props_schema, 50),
        ("date", "Date", std_structure, layout_vertical, layout_horizontal, props_schema, 60),
        ("checkbox", "Checkbox", std_structure, layout_vertical, layout_horizontal, props_schema, 70),
        ("radio", "Radio", std_structure, layout_vertical, layout_horizontal, '{"fields":[{"key":"label","type":"string"},{"key":"options","type":"array"},{"key":"required","type":"boolean"},{"key":"styleOverrides","type":"object"}]}', 80),
        ("textarea", "Text Area", std_structure, layout_vertical, layout_horizontal, props_schema, 90),
        ("dropdown", "Dropdown", std_structure, layout_vertical, layout_horizontal, '{"fields":[{"key":"label","type":"string"},{"key":"options","type":"array"},{"key":"placeholder","type":"string"},{"key":"required","type":"boolean"},{"key":"styleOverrides","type":"object"}]}', 100),
        ("terms", "Terms & Conditions", terms_structure, terms_layout_v, terms_layout_h, props_schema, 110),
        ("submit-button", "Submit Button", submit_structure, submit_layout_v, submit_layout_h, '{"fields":[{"key":"label","type":"string"},{"key":"styleOverrides","type":"object"}]}', 120),
        ("header", "Header", display_structure, display_layout, display_layout, '{"fields":[{"key":"text","type":"string"},{"key":"level","type":"number"},{"key":"styleOverrides","type":"object"}]}', 130),
        ("divider", "Divider", display_structure, display_layout, display_layout, '{"fields":[{"key":"width","type":"number"},{"key":"styleOverrides","type":"object"}]}', 140),
    ]

    for code, display_name, struct, layout_v, layout_h, props, sort_order in components:
        op.execute(
            f"""
            INSERT INTO [dbo].[FormBuilderComponent] (
                ComponentTypeID, ComponentScopeID, ComponentCode, DisplayName, SortOrder,
                PropertiesSchemaJSON, StructureJSON, DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON
            )
            SELECT ct.ComponentTypeID, ({scope_global_id}), N'{code}', N'{display_name}', {sort_order},
                N'{_esc_json(props)}', N'{_esc_json(struct)}',
                N'{_esc_json(layout_v)}', N'{_esc_json(layout_h)}'
            FROM [ref].[ComponentType] ct
            WHERE ct.ComponentTypeCode = N'{code}' AND ct.IsActive = 1
            AND NOT EXISTS (SELECT 1 FROM [dbo].[FormBuilderComponent] fbc
                JOIN [ref].[ComponentType] c ON fbc.ComponentTypeID = c.ComponentTypeID
                WHERE c.ComponentTypeCode = N'{code}' AND fbc.ComponentScopeID = ({scope_global_id}) AND fbc.IsDeleted = 0);
            """
        )


def downgrade() -> None:
    op.drop_index("IX_FormBuilderComponent_IsActive_IsDeleted", table_name="FormBuilderComponent", schema="dbo")
    op.drop_index("IX_FormBuilderComponent_ScopeGlobal", table_name="FormBuilderComponent", schema="dbo")
    op.drop_index("IX_FormBuilderComponent_Scope_Company", table_name="FormBuilderComponent", schema="dbo")
    op.drop_index("IX_FormBuilderComponent_Scope_Country", table_name="FormBuilderComponent", schema="dbo")
    op.drop_index("IX_FormBuilderComponent_ComponentTypeID", table_name="FormBuilderComponent", schema="dbo")
    op.drop_table("FormBuilderComponent", schema="dbo")

    op.drop_index("IX_ComponentType_IsActive_SortOrder", table_name="ComponentType", schema="ref")
    op.drop_index("IX_ComponentType_ComponentTypeCode", table_name="ComponentType", schema="ref")
    op.drop_table("ComponentType", schema="ref")

    op.drop_table("ComponentScope", schema="ref")

    op.drop_index("IX_GlobalFormDefaultsVersion_VersionNumber", table_name="GlobalFormDefaultsVersion", schema="dbo")
    op.drop_table("GlobalFormDefaultsVersion", schema="dbo")
    op.drop_index("IX_GlobalFormDefaults_IsActive", table_name="GlobalFormDefaults", schema="dbo")
    op.drop_table("GlobalFormDefaults", schema="dbo")

    op.drop_index("IX_CompanyFormDefaultsVersion_CompanyID_VersionNumber", table_name="CompanyFormDefaultsVersion", schema="dbo")
    op.drop_table("CompanyFormDefaultsVersion", schema="dbo")
    op.drop_index("IX_CompanyFormDefaults_IsActive_IsDeleted", table_name="CompanyFormDefaults", schema="dbo")
    op.drop_index("IX_CompanyFormDefaults_CompanyID", table_name="CompanyFormDefaults", schema="dbo")
    op.drop_table("CompanyFormDefaults", schema="dbo")

    op.drop_index("IX_FormDefaultsSchemaVersion_IsActive", table_name="FormDefaultsSchemaVersion", schema="ref")
    op.drop_table("FormDefaultsSchemaVersion", schema="ref")
