"""
Get Database Schema from SQL Server
Query actual database to see what tables exist and their structure
"""
import sys
import os

# Add backend to path so we can import database connection
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text, inspect
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

def get_table_columns(table_name):
    """Get all columns for a specific table"""
    query = text("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        return result.fetchall()

def get_primary_keys(table_name):
    """Get primary key columns for a table"""
    query = text("""
        SELECT 
            COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        return [row[0] for row in result.fetchall()]

def get_foreign_keys(table_name):
    """Get foreign key relationships for a table"""
    query = text("""
        SELECT 
            fk.name AS FK_NAME,
            c.name AS COLUMN_NAME,
            rt.name AS REFERENCED_TABLE,
            rc.name AS REFERENCED_COLUMN
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.tables t ON fkc.parent_object_id = t.object_id
        INNER JOIN sys.columns c ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id
        INNER JOIN sys.tables rt ON fkc.referenced_object_id = rt.object_id
        INNER JOIN sys.columns rc ON fkc.referenced_object_id = rc.object_id AND fkc.referenced_column_id = rc.column_id
        WHERE t.name = :table_name
        ORDER BY fk.name
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        return result.fetchall()

def main():
    print("=" * 80)
    print("ACTUAL DATABASE SCHEMA - EventLeadPlatform")
    print("=" * 80)
    print()
    
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[OK] Database connection successful")
        print()
        
        # Get all tables
        tables = get_all_tables()
        print(f"TOTAL TABLES FOUND: {len(tables)}")
        print()
        
        # Print each table
        for idx, (schema, table_name, table_type) in enumerate(tables, 1):
            print("-" * 80)
            print(f"TABLE {idx}: [{schema}].[{table_name}]")
            print("-" * 80)
            
            # Get primary keys
            pks = get_primary_keys(table_name)
            if pks:
                print(f"PRIMARY KEY: {', '.join(pks)}")
            else:
                print("[!] NO PRIMARY KEY")
            
            # Get columns
            columns = get_table_columns(table_name)
            print(f"\nCOLUMNS ({len(columns)}):")
            for col_name, data_type, max_length, is_nullable, default_value in columns:
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                length_str = f"({max_length})" if max_length and data_type in ['nvarchar', 'varchar', 'char', 'nchar'] else ""
                pk_marker = " [PK]" if col_name in pks else ""
                print(f"  - {col_name}: {data_type.upper()}{length_str} {nullable}{pk_marker}")
            
            # Get foreign keys
            fks = get_foreign_keys(table_name)
            if fks:
                print(f"\nFOREIGN KEYS ({len(fks)}):")
                for fk_name, col_name, ref_table, ref_col in fks:
                    print(f"  - {col_name} -> [{ref_table}].[{ref_col}]")
            
            print()
        
        print("=" * 80)
        print(f"[OK] SCHEMA EXPORT COMPLETE - {len(tables)} tables found")
        print("=" * 80)
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

