#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reload_sample_data.py
- Recarga datos de ejemplo en SICEFA
"""

import sys

def _import_mysql():
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def reload_data():
    """Recarga datos de ejemplo"""
    mysql, err = _import_mysql()
    if not mysql:
        print(f"❌ Error: mysql-connector-python no está instalado")
        return False
    
    try:
        print("=" * 80)
        print("📝 RECARGADOR DE DATOS DE EJEMPLO")
        print("=" * 80)
        
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor()
        
        # Limpiar datos previos
        print("\n🧹 Limpiando datos previos...")
        cursor.execute("DELETE FROM people WHERE id > 4456")
        cursor.execute("DELETE FROM courses WHERE id > 41")
        cursor.execute("DELETE FROM staff")
        connection.commit()
        print("✅ Datos limpios")
        
        # Insertar personas
        print("\n👥 Insertando personas...")
        insert_people = """
        INSERT INTO `people` (`first_name`, `first_last_name`, `second_last_name`, `document_type`, `document_number`, `personal_email`, `telephone1`, `created_at`, `updated_at`)
        VALUES
        ('Juan', 'Pérez', 'García', 'CC', '1234567890', 'juan@example.com', '3001234567', NOW(), NOW()),
        ('María', 'García', 'López', 'CC', '0987654321', 'maria@example.com', '3007654321', NOW(), NOW()),
        ('Carlos', 'López', 'Martínez', 'CC', '1122334455', 'carlos@example.com', '3002233445', NOW(), NOW()),
        ('Ana', 'Martínez', 'Rodríguez', 'CC', '5544332211', 'ana@example.com', '3005544332', NOW(), NOW()),
        ('Pedro', 'Rodríguez', 'Gómez', 'CC', '9876543210', 'pedro@example.com', '3009876543', NOW(), NOW()),
        ('Laura', 'Gómez', 'Torres', 'CC', '1111111111', 'laura@example.com', '3101111111', NOW(), NOW()),
        ('Miguel', 'Sánchez', 'Herrera', 'CC', '2222222222', 'miguel@example.com', '3102222222', NOW(), NOW()),
        ('Sofía', 'Torres', 'Jiménez', 'CC', '3333333333', 'sofia@example.com', '3103333333', NOW(), NOW()),
        ('Diego', 'Rivera', 'Vargas', 'CC', '4444444444', 'diego@example.com', '3104444444', NOW(), NOW()),
        ('Valentina', 'Herrera', 'Castro', 'CC', '5555555555', 'valentina@example.com', '3105555555', NOW(), NOW());
        """
        cursor.execute(insert_people)
        connection.commit()
        print("✅ 10 personas insertadas")
        
        # Insertar cursos
        print("\n📚 Insertando cursos...")
        insert_courses = """
        INSERT INTO `courses` (`name`, `code`, `description`, `state`, `created_at`, `updated_at`)
        VALUES
        ('Programación Básica', 'PROG-001', 'Introducción a la programación en Python', 'Activo', NOW(), NOW()),
        ('Desarrollo Web', 'WEB-001', 'Desarrollo de aplicaciones web con Django', 'Activo', NOW(), NOW()),
        ('Bases de Datos', 'BD-001', 'Diseño e implementación de bases de datos MySQL', 'Activo', NOW(), NOW()),
        ('Redes de Computadores', 'RED-001', 'Fundamentos de redes y telecomunicaciones', 'Activo', NOW(), NOW()),
        ('Seguridad Informática', 'SEG-001', 'Introducción a la seguridad informática', 'Activo', NOW(), NOW()),
        ('Administración de Sistemas', 'ADM-001', 'Administración de servidores Linux', 'Activo', NOW(), NOW()),
        ('Cloud Computing', 'CLOUD-001', 'Plataformas en la nube AWS y Azure', 'Activo', NOW(), NOW()),
        ('Machine Learning', 'ML-001', 'Introducción a aprendizaje automático', 'Activo', NOW(), NOW());
        """
        cursor.execute(insert_courses)
        connection.commit()
        print("✅ 8 cursos insertados")
        
        # Insertar personal (instructores)
        print("\n👔 Insertando personal (instructores)...")
        insert_staff = """
        INSERT INTO `staff` (`person_id`, `role`, `department`, `state`, `created_at`, `updated_at`)
        SELECT id, 'INSTRUCTOR', 'Capacitación', 'Activo', NOW(), NOW()
        FROM people 
        WHERE document_number IN ('1234567890', '0987654321', '1122334455')
        """
        cursor.execute(insert_staff)
        connection.commit()
        print("✅ Personal insertado")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 80)
        print("✅ DATOS RECARGADOS CORRECTAMENTE")
        print("=" * 80)
        print("\n📊 Resumen:")
        print("   - 10 personas cargadas")
        print("   - 8 cursos cargados")
        print("   - 12 ambientes disponibles")
        print("   - 3 instructores activos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error recargando datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = reload_data()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
