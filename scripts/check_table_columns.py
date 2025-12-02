#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_table_columns.py
Verifica la estructura de las tablas de SICEFA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def check_columns():
    """Verifica la estructura de las tablas"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            tables = ['people', 'staff', 'courses', 'environments', 'keys']
            
            for table in tables:
                print(f"\n📋 Tabla: {table}")
                print("-" * 60)
                try:
                    cur.execute(f"DESCRIBE {table}")
                    columns = cur.fetchall()
                    for col_name, col_type, null, key, default, extra in columns:
                        print(f"  {col_name}: {col_type}")
                except Exception as e:
                    print(f"  Error: {e}")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_columns()
