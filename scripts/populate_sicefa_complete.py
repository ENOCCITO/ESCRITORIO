#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
populate_sicefa_complete.py
Completa las tablas de SICEFA con datos realistas
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
                people_data = [
                    ('Juan', 'García', 'López', 'CC', '1234567890', '2020-01-15', '1985-03-20', 'O+', 'M', 15),
                    ('María', 'Rodríguez', 'Pérez', 'CC', '1234567891', '2020-01-15', '1990-06-10', 'A+', 'F', 15),
                    ('Carlos', 'López', 'García', 'CC', '1234567892', '2020-01-15', '1988-11-25', 'B+', 'M', 16),
                    ('Ana', 'Flores', 'Torres', 'CC', '1234567893', '2020-01-15', '1992-05-08', 'O+', 'F', 17),
                    ('Pedro', 'Cruz', 'Sánchez', 'CC', '1234567894', '2020-01-15', '1987-09-12', 'AB+', 'M', 15),
                    ('Laura', 'Vega', 'Martínez', 'CC', '1234567895', '2020-01-15', '1991-02-28', 'A+', 'F', 16),
                    ('Fernando', 'Díaz', 'Jiménez', 'CC', '1234567896', '2020-01-15', '1989-07-19', 'B-', 'M', 17),
                    ('Patricia', 'Morales', 'Ruiz', 'CC', '1234567897', '2020-01-15', '1993-04-14', 'O-', 'F', 15),
                    ('Roberto', 'Gutiérrez', 'Hernández', 'CC', '1234567898', '2020-01-15', '1986-12-03', 'A-', 'M', 16),
                    ('Isabel', 'Ramírez', 'Vargas', 'CC', '1234567899', '2020-01-15', '1994-08-21', 'B+', 'F', 17),
                ]
                
                for nombre, apellido1, apellido2, tipo_doc, num_doc, fecha_exp, fecha_nac, tipo_sangre, genero, eps_id in people_data:
                    try:
                        cur.execute("""
                            INSERT INTO people 
                            (first_name, first_last_name, second_last_name, document_type, document_number, 
                             date_of_issue, date_of_birth, blood_type, gender, eps_id, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NOW(), NOW())
                        """, (nombre, apellido1, apellido2, tipo_doc, num_doc, fecha_exp, fecha_nac, tipo_sangre, genero, eps_id))
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
            
            if staff_count < 5:
                print("   Insertando instructores/staff...")
                cur.execute("SELECT id FROM people LIMIT 5")
                people_ids = [row[0] for row in cur.fetchall()]
                
                for i, person_id in enumerate(people_ids[:5]):
                    try:
                        roles = ['Instructor', 'Coordinador', 'Capacitador', 'Supervisor', 'Director']
                        cur.execute("""
                            INSERT INTO staff (person_id, role, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, NULL, NOW(), NOW())
                        """, (person_id, roles[i]))
                    except Exception as e:
                        if 'Duplicate' not in str(e):
                            print(f"   Advertencia: {str(e)[:60]}")
                
                cnx.commit()
                print("   ✅ Staff insertado")
            
            # 3. Inserta cursos si es necesario
            print("📝 3. Verificando tabla 'courses'...")
            cur.execute("SELECT COUNT(*) FROM courses")
            courses_count = cur.fetchone()[0]
            print(f"   Cursos existentes: {courses_count}")
            
            if courses_count < 5:
                print("   Insertando cursos...")
                courses_data = [
                    ('Programación en Python', 'Aprenda Python desde cero', 40),
                    ('Desarrollo Web', 'HTML, CSS, JavaScript y PHP', 50),
                    ('Bases de Datos', 'SQL y diseño de BD', 35),
                    ('Sistemas Operativos', 'Windows, Linux y administración', 45),
                    ('Redes y Telecomunicaciones', 'Fundamentos de redes', 40),
                ]
                
                for nombre, descripcion, duracion_horas in courses_data:
                    try:
                        cur.execute("""
                            INSERT INTO courses (name, description, duration_hours, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, %s, NULL, NOW(), NOW())
                        """, (nombre, descripcion, duracion_horas))
                    except Exception as e:
                        if 'Duplicate' not in str(e):
                            print(f"   Advertencia: {str(e)[:60]}")
                
                cnx.commit()
                print("   ✅ Cursos insertados")
            
            # 4. Enlazar cursos con instructores
            print("📝 4. Verificando tabla 'instructor_programs'...")
            cur.execute("SELECT COUNT(*) FROM instructor_programs")
            ip_count = cur.fetchone()[0]
            print(f"   Relaciones instructor-curso existentes: {ip_count}")
            
            if ip_count < 5:
                print("   Enlazando instructores con cursos...")
                cur.execute("SELECT id FROM staff LIMIT 3")
                staff_ids = [row[0] for row in cur.fetchall()]
                cur.execute("SELECT id FROM courses LIMIT 3")
                course_ids = [row[0] for row in cur.fetchall()]
                
                for i, staff_id in enumerate(staff_ids):
                    try:
                        course_id = course_ids[i % len(course_ids)]
                        cur.execute("""
                            INSERT INTO instructor_programs (staff_id, course_id, deleted_at, created_at, updated_at)
                            VALUES (%s, %s, NULL, NOW(), NOW())
                        """, (staff_id, course_id))
                    except Exception as e:
                        if 'Duplicate' not in str(e):
                            print(f"   Advertencia: {str(e)[:60]}")
                
                cnx.commit()
                print("   ✅ Relaciones insertadas")
            
            # 5. Verificar/crear datos para environments
            print("📝 5. Verificando tabla 'environments'...")
            cur.execute("SELECT COUNT(*) FROM environments")
            env_count = cur.fetchone()[0]
            print(f"   Ambientes existentes: {env_count}")
            
            # Resumen final
            print("\n" + "="*60)
            print("✅ POPULACIÓN DE SICEFA COMPLETADA")
            print("="*60)
            print("\nResumen:")
            cur.execute("SELECT COUNT(*) FROM people WHERE deleted_at IS NULL")
            print(f"  👥 Personas: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM staff WHERE deleted_at IS NULL")
            print(f"  👔 Staff: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM courses WHERE deleted_at IS NULL")
            print(f"  📚 Cursos: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM environments WHERE deleted_at IS NULL")
            print(f"  🏢 Ambientes: {cur.fetchone()[0]}")
            cur.execute("SELECT COUNT(*) FROM `keys` WHERE status = 'Disponible'")
            print(f"  🔑 Llaves disponibles: {cur.fetchone()[0]}")
            print("="*60 + "\n")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_sicefa()
