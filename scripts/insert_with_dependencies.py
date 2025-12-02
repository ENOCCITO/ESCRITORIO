#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_with_dependencies.py
Inserta datos en el orden correcto respetando las FK
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_with_dependencies():
    """Inserta datos en el orden correcto"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Insertando datos con dependencias en SICEFA...\n")
            
            # ===== 1. CREAR FARM =====
            print("📝 Creando farm...")
            try:
                # Obtener una persona existente
                cur.execute("SELECT id FROM people LIMIT 1")
                person_result = cur.fetchone()
                if not person_result:
                    print("   ❌ No hay personas en la base de datos")
                    return
                
                person_id = person_result[0]
                
                # Intentar crear farm
                cur.execute("""
                    INSERT INTO farms (name, description, area, person_id, deleted_at, created_at, updated_at)
                    VALUES ('SENA Centro', 'Centro de formación SENA', '5000.50', %s, NULL, NOW(), NOW())
                """, (person_id,))
                cnx.commit()
                farm_id = cur.lastrowid
                print(f"   ✅ Farm creada con ID: {farm_id}\n")
            except Exception as e:
                if "Duplicate" in str(e):
                    # Usar la existente
                    cur.execute("SELECT id FROM farms LIMIT 1")
                    farm_id = cur.fetchone()[0]
                    print(f"   ℹ️  Farm ya existe (ID: {farm_id})\n")
                else:
                    print(f"   ❌ Error: {e}\n")
                    return
            
            # ===== 2. CREAR CLASS_ENVIRONMENT =====
            print("📝 Creando class_environment...")
            try:
                cur.execute("""
                    INSERT INTO class_environments (name, deleted_at, created_at, updated_at)
                    VALUES ('Clase Tipo', NULL, NOW(), NOW())
                """)
                cnx.commit()
                class_env_id = cur.lastrowid
                print(f"   ✅ Class Environment creada con ID: {class_env_id}\n")
            except Exception as e:
                if "Duplicate" in str(e):
                    # Usar la existente
                    cur.execute("SELECT id FROM class_environments LIMIT 1")
                    result = cur.fetchone()
                    if result:
                        class_env_id = result[0]
                        print(f"   ℹ️  Class Environment ya existe (ID: {class_env_id})\n")
                    else:
                        print(f"   ❌ No se puede crear class_environment: {e}\n")
                        return
                else:
                    print(f"   ❌ Error: {e}\n")
                    return
            
            # ===== 3. INSERTAR AMBIENTES =====
            print("📝 Insertando ambientes...")
            
            environments_data = [
                ('Aula 101', 'Aula de capacitación general'),
                ('Aula 102', 'Aula de programación'),
                ('Aula 103', 'Aula de bases de datos'),
                ('Aula 201', 'Aula de desarrollo web'),
                ('Aula 202', 'Aula de diseño gráfico'),
                ('Laboratorio 101', 'Laboratorio de hardware'),
                ('Laboratorio 201', 'Laboratorio de redes'),
                ('Taller 101', 'Taller de soldadura'),
                ('Biblioteca', 'Centro de recursos de aprendizaje'),
                ('Auditorio Principal', 'Auditorio para eventos'),
                ('Cafetería', 'Área de descanso y alimentación'),
                ('Oficina Administrativa', 'Oficina de administración'),
            ]
            
            ambientes_insertados = 0
            for name, description in environments_data:
                try:
                    cur.execute("""
                        INSERT INTO environments (name, description, status, farm_id, 
                                               class_environment_id, deleted_at, created_at, updated_at)
                        VALUES (%s, %s, 'Disponible', %s, %s, NULL, NOW(), NOW())
                    """, (name, description, farm_id, class_env_id))
                    cnx.commit()
                    print(f"   ✅ {name}")
                    ambientes_insertados += 1
                except Exception as e:
                    if "Duplicate" in str(e):
                        print(f"   ℹ️  {name} ya existe")
                    else:
                        print(f"   ⚠️  {name}: {str(e)[:60]}")
            
            # ===== RESUMEN =====
            print("\n" + "="*60)
            print("✅ INSERCIÓN COMPLETADA")
            print("="*60)
            
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            total_ambientes = cur.fetchone()[0]
            
            print(f"\n📊 RESUMEN FINAL:")
            print(f"   🏢 Total de ambientes en SICEFA: {total_ambientes}")
            print(f"   ✨ Los ambientes están listos para visualizar en las interfaces")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_with_dependencies()
