#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_table_structure.py
Verifica la estructura de las tablas principales de SICEFA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def check_table_structure():
    """Verifica la estructura de las tablas"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            tables = ['people', 'keys', 'environments', 'courses', 'staff', 
                     'instructor_programs', 'environment_keys', 'environments_instructor_programs']
            
            for table in tables:
                print(f"\n{'='*60}")
                print(f"TABLA: {table}")
                print('='*60)
                
                cur.execute(f"DESCRIBE {table}")
                columns = cur.fetchall()
                
                for col in columns:
                    col_name = col[0]
                    col_type = col[1]
                    nullable = col[2]
                    key = col[3]
                    default = col[4]
                    extra = col[5]
                    
                    print(f"  {col_name:30} | {col_type:20} | {nullable} | {key} | {extra}")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()
