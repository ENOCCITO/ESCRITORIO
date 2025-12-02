#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
populate_sicefa_final.py
Completa las tablas de SICEFA con datos correctos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def populate_sicefa():
    """Completa las tablas de SICEFA con datos realistas"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Poblando SICEFA con datos realistas...\n")
            
            # 1. Insertar datos en la tabla 'people' si está vacía
            print("📝 1. Verificando tabla 'people'...")
            cur.execute("SELECT COUNT(*) FROM people")
            people_count = cur.fetchone()[0]
            print(f"   Personas existentes: {people_count}")
            
            if people_count < 20:
                print("   Insertando más personas...")
                # Usar las enumeraciones correctas del campo
                people_data = [
                    ('Juan', 'García', 'López', "Cédula de ciudadanía", 1234567890, '1985-03-20', 'O+', 'Masculino', 15),
                    ('María', 'Rodríguez', 'Pérez', "Cédula de ciudadanía", 1234567891, '1990-06-10', 'A+', 'Femenino', 15),
                    ('Carlos', 'López', 'García', "Cédula de ciudadanía", 1234567892, '1988-11-25', 'B+', 'Masculino', 16),
                    ('Ana', 'Flores', 'Torres', "Cédula de ciudadanía", 1234567893, '1992-05-08', 'O+', 'Femenino', 17),
                    ('Pedro', 'Cruz', 'Sánchez', "Cédula de ciudadanía", 1234567894, '1987-09-12', 'AB+', 'Masculino', 15),
                    ('Laura', 'Vega', 'Martínez', "Cédula de ciudadanía", 1234567895, '1991-02-28', 'A+', 'Femenino', 16),
                    ('Fernando', 'Díaz', 'Jiménez', "Cédula de ciudadanía", 1234567896, '1989-07-19', 'B-', 'Masculino', 17),
                    ('Patricia', 'Morales', 'Ruiz', "Cédula de ciudadanía", 1234567897, '1993-04-14', 'O-', 'Femenino', 15),
                    ('Roberto', 'Gutiérrez', 'Hernández', "Cédula de ciudadanía", 1234567898, '1986-12-03', 'A-', 'Masculino', 16),
                    ('Isabel', 'Ramírez', 'Vargas', "Cédula de ciudadanía", 1234567899, '1994-08-21', 'B+', 'Femenino', 17),
                ]
                
                for nombre, apellido1, apellido2, tipo_doc, num_doc, fecha_nac, tipo_sangre, genero, eps_id in people_data:
                    try:
                        cur.execute("""
                            INSERT INTO people 
                            (first_name, first_last_name, second_last_name, document_type, document_number, 
                             date_of_birth, blood_type, gender, eps_id, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NOW(), NOW())
                        """, (nombre, apellido1, apellido2, tipo_doc, num_doc, fecha_nac, tipo_sangre, genero, eps_id))
                    except Exception as e:
                        if 'Duplicate' not in str(e):
                            print(f"   Advertencia: {str(e)[:60]}")
                
                cnx.commit()
                print("   ✅ Personas insertadas")
            
            # 2. Insertar staff/instructores
            print("📝 2. Verificando tabla 'staff'...")
            cur.execute("SELECT COUNT(*) FROM staff")
            staff_count = cur.fetchone()[0]
            print(f"   Staff existente: {staff_count}")
            
            if staff_count < 10:
                print("   Insertando instructores/staff...")
                cur.execute("SELECT id FROM people WHERE deleted_at IS NULL LIMIT 10")
                people_ids = [row[0] for row in cur.fetchall()]
                
                roles = ['Instructor', 'Coordinador', 'Capacitador', 'Supervisor', 'Director', 
                         'Administrador', 'Asistente', 'Encargado', 'Técnico', 'Gestor']
                
                for i, person_id in enumerate(people_ids[:10]):
                    try:
                        cur.execute("""
                            INSERT INTO staff (person_id, role, state, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, 'Activo', NULL, NOW(), NOW())
                        """, (person_id, roles[i]))
                    except Exception as e:
                        if 'Duplicate' not in str(e):
                            print(f"   Advertencia: {str(e)[:60]}")
                
                cnx.commit()
                print("   ✅ Staff insertado")
            
            # Resumen final
            print("\n" + "="*60)
            print("✅ POPULACIÓN DE SICEFA COMPLETADA")
            print("="*60)
            print("\nResumen:")
            cur.execute("SELECT COUNT(*) FROM people WHERE deleted_at IS NULL")
            print(f"  👥 Personas: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM staff WHERE deleted_at IS NULL")
            print(f"  👔 Staff: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            print(f"  🏢 Ambientes: {cur.fetchone()[0]}")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_sicefa()
