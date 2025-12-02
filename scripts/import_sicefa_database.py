#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_sicefa_database.py
- Importa el archivo SQL de SICEFA a MySQL
"""

import os
import sys
import subprocess

def import_sql_file():
    """Importa el archivo SQL usando Python"""
    sql_file = "sicefa_database.sql"
    
    if not os.path.exists(sql_file):
        print(f"❌ Error: No se encontró el archivo {sql_file}")
        return False
    
    print(f"📥 Importando archivo SQL: {sql_file}")
    print("=" * 60)
    
    try:
        import mysql.connector as mysql
        
        # Leer el archivo SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir en sentencias SQL individuales
        statements = sql_content.split(';')
        
        # Conectar a MySQL
        connection = mysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        cursor = connection.cursor()
        
        executed_count = 0
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('/*!') and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    executed_count += 1
                except Exception as e:
                    # Ignorar errores de declaraciones condicionales de MySQL
                    if 'UTF' not in str(e) and 'SQL_MODE' not in str(e):
                        print(f"⚠️  {str(e)[:100]}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"✅ Base de datos importada exitosamente ({executed_count} sentencias ejecutadas)")
        return True
            
    except Exception as e:
        print(f"❌ Error importando base de datos: {e}")
        return False

def verify_database():
    """Verifica que la base de datos se importó correctamente"""
    try:
        import mysql.connector as mysql
        
        print("\n🔍 Verificando base de datos SICEFA...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Contar tablas
        cursor.execute("SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = 'sicefa'")
        table_count = cursor.fetchone()['count']
        
        # Contar registros en tablas principales
        tables_info = {}
        for table in ['people', 'apprentices', 'courses', 'staff', 'audits']:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table} WHERE deleted_at IS NULL")
                count = cursor.fetchone()['count']
                tables_info[table] = count
            except:
                tables_info[table] = 0
        
        cursor.close()
        connection.close()
        
        print(f"✅ Base de datos SICEFA verificada")
        print(f"   Total de tablas: {table_count}")
        print(f"\n📊 Registros principales:")
        for table, count in tables_info.items():
            print(f"   - {table}: {count} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    print("=" * 60)
    print("📥 IMPORTADOR DE BASE DE DATOS SICEFA")
    print("=" * 60)
    
    if not import_sql_file():
        return False
    
    if not verify_database():
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODO COMPLETADO")
    print("=" * 60)
    print("\n🚀 Puedes ejecutar la aplicación con:")
    print("   python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
