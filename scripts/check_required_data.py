#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_required_data.py
Verifica qué datos existen en las tablas de referencia
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def check_required_data():
    """Verifica datos requeridos"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔍 Verificando datos requeridos en SICEFA...\n")
            
            # Verificar e_p_s
            print("📋 Tabla: e_p_s")
            cur.execute("SELECT id, name FROM e_p_s LIMIT 5")
            eps_data = cur.fetchall()
            if eps_data:
                print(f"   ✅ Encontrados {cur.rowcount} registros")
                for eps_id, eps_name in eps_data:
                    print(f"      - ID: {eps_id}, Name: {eps_name}")
            else:
                print("   ❌ No hay registros en e_p_s")
            
            # Verificar population_groups
            print("\n📋 Tabla: population_groups")
            cur.execute("SELECT id, name FROM population_groups LIMIT 5")
            pop_data = cur.fetchall()
            if pop_data:
                print(f"   ✅ Encontrados registros")
                for pop_id, pop_name in pop_data:
                    print(f"      - ID: {pop_id}, Name: {pop_name}")
            else:
                print("   ❌ No hay registros en population_groups")
            
            # Verificar pension_entities
            print("\n📋 Tabla: pension_entities")
            cur.execute("SELECT id, name FROM pension_entities LIMIT 5")
            pens_data = cur.fetchall()
            if pens_data:
                print(f"   ✅ Encontrados registros")
                for pens_id, pens_name in pens_data:
                    print(f"      - ID: {pens_id}, Name: {pens_name}")
            else:
                print("   ❌ No hay registros en pension_entities")
            
            # Verificar environments
            print("\n📋 Tabla: environments")
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            env_count = cur.fetchone()[0]
            print(f"   ✅ Total ambientes: {env_count}")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_required_data()
