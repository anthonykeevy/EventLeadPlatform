"""Story 5.3: Schema Versioning - SchemaVersionString + SchemaDocument for DefinitionJSON

Revision ID: 040
Revises: 039
Create Date: 2026-02-16

Adds SchemaVersionString (e.g. "1.0") to ref.FormDefaultsSchemaVersion for API contract.
Populates SchemaDocument with DefinitionJSON JSON Schema from Pydantic model.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql
import json
import sys
import os

# Add backend to path for schema import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

revision = "040"
down_revision = "039"
branch_labels = None
depends_on = None


def _get_definition_json_schema() -> str:
    """Generate JSON Schema from FormDefinition Pydantic model."""
    from schemas.form_definition import FormDefinition
    return json.dumps(FormDefinition.model_json_schema())


def upgrade() -> None:
    # Add SchemaVersionString column (NVARCHAR(20))
    op.add_column(
        "FormDefaultsSchemaVersion",
        sa.Column("SchemaVersionString", mssql.NVARCHAR(length=20), nullable=True),
        schema="ref",
    )
    # Backfill existing row with SchemaVersionString
    op.execute(
        """
        UPDATE [ref].[FormDefaultsSchemaVersion]
        SET SchemaVersionString = N'1.0'
        WHERE SchemaVersion = 1;
        """
    )
    # Populate SchemaDocument using parameterized query
    from sqlalchemy import text
    conn = op.get_bind()
    schema_doc = _get_definition_json_schema()
    conn.execute(
        text("UPDATE [ref].[FormDefaultsSchemaVersion] SET SchemaDocument = :doc WHERE SchemaVersion = 1"),
        {"doc": schema_doc}
    )


def downgrade() -> None:
    op.drop_column(
        "FormDefaultsSchemaVersion",
        "SchemaVersionString",
        schema="ref",
    )
    # Clear SchemaDocument (optional; could leave as-is)
    op.execute(
        """
        UPDATE [ref].[FormDefaultsSchemaVersion]
        SET SchemaDocument = NULL
        WHERE SchemaVersion = 1;
        """
    )
