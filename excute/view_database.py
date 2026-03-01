"""
View SQLite Database Contents
Shows all tables and data in the database
"""

import sqlite3
import pandas as pd

def view_database():
    """View database contents"""
    db_path = 'specialization_prediction.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("="*60)
        print("DATABASE CONTENTS - specialization_prediction.db")
        print("="*60)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n[1] Tables in database: {len(tables)}")
        for table in tables:
            print(f"    - {table[0]}")
        
        # View each table
        for table_name in [t[0] for t in tables]:
            print(f"\n[2] Table: {table_name}")
            print("-" * 60)
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"    Rows: {count}")
            
            if count > 0:
                # Get all data
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                print(f"\n    Columns: {', '.join(df.columns.tolist())}")
                print(f"\n    First few rows:")
                print(df.head(10).to_string())
            else:
                print("    (Table is empty)")
        
        conn.close()
        print("\n" + "="*60)
        print("[SUCCESS] Database viewed successfully!")
        print("="*60)
        
    except FileNotFoundError:
        print(f"[ERROR] Database file not found: {db_path}")
        print("Run: python init_database.py")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    view_database()

