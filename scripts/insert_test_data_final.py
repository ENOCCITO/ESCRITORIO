#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_test_data_final.py
Script para insertar datos de prueba en SICEFA usando solo las tablas que existen
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def insert_test_data():
    """Inserta datos de prueba en las tablas que existen"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Insertando datos de prueba en SICEFA...\n")
            
            # Obtener IDs válidos de EPS
            cur.execute("SELECT id FROM e_p_s LIMIT 1")
            eps_id_result = cur.fetchone()
            eps_id = eps_id_result[0] if eps_id_result else 1
            
            try:
                cur.execute("SELECT id FROM population_groups LIMIT 1")
                pop_id_result = cur.fetchone()
                pop_id = pop_id_result[0] if pop_id_result else 1
            except:
                pop_id = 1
            
            try:
                cur.execute("SELECT id FROM pension_entities LIMIT 1")
                pens_id_result = cur.fetchone()
                pens_id = pens_id_result[0] if pens_id_result else 1
            except:
                pens_id = 1
            
            # ===== 1. INSERTAR PERSONAS =====
            print("📝 1. Insertando personas...")
            people_data = [
                ('Juan', 'García', 'López', 'Cédula de ciudadanía', 1234567890),
                ('María', 'Rodríguez', 'Martínez', 'Cédula de ciudadanía', 1234567891),
                ('Carlos', 'López', 'Pérez', 'Cédula de ciudadanía', 1234567892),
                ('Ana', 'Flores', 'García', 'Cédula de ciudadanía', 1234567893),
                ('Pedro', 'Cruz', 'Ruiz', 'Cédula de ciudadanía', 1234567894),
                ('Laura', 'Vega', 'Sánchez', 'Cédula de ciudadanía', 1234567895),
            ]
            
            people_inserted = []
            for first_name, first_last, second_last, doc_type, doc_number in people_data:
                try:
                    cur.execute("""
                        INSERT INTO people (first_name, first_last_name, second_last_name, 
                                          document_type, document_number, personal_email, telephone1, 
                                          date_of_birth, deleted_at, created_at, updated_at,
                                          eps_id, population_group_id, pension_entity_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, NOW(), NOW(), %s, %s, %s)
                    """, (first_name, first_last, second_last, doc_type, doc_number, 
                          f"{first_name.lower()}@sena.edu.co", 3001234567, "1990-01-15",
                          eps_id, pop_id, pens_id))
                    cnx.commit()
                    people_inserted.append((first_name, first_last))
                    print(f"   ✅ Persona: {first_name} {first_last} {second_last}")
                except Exception as e:
                    if "Duplicate" in str(e):
                        print(f"   ℹ️  Persona {first_name} {first_last} ya existe")
                        people_inserted.append((first_name, first_last))
                    else:
                        print(f"   ⚠️  Error: {e}")
            
            # ===== 2. INSERTAR STAFF (INSTRUCTORES) =====
            print("\n📝 2. Insertando personal (instructores)...")
            cur.execute("SELECT id FROM people WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 2")
            instructor_people = cur.fetchall()
            
            staff_inserted = []
            if instructor_people:
                for person_id in instructor_people:
                    try:
                        cur.execute("""
                            INSERT INTO staff (person_id, role, department, start_date, end_date, 
                                             state, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, %s, NOW(), NULL, 'Activo', NULL, NOW(), NOW())
                        """, (person_id[0], 'INSTRUCTOR', 'Formación'))
                        cnx.commit()
                        staff_inserted.append(person_id[0])
                        print(f"   ✅ Instructor agregado (Person ID: {person_id[0]})")
                    except Exception as e:
                        if "Duplicate" in str(e):
                            print(f"   ℹ️  Staff para persona {person_id[0]} ya existe")
                            staff_inserted.append(person_id[0])
                        else:
                            print(f"   ⚠️  Error: {e}")
            
            # ===== RESUMEN FINAL =====
            print("\n" + "="*60)
            print("✅ DATOS INSERTADOS EN SICEFA")
            print("="*60)
            
            # Verificar datos
            cur.execute("SELECT COUNT(*) FROM people WHERE deleted_at IS NULL")
            people_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            env_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM staff WHERE deleted_at IS NULL")
            staff_count = cur.fetchone()[0]
            
            print(f"\n📊 RESUMEN DE DATOS:")
            print(f"   👥 Personas: {people_count}")
            print(f"   🏢 Ambientes: {env_count}")
            print(f"   👨‍🏫 Personal: {staff_count}")
            print(f"\n✨ Los datos están listos para ser visualizados en las interfaces")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_test_data()
