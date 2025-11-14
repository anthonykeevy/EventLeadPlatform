"""
Get Database Schema from SQL Server
Query actual database to see what tables exist and their structure
"""
import sys
import os
import argparse
from datetime import datetime
from collections import defaultdict

# Load environment variables from .env file before importing database module
try:
    from dotenv import load_dotenv
    # Try loading .env from multiple locations (matching backend behavior)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    backend_dir = os.path.join(project_root, 'backend')
    
    # Try backend/.env first (where backend typically loads from)
    env_file = os.path.join(backend_dir, '.env')
    if not os.path.exists(env_file):
        # Try root/.env
        env_file = os.path.join(project_root, '.env')
    if not os.path.exists(env_file):
        # Try root/.env.local
        env_file = os.path.join(project_root, '.env.local')
    if not os.path.exists(env_file):
        # Try backend/.env.local
        env_file = os.path.join(backend_dir, '.env.local')
    
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"[INFO] Loaded environment variables from: {env_file}")
    else:
        # Try load_dotenv() without path (uses current working directory)
        load_dotenv()
        print(f"[INFO] Attempted to load .env from current working directory")
        if not os.getenv('DATABASE_URL'):
            print(f"[WARNING] DATABASE_URL not found. Checked:")
            print(f"  - {os.path.join(backend_dir, '.env')}")
            print(f"  - {os.path.join(project_root, '.env')}")
            print(f"  - {os.path.join(project_root, '.env.local')}")
            print(f"  - {os.path.join(backend_dir, '.env.local')}")
            print(f"  - Current working directory")
except ImportError:
    print("[WARNING] python-dotenv not installed. Install with: pip install python-dotenv")
    print("[WARNING] Using system environment variables only.")

# Add backend to path so we can import database connection
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text
from common.database import engine

def get_all_tables():
    """Get all tables in the database"""
    query = text("""
        SELECT 
            TABLE_SCHEMA,
            TABLE_NAME,
            TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()

def get_table_columns(schema_name, table_name):
    """Get all columns for a specific table"""
    query = text("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = :schema_name
        AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"schema_name": schema_name, "table_name": table_name})
        return result.fetchall()

def get_primary_keys(schema_name, table_name):
    """Get primary key columns for a table"""
    query = text("""
        SELECT 
            COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        AND TABLE_SCHEMA = :schema_name
        AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"schema_name": schema_name, "table_name": table_name})
        return [row[0] for row in result.fetchall()]

def get_foreign_keys(schema_name, table_name):
    """Get foreign key relationships for a table"""
    query = text("""
        SELECT 
            fk.name AS FK_NAME,
            c.name AS COLUMN_NAME,
            rs.name AS REFERENCED_SCHEMA,
            rt.name AS REFERENCED_TABLE,
            rc.name AS REFERENCED_COLUMN
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.tables t ON fkc.parent_object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.columns c ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id
        INNER JOIN sys.tables rt ON fkc.referenced_object_id = rt.object_id
        INNER JOIN sys.schemas rs ON rt.schema_id = rs.schema_id
        INNER JOIN sys.columns rc ON fkc.referenced_object_id = rc.object_id AND fkc.referenced_column_id = rc.column_id
        WHERE s.name = :schema_name
        AND t.name = :table_name
        ORDER BY fk.name
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"schema_name": schema_name, "table_name": table_name})
        return result.fetchall()

def get_table_domain(table_name):
    """Map table name to domain for grouping"""
    table_lower = table_name.lower()
    
    # User Domain
    if table_lower.startswith('user') or table_lower in ['userinvitation', 'useremailverificationtoken', 
                                                          'userpasswordresettoken', 'userrefreshtoken', 
                                                          'usercompany', 'userindustry']:
        return 'User Domain'
    
    # Company Domain
    if table_lower.startswith('company') or table_lower in ['companyrelationship', 'companyswitchrequest']:
        return 'Company Domain'
    
    # Event Domain
    if table_lower.startswith('event'):
        return 'Event Domain'
    
    # Form Domain
    if table_lower.startswith('form'):
        return 'Form Domain'
    
    # Reference Domain (ref schema tables)
    if table_lower in ['country', 'language', 'industry', 'userstatus', 'userinvitationstatus', 
                        'userrole', 'usercompanyrole', 'usercompanystatus', 'settingcategory', 
                        'settingtype', 'ruletype', 'customertier', 'joinedvia', 'themepreference', 
                        'layoutdensity', 'fontsize', 'eventtype', 'eventstatus', 'recurrencepattern',
                        'companyrelationshiptype', 'companyswitchrequeststatus', 'companyswitchrequesttype',
                        'formstatus', 'formapprovalstatus', 'formaccesscontrolaccesstype',
                        'publicreviewstatus']:
        return 'Reference'
    
    # Audit Domain
    if table_lower.startswith('audit') or table_lower in ['activitylog', 'approvalaudittrail']:
        return 'Audit'
    
    # Log Domain
    if table_lower in ['apirequest', 'applicationerror', 'authevent', 'emaildelivery', 
                        'integrationevent', 'performancemetric', 'useraction']:
        return 'Log'
    
    # Config Domain
    if table_lower in ['appsetting', 'validationrule', 'companyvalidationrule']:
        return 'Config'
    
    # Cache Domain
    if table_lower in ['abrsearch']:
        return 'Cache'
    
    # System tables
    if table_lower in ['alembic_version']:
        return 'System'
    
    # Default to schema-based domain
    return 'Other'

def generate_markdown_schema(tables, output_path):
    """Generate Markdown-formatted schema export with domain grouping"""
    # Group tables by domain
    tables_by_domain = defaultdict(list)
    for schema, table_name, table_type in tables:
        domain = get_table_domain(table_name)
        tables_by_domain[domain].append((schema, table_name, table_type))
    
    # Sort tables within each domain by name
    for domain in tables_by_domain:
        tables_by_domain[domain].sort(key=lambda x: x[1])  # Sort by table name
    
    # Domain display order
    domain_order = ['User Domain', 'Company Domain', 'Event Domain', 'Form Domain', 
                     'Reference', 'Config', 'Audit', 'Log', 'Cache', 'System', 'Other']
    
    # Generate Markdown content
    lines = []
    lines.append("# Database Schema - EventLeadPlatform")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Total Tables:** {len(tables)}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("This document provides a complete schema reference for the EventLeadPlatform database. Tables are grouped by **domain** (User, Company, Event, Form, etc.) rather than schema. Each table name includes its schema prefix (e.g., `dbo.User`, `ref.Country`) for clarity.")
    lines.append("")
    lines.append("**Notation:**")
    lines.append("- `PK` = Primary Key column")
    lines.append("- `FK→Table` = Foreign Key to another table (table name shown; schema prefix included if different schema)")
    lines.append("- `FK→dbo.User` = Foreign Key to dbo.User (different schema)")
    lines.append("- `FK→User` = Foreign Key to User table in same schema")
    lines.append("- Empty cells in Default column = no default value")
    lines.append("")
    lines.append("**Schema Organization:**")
    lines.append("- `dbo` = Core business entities (User, Company, Event, Form)")
    lines.append("- `ref` = Reference/lookup tables (Country, UserStatus, EventType, etc.)")
    lines.append("- `config` = Configuration tables (AppSetting, ValidationRule)")
    lines.append("- `audit` = Audit trail tables (compliance tracking)")
    lines.append("- `log` = Technical logging tables (API requests, errors, etc.)")
    lines.append("- `cache` = Cache tables (ABR search results)")
    lines.append("")
    
    # Process each domain
    for domain in domain_order:
        if domain not in tables_by_domain:
            continue
        
        domain_tables = tables_by_domain[domain]
        lines.append(f"## {domain}")
        lines.append("")
        
        # Process each table in the domain
        for schema, table_name, table_type in domain_tables:
            # Table name with schema prefix
            full_table_name = f"{schema}.{table_name}"
            lines.append(f"### Table: {full_table_name}")
            lines.append("")
            
            # Get primary keys
            pks = get_primary_keys(schema, table_name)
            
            # Get columns
            columns = get_table_columns(schema, table_name)
            
            # Get foreign keys - create a mapping by column name with shortened references
            fks = get_foreign_keys(schema, table_name)
            fk_map = {}
            for fk_name, col_name, ref_schema, ref_table, ref_col in fks:
                # Shorten FK reference: use just table name if same schema, otherwise include schema
                if ref_schema == schema:
                    fk_map[col_name] = ref_table
                else:
                    fk_map[col_name] = f"{ref_schema}.{ref_table}"
            
            # Create Markdown table
            lines.append(f"**Columns ({len(columns)}):**")
            lines.append("")
            lines.append("| Column Name | Data Type | Nullable | Default | Notes |")
            lines.append("|------------|-----------|----------|---------|-------|")
            
            for col_name, data_type, max_length, is_nullable, default_value in columns:
                # Format data type
                length_str = f"({max_length})" if max_length and data_type in ['nvarchar', 'varchar', 'char', 'nchar'] else ""
                data_type_str = f"{data_type.upper()}{length_str}"
                
                # Format nullable
                nullable_str = "YES" if is_nullable == "YES" else "NO"
                
                # Format default (only show if present)
                default_str = ""
                if default_value:
                    default_str = str(default_value)
                    # Clean up default values
                    if default_str.startswith('(getutcdate()'):
                        default_str = "getutcdate()"
                    elif default_str.startswith('(('):
                        default_str = default_str[2:-2] if default_str.endswith('))') else default_str[2:-1]
                    elif default_str.startswith('('):
                        default_str = default_str[1:-1] if default_str.endswith(')') else default_str[1:]
                    if len(default_str) > 30:
                        default_str = default_str[:27] + "..."
                
                # Format notes (combine PK and FK)
                notes_parts = []
                if col_name in pks:
                    notes_parts.append("PK")
                if col_name in fk_map:
                    notes_parts.append(f"FK→{fk_map[col_name]}")
                notes_str = ", ".join(notes_parts) if notes_parts else ""
                
                lines.append(f"| {col_name} | {data_type_str} | {nullable_str} | {default_str} | {notes_str} |")
            
            lines.append("")
            lines.append("---")
            lines.append("")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Extract database schema from SQL Server',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path for Markdown export (default: docs/database-schema.md)'
    )
    parser.add_argument(
        '--file', '-f',
        action='store_true',
        help='Enable file output (writes to docs/database-schema.md if --output not specified)'
    )
    
    args = parser.parse_args()
    
    # Determine output file
    output_file = None
    if args.file or args.output:
        if args.output:
            output_file = args.output
        else:
            # Default to docs/database-schema.md
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            output_file = os.path.join(project_root, 'docs', 'database-schema.md')
            # Ensure docs directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("=" * 80)
    print("ACTUAL DATABASE SCHEMA - EventLeadPlatform")
    print("=" * 80)
    print()
    
    try:
        # Test connection
        print("[INFO] Attempting database connection...")
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("[OK] Database connection successful")
            print()
        except Exception as conn_error:
            error_str = str(conn_error)
            if "ODBC Driver" in error_str or "IM002" in error_str:
                print("[ERROR] ODBC Driver not found or not specified correctly")
                print()
                print("Common solutions:")
                print("1. Check if ODBC Driver is installed:")
                print("   - Windows: Check 'ODBC Data Sources' in Control Panel")
                print("   - Look for 'ODBC Driver 17 for SQL Server' or 'ODBC Driver 18 for SQL Server'")
                print()
                print("2. Verify DATABASE_URL in your .env file includes the correct driver:")
                print("   Example: driver=ODBC+Driver+18+for+SQL+Server")
                print()
                print("3. Install ODBC Driver if missing:")
                print("   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
                print()
                print(f"Full error: {error_str}")
            raise conn_error
        
        # Get all tables
        tables = get_all_tables()
        print(f"TOTAL TABLES FOUND: {len(tables)}")
        print()
        
        # Generate Markdown file if requested
        if output_file:
            print(f"[INFO] Generating Markdown export to: {output_file}")
            generate_markdown_schema(tables, output_file)
            print(f"[OK] Markdown export complete: {output_file}")
            print()
        
        # Print each table (console output)
        for idx, (schema, table_name, table_type) in enumerate(tables, 1):
            print("-" * 80)
            print(f"TABLE {idx}: [{schema}].[{table_name}]")
            print("-" * 80)
            
            # Get primary keys
            pks = get_primary_keys(schema, table_name)
            if pks:
                print(f"PRIMARY KEY: {', '.join(pks)}")
            else:
                print("[!] NO PRIMARY KEY")
            
            # Get columns
            columns = get_table_columns(schema, table_name)
            print(f"\nCOLUMNS ({len(columns)}):")
            for col_name, data_type, max_length, is_nullable, default_value in columns:
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                length_str = f"({max_length})" if max_length and data_type in ['nvarchar', 'varchar', 'char', 'nchar'] else ""
                pk_marker = " [PK]" if col_name in pks else ""
                print(f"  - {col_name}: {data_type.upper()}{length_str} {nullable}{pk_marker}")
            
            # Get foreign keys
            fks = get_foreign_keys(schema, table_name)
            if fks:
                print(f"\nFOREIGN KEYS ({len(fks)}):")
                for fk_name, col_name, ref_schema, ref_table, ref_col in fks:
                    print(f"  - {col_name} -> [{ref_schema}].[{ref_table}].[{ref_col}]")
            
            print()
        
        print("=" * 80)
        print(f"[OK] SCHEMA EXPORT COMPLETE - {len(tables)} tables found")
        if output_file:
            print(f"[OK] Markdown file saved to: {output_file}")
        print("=" * 80)
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

