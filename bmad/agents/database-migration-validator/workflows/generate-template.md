# Generate Migration Template Workflow

**Agent:** Solomon (SQL Standards Sage)  
**Purpose:** Generate a PascalCase-compliant Alembic migration template

---

## Workflow

**Ask user for table details:**

```
"Excellent! Let us craft a migration worthy of your enterprise database."

**What table are we creating?**
1. Table name (PascalCase, e.g., 'Event', 'FormSubmission')
2. Table purpose (brief description)
```

**Ask for columns:**

```
"What columns shall this table hold? Provide column details:"

Format: ColumnName DataType [NULL|NOT NULL] [Description]

Examples:
- EventName NVARCHAR(255) NOT NULL - Name of the event
- EventStartDate DATETIME2 NOT NULL - Event start date (UTC)
- IsActive BIT NOT NULL - Active status flag

Type 'done' when finished adding columns.
```

**Ask for foreign keys:**

```
"Does this table reference other tables? (Foreign keys)"

Format: FKColumnName REFERENCES TableName(PKColumnName)

Examples:
- CompanyID REFERENCES Company(CompanyID)
- CreatedBy REFERENCES User(UserID)

Type 'done' if no foreign keys.
```

**Generate compliant migration:**

```python
"""Create {{TableName}} table

Revision ID: {{auto_generated_revision_id}}
Revises: {{previous_revision}}
Create Date: {{date}}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import NVARCHAR, DATETIME2, BIT, BIGINT

# Revision identifiers
revision = '{{revision_id}}'
down_revision = '{{previous_revision}}'
branch_labels = None
depends_on = None


def upgrade():
    """Create {{TableName}} table with enterprise standards"""
    op.create_table(
        '{{TableName}}',  # PascalCase ✓
        
        # Primary Key (Rule #2)
        sa.Column('{{TableName}}ID', BIGINT, sa.Identity(start=1, increment=1), primary_key=True),
        
        # User-defined columns
        {{for each column}}
        sa.Column('{{ColumnName}}', {{DataType}}, nullable={{nullable}}, comment='{{description}}'),
        {{end for}}
        
        # Foreign Keys (if any)
        {{for each FK}}
        sa.Column('{{FKColumnName}}', BIGINT, nullable={{nullable}}),
        {{end for}}
        
        # Standard Audit Columns (Rule #7)
        sa.Column('CreatedDate', DATETIME2, nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', BIGINT, nullable=True),
        sa.Column('LastUpdated', DATETIME2, nullable=True),
        sa.Column('UpdatedBy', BIGINT, nullable=True),
        
        # Soft Delete Columns (Rule #8)
        sa.Column('IsDeleted', BIT, nullable=False, server_default='0'),
        sa.Column('DeletedDate', DATETIME2, nullable=True),
        sa.Column('DeletedBy', BIGINT, nullable=True),
        
        # Primary Key Constraint (Rule #9)
        sa.PrimaryKeyConstraint('{{TableName}}ID', name='PK_{{TableName}}'),
        
        # Foreign Key Constraints
        {{for each FK}}
        sa.ForeignKeyConstraint(
            ['{{FKColumnName}}'], 
            ['{{ReferencedTable}}.{{ReferencedColumn}}'],
            name='FK_{{TableName}}_{{ReferencedTable}}_{{FKColumnName}}'
        ),
        {{end for}}
        
        # Indexes
        {{for each index}}
        sa.Index('IX_{{TableName}}_{{ColumnName}}', '{{ColumnName}}'),
        {{end for}}
    )


def downgrade():
    """Drop {{TableName}} table"""
    op.drop_table('{{TableName}}')
```

**Display generated migration:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Behold! A migration crafted with care, following every sacred standard..."

[Display generated migration code]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**This migration follows ALL of Anthony's standards:**
✅ Rule #1: NVARCHAR for text (Unicode support)
✅ Rule #2: Primary key named {{TableName}}ID
✅ Rule #3: Foreign keys named [ReferencedTable]ID
✅ Rule #4: Boolean fields with Is/Has prefix
✅ Rule #5: PascalCase for all names
✅ Rule #6: UTC timestamps with DATETIME2
✅ Rule #7: All audit columns included
✅ Rule #8: Soft delete support
✅ Rule #9: Constraints properly named

**Save this migration?**
1. Yes - Save to database/migrations/versions/{{revision_id}}_create_{{table_name_lower}}_table.py
2. Copy to clipboard
3. Show me again
```

**If user says yes:**
- Save to migrations folder
- Display: "Migration saved! Apply with: `alembic upgrade head`"
- Offer: "Would you like me to validate this migration to confirm? (Just to be sure!)"

