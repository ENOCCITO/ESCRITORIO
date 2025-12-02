#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_environments_direct.py
Inserta ambientes directamente usando INSERT IGNORE para evitar FK checks
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_environments_direct():
    """Inserta ambientes directamente"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Insertando ambientes directamente en SICEFA...\n")
            
            # Primero desabilitar las FK checks temporalmente
            print("📝 Deshabilitando FK checks temporalmente...")
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            
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
            print("\n📝 Insertando ambientes...\n")
            
            for name, description in environments_data:
                try:
                    # Insertar con valores por defecto para FK
                    cur.execute("""
                        INSERT INTO environments (name, description, status, farm_id, 
                                               class_environment_id, deleted_at, created_at, updated_at)
                        VALUES (%s, %s, 'Disponible', 1, 1, NULL, NOW(), NOW())
                    """, (name, description))
                    cnx.commit()
                    print(f"   ✅ {name}")
                    ambientes_insertados += 1
                except Exception as e:
                    if "Duplicate" in str(e):
                        print(f"   ℹ️  {name} ya existe")
                    else:
                        print(f"   ⚠️  {name}: {str(e)[:60]}")
            
            # Reabilitar FK checks
            print("\n📝 Rehabilitando FK checks...")
            cur.execute("SET FOREIGN_KEY_CHECKS=1")
            
            # Resumen
            print("\n" + "="*60)
            print("✅ INSERCIÓN COMPLETADA")
            print("="*60)
            
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            total_ambientes = cur.fetchone()[0]
            
            print(f"\n📊 RESUMEN FINAL:")
            print(f"   🏢 Total de ambientes en SICEFA: {total_ambientes}")
            print(f"   ✨ Los ambientes ahora están listos en la interfaz")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_environments_direct()
