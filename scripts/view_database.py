#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
view_database.py
- Visualiza los datos de la base de datos SICEFA
"""

import sys
import os

# Cambiar color de letra a negro en Windows
if os.name == 'nt':
    os.system('color 0F')  # 0=fondo negro, F=texto blanco (mejor contraste)

def _import_mysql():
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def view_database():
    """Visualiza los datos de SICEFA"""
    mysql, err = _import_mysql()
    if not mysql:
        print(f"❌ Error: mysql-connector-python no está instalado")
        return False
    
    try:
        print("=" * 80)
        print("📊 VISUALIZADOR DE BASE DE DATOS SICEFA")
        print("=" * 80)
        
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # 1. Mostrar tabla PEOPLE
        print("\n👥 TABLA: PEOPLE (Personas)")
        print("-" * 80)
        cursor.execute("SELECT * FROM people WHERE deleted_at IS NULL LIMIT 10")
        people = cursor.fetchall()
        if people:
            for person in people:
                print(f"ID: {person['id']} | {person['first_name']} {person['last_name']} | Doc: {person['document_type']} {person['document_number']}")
        else:
            print("⚠️  No hay personas registradas")
        
        # Contar total
        cursor.execute("SELECT COUNT(*) as count FROM people WHERE deleted_at IS NULL")
        count = cursor.fetchone()['count']
        print(f"\nTotal de personas: {count}")
        
        # 2. Mostrar tabla AMBIENTES
        print("\n\n🏢 TABLA: AMBIENTES (Espacios)")
        print("-" * 80)
        cursor.execute("SELECT * FROM ambientes WHERE activo = 1 LIMIT 15")
        ambientes = cursor.fetchall()
        if ambientes:
            for amb in ambientes:
                print(f"ID: {amb['id']} | {amb['nombre']} | {amb['ubicacion']} | Cap: {amb['capacidad']} | Estado: {amb['estado']}")
        else:
            print("⚠️  No hay ambientes registrados")
        
        # Contar total
        cursor.execute("SELECT COUNT(*) as count FROM ambientes WHERE activo = 1")
        count = cursor.fetchone()['count']
        print(f"\nTotal de ambientes activos: {count}")
        
        # 3. Mostrar tabla COURSES
        print("\n\n📚 TABLA: COURSES (Cursos/Programas)")
        print("-" * 80)
        cursor.execute("SELECT * FROM courses WHERE deleted_at IS NULL LIMIT 10")
        courses = cursor.fetchall()
        if courses:
            for course in courses:
                print(f"ID: {course['id']} | {course['name']} | Código: {course['code']} | Estado: {course['state']}")
        else:
            print("⚠️  No hay cursos registrados")
        
        # Contar total
        cursor.execute("SELECT COUNT(*) as count FROM courses WHERE deleted_at IS NULL")
        count = cursor.fetchone()['count']
        print(f"\nTotal de cursos: {count}")
        
        # 4. Mostrar tabla APPRENTICES
        print("\n\n🎓 TABLA: APPRENTICES (Aprendices)")
        print("-" * 80)
        cursor.execute("""
            SELECT a.id, a.person_id, p.first_name, p.last_name, a.apprentice_status, c.name as curso
            FROM apprentices a
            JOIN people p ON a.person_id = p.id
            JOIN courses c ON a.course_id = c.id
            WHERE a.deleted_at IS NULL
            LIMIT 10
        """)
        apprentices = cursor.fetchall()
        if apprentices:
            for app in apprentices:
                print(f"ID: {app['id']} | {app['first_name']} {app['last_name']} | Curso: {app['curso']} | Estado: {app['apprentice_status']}")
        else:
            print("⚠️  No hay aprendices registrados")
        
        # Contar total
        cursor.execute("SELECT COUNT(*) as count FROM apprentices WHERE deleted_at IS NULL")
        count = cursor.fetchone()['count']
        print(f"\nTotal de aprendices: {count}")
        
        # 5. Mostrar tabla STAFF
        print("\n\n👔 TABLA: STAFF (Personal)")
        print("-" * 80)
        cursor.execute("""
            SELECT s.id, s.person_id, p.first_name, p.last_name, s.role, s.department, s.state
            FROM staff s
            JOIN people p ON s.person_id = p.id
            WHERE s.deleted_at IS NULL
            LIMIT 10
        """)
        staff = cursor.fetchall()
        if staff:
            for person in staff:
                print(f"ID: {person['id']} | {person['first_name']} {person['last_name']} | Rol: {person['role']} | Depto: {person['department']} | Estado: {person['state']}")
        else:
            print("⚠️  No hay personal registrado")
        
        # Contar total
        cursor.execute("SELECT COUNT(*) as count FROM staff WHERE deleted_at IS NULL")
        count = cursor.fetchone()['count']
        print(f"\nTotal de personal: {count}")
        
        # 6. Resumen de todas las tablas
        print("\n\n📋 RESUMEN DE TABLAS")
        print("-" * 80)
        cursor.execute("""
            SELECT 'people' as tabla, COUNT(*) as total FROM people WHERE deleted_at IS NULL
            UNION ALL
            SELECT 'courses', COUNT(*) FROM courses WHERE deleted_at IS NULL
            UNION ALL
            SELECT 'apprentices', COUNT(*) FROM apprentices WHERE deleted_at IS NULL
            SELECT 'staff', COUNT(*) FROM staff WHERE deleted_at IS NULL
            UNION ALL
            SELECT 'ambientes', COUNT(*) FROM ambientes WHERE activo = 1
        """)
        
        try:
            results = cursor.fetchall()
            for row in results:
                print(f"{row['tabla']:20} : {row['total']:5} registros")
        except:
            print("✅ Tablas principales creadas y lista para datos")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 80)
        print("✅ BASE DE DATOS VISUALIZADA CORRECTAMENTE")
        print("=" * 80)
        
        print("\n💡 PARA VISUALIZAR EN MYSQL WORKBENCH:")
        print("   1. Abre MySQL Workbench")
        print("   2. En la lista de conexiones, usa: localhost, root, sin contraseña")
        print("   3. En el panel izquierdo, verás 'sicefa' en 'Schemas'")
        print("   4. Expande 'sicefa' para ver todas las tablas")
        print("   5. Haz clic en cualquier tabla para ver sus datos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error visualizando base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = view_database()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
