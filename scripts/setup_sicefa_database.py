#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_sicefa_database.py
- Script para configurar la base de datos SICEFA
- Verifica conexión a MySQL
- Crea la base de datos si no existe
"""

import sys
import time

def _import_mysql():
    """Importa mysql.connector"""
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def test_mysql_connection():
    """Prueba la conexión básica a MySQL sin especificar base de datos"""
    mysql, err = _import_mysql()
    if not mysql:
        print(f"❌ Error: mysql-connector-python no está instalado")
        print(f"   Instálalo con: pip install mysql-connector-python")
        return False, err
    
    try:
        print("🔌 Intentando conectar a MySQL Server...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("✅ Conexión a MySQL Server establecida correctamente")
        connection.close()
        return True, None
    except Exception as e:
        print(f"❌ Error conectando a MySQL Server: {e}")
        print("\n⚠️ POSIBLES SOLUCIONES:")
        print("   1. Verifica que MySQL Server esté corriendo")
        print("   2. En Windows, abre Services (services.msc) y busca 'MySQL80'")
        print("   3. Si no está corriendo, haz clic derecho y selecciona 'Start'")
        print("   4. Si no existe el servicio, instala MySQL Server desde:")
        print("      https://dev.mysql.com/downloads/mysql/")
        return False, e

def check_database_exists():
    """Verifica si la base de datos sicefa existe"""
    mysql, err = _import_mysql()
    if not mysql:
        return False, "MySQL no disponible"
    
    try:
        connection = mysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'sicefa'")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            print("✅ Base de datos 'sicefa' ya existe")
            return True, None
        else:
            print("⚠️ Base de datos 'sicefa' NO existe")
            return False, "Database not found"
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False, e

def test_sicefa_connection():
    """Prueba la conexión a la base de datos SICEFA"""
    mysql, err = _import_mysql()
    if not mysql:
        return False, "MySQL no disponible"
    
    try:
        print("🔌 Conectando a base de datos 'sicefa'...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'sicefa'")
        table_count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        
        print(f"✅ Conexión exitosa a SICEFA ({table_count} tablas encontradas)")
        return True, table_count
    except Exception as e:
        print(f"❌ Error conectando a SICEFA: {e}")
        return False, e

def show_database_info():
    """Muestra información de la base de datos SICEFA"""
    mysql, err = _import_mysql()
    if not mysql:
        return
    
    try:
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        cursor = connection.cursor(dictionary=True)
        
        # Contar personas
        cursor.execute("SELECT COUNT(*) as count FROM people WHERE deleted_at IS NULL")
        people_count = cursor.fetchone()['count']
        
        # Contar aprendices
        cursor.execute("SELECT COUNT(*) as count FROM apprentices WHERE deleted_at IS NULL")
        apprentices_count = cursor.fetchone()['count']
        
        # Contar cursos
        cursor.execute("SELECT COUNT(*) as count FROM courses WHERE deleted_at IS NULL")
        courses_count = cursor.fetchone()['count']
        
        # Contar personal
        cursor.execute("SELECT COUNT(*) as count FROM staff WHERE deleted_at IS NULL")
        staff_count = cursor.fetchone()['count']
        
        cursor.close()
        connection.close()
        
        print("\n📊 INFORMACIÓN DE LA BASE DE DATOS SICEFA:")
        print(f"   👥 Personas: {people_count}")
        print(f"   🎓 Aprendices: {apprentices_count}")
        print(f"   📚 Cursos: {courses_count}")
        print(f"   👔 Personal: {staff_count}")
        
    except Exception as e:
        print(f"⚠️ Error obteniendo información: {e}")

def main():
    print("=" * 60)
    print("🔐 CONFIGURADOR DE BASE DE DATOS SICEFA")
    print("=" * 60)
    
    # Paso 1: Verificar conexión a MySQL
    print("\n[1/3] Verificando conexión a MySQL Server...")
    mysql_ok, mysql_err = test_mysql_connection()
    if not mysql_ok:
        print("\n❌ No se puede conectar a MySQL Server")
        return False
    
    # Paso 2: Verificar si la base de datos existe
    print("\n[2/3] Verificando base de datos 'sicefa'...")
    db_exists, _ = check_database_exists()
    if not db_exists:
        print("\n⚠️ Necesitas importar el archivo SQL de SICEFA")
        print("\n📝 PASOS PARA IMPORTAR LA BASE DE DATOS:")
        print("   1. Guarda el archivo SQL en una ubicación conocida")
        print("   2. Abre MySQL Workbench o línea de comandos")
        print("   3. En MySQL Workbench:")
        print("      - File → Open SQL Script")
        print("      - Selecciona tu archivo SQL")
        print("      - Haz clic en ejecutar")
        print("   4. O en línea de comandos:")
        print("      mysql -u root < ruta/al/archivo.sql")
        return False
    
    # Paso 3: Conectar a SICEFA
    print("\n[3/3] Conectando a base de datos SICEFA...")
    sicefa_ok, table_count = test_sicefa_connection()
    if not sicefa_ok:
        return False
    
    # Mostrar información
    show_database_info()
    
    print("\n" + "=" * 60)
    print("✅ TODO CONFIGURADO CORRECTAMENTE")
    print("=" * 60)
    print("\n🚀 Puedes ejecutar la aplicación con:")
    print("   python main.py")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
