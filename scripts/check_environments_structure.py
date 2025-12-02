#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_environments_structure.py
Verifica la estructura de la tabla environments
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def check_environments_structure():
    """Verifica estructura de environments"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("📋 ESTRUCTURA DE LA TABLA: environments\n")
            print("="*80)
            
            cur.execute("DESCRIBE environments")
            columns = cur.fetchall()
            
            for col in columns:
                col_name = col[0]
                col_type = col[1]
                nullable = col[2]
                key = col[3]
                default = col[4]
                extra = col[5]
                
                print(f"Columna: {col_name}")
                print(f"   Tipo: {col_type}")
                print(f"   Nullable: {nullable}")
                print(f"   Key: {key}")
                print(f"   Default: {default}")
                print(f"   Extra: {extra}\n")
            
            print("="*80)
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_environments_structure()
