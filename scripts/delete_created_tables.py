#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delete_created_tables.py
- Script para eliminar las tablas que fueron creadas (que no eran parte del flujo original)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def delete_created_tables():
    """Elimina las tablas que fueron creadas"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Eliminando tablas creadas...\n")
            
            # Tablas a eliminar (que no eran parte del flujo original)
            tables_to_delete = [
                'eps',  # Creada - ya existe e_p_s
                'pension_entities',  # Creada
                'population_groups',  # Creada
                'ambientes',  # Creada - debería usar environments
            ]
            
            for table in tables_to_delete:
                try:
                    cur.execute(f"DROP TABLE IF EXISTS `{table}`")
                    cnx.commit()
                    print(f"   ✅ Tabla '{table}' eliminada")
                except Exception as e:
                    print(f"   ⚠️  Error eliminando '{table}': {e}")
            
            print("\n✅ ¡Tablas eliminadas correctamente!")
            
    except Exception as e:
        print(f"❌ Error eliminando tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_created_tables()
