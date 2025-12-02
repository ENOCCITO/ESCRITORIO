#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_test_data.py
- Script para insertar datos de prueba en la base de datos SICEFA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_test_data():
    """Inserta datos de prueba en la base de datos SICEFA"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            
            print("🔄 Insertando datos de prueba en SICEFA...\n")
            
            # 1. Insertar EPS (Entidades Prestadoras de Salud)
            print("📋 Insertando EPS...")
            eps_data = [
                ('EPS SANITAS', 'Sanitas'),
                ('EPS AXA COLPATRIA', 'AXA Colpatria'),
                ('EPS SURA', 'SURA'),
                ('COOMEVA', 'COOMEVA'),
                ('EPS FAMISANAR', 'Famisanar'),
            ]
            
            for nombre, sigla in eps_data:
                try:
                    cur.execute("""
                        INSERT INTO e_p_s (name, deleted_at)
                        VALUES (%s, NULL)
                    """, (nombre,))
                except Exception as e:
                    print(f"   Info: {nombre} - {e}")
            cnx.commit()
            print(f"   ✅ EPS insertadas")
            
            # 2. Crear un grupo poblacional por defecto
            print("📋 Configurando grupo poblacional...")
            try:
                cur.execute("INSERT IGNORE INTO population_groups (name, description) VALUES ('General', 'Población general')")
                cnx.commit()
            except:
                pass
            
            # Obtener el ID
            cur.execute("SELECT id FROM population_groups LIMIT 1")
            pop_row = cur.fetchone()
            pop_id = pop_row['id'] if pop_row else 1
            print(f"   ✅ Grupo poblacional listo (ID: {pop_id})")
            
            # 3. Crear una entidad de pensión por defecto
            print("📋 Configurando entidad de pensión...")
            try:
                cur.execute("INSERT IGNORE INTO pension_entities (name, description) VALUES ('COLPENSIONES', 'Colpensiones')")
                cnx.commit()
            except:
                pass
            
            # Obtener el ID
            cur.execute("SELECT id FROM pension_entities LIMIT 1")
            pension_row = cur.fetchone()
            pension_id = pension_row['id'] if pension_row else 1
            print(f"   ✅ Entidad de pensión lista (ID: {pension_id})")
            
            # 4. Obtener primer EPS ID
            cur.execute("SELECT id FROM e_p_s LIMIT 1")
            eps_row = cur.fetchone()
            eps_id = eps_row['id'] if eps_row else 1
            
            # 5. Insertar Personas de prueba
            print("📋 Insertando personas...")
            
            personal_data = [
                ('Juan', 'García', 'Pérez', 1234567890),
                ('María', 'Rodríguez', 'López', 987654321),
                ('Carlos', 'Martínez', 'González', 1122334455),
                ('Ana', 'Flores', 'Sánchez', 5566778899),
                ('Pedro', 'Cruz', 'Ramírez', 9988776655),
                ('Laura', 'Vega', 'Díaz', 4455667788),
            ]
            
            inserted_count = 0
            for first_name, first_last_name, second_last_name, document_number in personal_data:
                try:
                    cur.execute("""
                        INSERT INTO people 
                        (first_name, first_last_name, second_last_name, document_number,
                         eps_id, pension_entity_id, population_group_id, deleted_at, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NOW(), NOW())
                    """, (first_name, first_last_name, second_last_name, document_number, eps_id, pension_id, pop_id))
                    cnx.commit()
                    inserted_count += 1
                    print(f"   ✅ {first_name} {first_last_name} insertado")
                except Exception as e:
                    print(f"   ⚠️  Error insertando {first_name}: {e}")
                    cnx.rollback()
            
            print(f"\n✅ {inserted_count} personas insertadas correctamente")
            
            # 5. Mostrar resumen
            print("\n📊 RESUMEN DE DATOS EN LA BASE DE DATOS:\n")
            
            try:
                cur.execute("SELECT COUNT(*) as count FROM e_p_s")
                eps_count = cur.fetchone()['count']
                print(f"   👥 EPS: {eps_count}")
            except:
                print(f"   👥 EPS: error al contar")
            
            try:
                cur.execute("SELECT COUNT(*) as count FROM people WHERE deleted_at IS NULL")
                people_count = cur.fetchone()['count']
                print(f"   👤 Personas activas: {people_count}")
            except:
                print(f"   👤 Personas activas: error al contar")
            
            try:
                cur.execute("SELECT COUNT(*) as count FROM ambientes WHERE activo = 1")
                ambientes_count = cur.fetchone()['count']
                print(f"   🏢 Ambientes activos: {ambientes_count}")
            except:
                print(f"   🏢 Ambientes activos: error al contar")
            
            print("\n✅ ¡Datos de prueba insertados correctamente!")
            
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_test_data()
