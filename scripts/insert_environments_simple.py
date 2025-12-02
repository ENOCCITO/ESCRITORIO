#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_environments_simple.py
Inserta ambientes en SICEFA de forma simple
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_environments():
    """Inserta ambientes de prueba"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Insertando ambientes en SICEFA...\n")
            
            # Obtener IDs válidos para las claves foráneas
            cur.execute("SELECT id FROM farms LIMIT 1")
            farm_id = cur.fetchone()
            
            cur.execute("SELECT id FROM class_environments LIMIT 1")
            class_env_id = cur.fetchone()
            
            if not farm_id or not class_env_id:
                print("   ⚠️  Faltan tablas requeridas (farms o class_environments)")
                print("   ℹ️  Intentando insertar ambientes de todas formas...\n")
                farm_id = 1  # Valor por defecto
                class_env_id = 1  # Valor por defecto
            else:
                farm_id = farm_id[0]
                class_env_id = class_env_id[0]
                print(f"   ✅ Farm ID: {farm_id}")
                print(f"   ✅ Class Environment ID: {class_env_id}\n")
            
            # Datos de ambientes a insertar
            environments_data = [
                ('Aula 101', 'Aula de capacitación general', '10.5', '5.6789', 'Disponible', 'Aula'),
                ('Aula 102', 'Aula de programación', '10.6', '5.6790', 'Disponible', 'Aula'),
                ('Aula 103', 'Aula de bases de datos', '10.7', '5.6791', 'Disponible', 'Aula'),
                ('Aula 201', 'Aula de desarrollo web', '10.8', '5.6792', 'Disponible', 'Aula'),
                ('Aula 202', 'Aula de diseño gráfico', '10.9', '5.6793', 'Disponible', 'Aula'),
                ('Laboratorio 101', 'Laboratorio de hardware', '11.0', '5.6794', 'Disponible', 'Laboratorio'),
                ('Laboratorio 201', 'Laboratorio de redes', '11.1', '5.6795', 'Disponible', 'Laboratorio'),
                ('Taller 101', 'Taller de soldadura', '11.2', '5.6796', 'Disponible', 'Taller'),
                ('Biblioteca', 'Centro de recursos de aprendizaje', '11.3', '5.6797', 'Disponible', 'Biblioteca'),
                ('Auditorio Principal', 'Auditorio para eventos', '11.4', '5.6798', 'Disponible', 'Auditorio'),
                ('Cafetería', 'Área de descanso y alimentación', '11.5', '5.6799', 'Disponible', 'Cafetería'),
                ('Oficina Administrativa', 'Oficina de administración', '11.6', '5.6800', 'Disponible', 'Oficina'),
            ]
            
            ambientes_insertados = 0
            for name, description, length, latitude, status, type_env in environments_data:
                try:
                    cur.execute("""
                        INSERT INTO environments (name, description, length, latitude, 
                                               farm_id, class_environment_id, status, type_environment,
                                               deleted_at, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, NOW(), NOW())
                    """, (name, description, length, latitude, farm_id, class_env_id, status, type_env))
                    cnx.commit()
                    print(f"   ✅ Ambiente: {name}")
                    ambientes_insertados += 1
                except Exception as e:
                    if "Duplicate" in str(e):
                        print(f"   ℹ️  Ambiente {name} ya existe")
                    else:
                        print(f"   ⚠️  Error: {str(e)[:80]}...")
            
            # Resumen
            print("\n" + "="*60)
            print("✅ AMBIENTES INSERTADOS")
            print("="*60)
            
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            total_ambientes = cur.fetchone()[0]
            
            print(f"\n📊 Total de ambientes en SICEFA: {total_ambientes}")
            print(f"   Ambientes insertados: {ambientes_insertados}")
            print("\n✨ Los datos están listos para ser visualizados en las interfaces")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_environments()
