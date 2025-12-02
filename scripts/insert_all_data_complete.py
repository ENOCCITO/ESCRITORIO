#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_all_data_complete.py
Inserta todos los datos necesarios en SICEFA de forma completa
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_all_data():
    """Inserta datos completos en SICEFA"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Insertando datos completos en SICEFA...\n")
            
            # ===== 1. VERIFICAR si ya existen ambientes =====
            print("📋 Verificando ambientes existentes...")
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            env_count = cur.fetchone()[0]
            
            if env_count > 0:
                print(f"   ✅ Ya hay {env_count} ambientes en la BD\n")
                cur.close()
                return
            
            print("   ℹ️  No hay ambientes, insertando...\n")
            
            # ===== 2. INSERTAR AMBIENTES con NULL para las FK =====
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
            
            # Intentar insertar con la estructura simplificada
            ambientes_insertados = 0
            for name, description in environments_data:
                try:
                    # Intentar insertar solo con campos obligatorios
                    cur.execute("""
                        INSERT INTO environments (name, description, status, created_at, updated_at)
                        VALUES (%s, %s, 'Disponible', NOW(), NOW())
                    """, (name, description))
                    cnx.commit()
                    print(f"   ✅ {name}")
                    ambientes_insertados += 1
                except Exception as e:
                    if "Duplicate" in str(e):
                        print(f"   ℹ️  {name} ya existe")
                    else:
                        # Si falla, intentar con todos los campos NULL donde sea posible
                        try:
                            cur.execute("""
                                INSERT INTO environments (name, description, status, type_environment,
                                                       deleted_at, created_at, updated_at)
                                VALUES (%s, %s, 'Disponible', NULL, NULL, NOW(), NOW())
                            """, (name, description))
                            cnx.commit()
                            print(f"   ✅ {name}")
                            ambientes_insertados += 1
                        except Exception as e2:
                            print(f"   ⚠️  {name}: {str(e2)[:60]}...")
            
            # Resumen
            print("\n" + "="*60)
            print("✅ INSERCIÓN COMPLETADA")
            print("="*60)
            
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            total_ambientes = cur.fetchone()[0]
            
            print(f"\n📊 RESUMEN FINAL:")
            print(f"   🏢 Ambientes en SICEFA: {total_ambientes}")
            print(f"   ✨ Los ambientes están listos para visualizar")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_all_data()
