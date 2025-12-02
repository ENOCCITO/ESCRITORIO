#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delete_created_tables_with_constraints.py
- Script para eliminar las tablas creadas eliminando primero las constraints
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def delete_created_tables_with_constraints():
    """Elimina las tablas que fueron creadas y sus constraints"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Eliminando tablas creadas...\n")
            
            # Primero eliminar las constraints de la tabla people
            print("📋 Eliminando constraints de la tabla 'people'...")
            try:
                cur.execute("ALTER TABLE `people` DROP FOREIGN KEY `people_pension_entity_id_foreign`")
                cnx.commit()
                print("   ✅ Constraint 'people_pension_entity_id_foreign' eliminado")
            except Exception as e:
                print(f"   ℹ️  {e}")
            
            try:
                cur.execute("ALTER TABLE `people` DROP FOREIGN KEY `people_population_group_id_foreign`")
                cnx.commit()
                print("   ✅ Constraint 'people_population_group_id_foreign' eliminado")
            except Exception as e:
                print(f"   ℹ️  {e}")
            
            # Ahora eliminar las tablas
            print("\n📋 Eliminando tablas creadas...")
            tables_to_delete = [
                'eps',
                'pension_entities',
                'population_groups',
                'ambientes',
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
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_created_tables_with_constraints()
