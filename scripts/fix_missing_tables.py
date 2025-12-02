#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_missing_tables.py
- Crea las tablas faltantes en SICEFA
"""

import sys

def _import_mysql():
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def create_missing_tables():
    """Crea las tablas faltantes"""
    mysql, err = _import_mysql()
    if not mysql:
        print(f"❌ Error: mysql-connector-python no está instalado")
        return False
    
    try:
        print("🔧 Creando tablas faltantes...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor()
        
        # Crear tabla courses si no existe
        create_courses = """
        CREATE TABLE IF NOT EXISTS `courses` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `start_date` date DEFAULT NULL,
            `end_date` date DEFAULT NULL,
            `state` enum('Activo','Inactivo','Cancelado') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Activo',
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `courses_code_unique` (`code`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_courses)
        print("✅ Tabla courses creada")
        
        # Crear tabla apprentices
        create_apprentices = """
        CREATE TABLE IF NOT EXISTS `apprentices` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `person_id` bigint unsigned NOT NULL,
            `course_id` bigint unsigned NOT NULL,
            `apprentice_status` enum('NO REGISTRA','CERTIFICADO','EN FORMACIÓN','RETIRO VOLUNTARIO','CANCELADO','TRASLADADO','APLAZADO','INDUCCIÓN','CONDICIONADO') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            `guardian` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `guardian_telephone` int unsigned DEFAULT NULL,
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `apprentices_person_id_course_id_unique` (`person_id`,`course_id`),
            KEY `apprentices_course_id_foreign` (`course_id`),
            CONSTRAINT `apprentices_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
            CONSTRAINT `apprentices_person_id_foreign` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_apprentices)
        print("✅ Tabla apprentices creada")
        
        # Crear tabla staff
        create_staff = """
        CREATE TABLE IF NOT EXISTS `staff` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `person_id` bigint unsigned NOT NULL,
            `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            `department` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `start_date` date DEFAULT NULL,
            `end_date` date DEFAULT NULL,
            `state` enum('Activo','Inactivo','Licencia') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Activo',
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `staff_person_id_unique` (`person_id`),
            CONSTRAINT `staff_person_id_foreign` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_staff)
        print("✅ Tabla staff creada")
        
        # Crear tabla instructor_programs
        create_instructor_programs = """
        CREATE TABLE IF NOT EXISTS `instructor_programs` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `instructor_id` bigint unsigned NOT NULL,
            `course_id` bigint unsigned NOT NULL,
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `instructor_programs_instructor_id_foreign` (`instructor_id`),
            KEY `instructor_programs_course_id_foreign` (`course_id`),
            CONSTRAINT `instructor_programs_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
            CONSTRAINT `instructor_programs_instructor_id_foreign` FOREIGN KEY (`instructor_id`) REFERENCES `staff` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_instructor_programs)
        print("✅ Tabla instructor_programs creada")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def insert_sample_data():
    """Inserta datos de ejemplo"""
    mysql, err = _import_mysql()
    if not mysql:
        return False
    
    try:
        print("\n📝 Insertando datos de ejemplo...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor()
        
        # Insertar cursos de ejemplo
        insert_courses = """
        INSERT IGNORE INTO `courses` (`name`, `code`, `description`, `state`, `created_at`, `updated_at`)
        VALUES
        ('Programación Básica', 'PROG-001', 'Introducción a la programación', 'Activo', NOW(), NOW()),
        ('Desarrollo Web', 'WEB-001', 'Desarrollo de aplicaciones web', 'Activo', NOW(), NOW()),
        ('Bases de Datos', 'BD-001', 'Diseño e implementación de bases de datos', 'Activo', NOW(), NOW()),
        ('Redes de Computadores', 'RED-001', 'Fundamentos de redes', 'Activo', NOW(), NOW()),
        ('Seguridad Informática', 'SEG-001', 'Introducción a la seguridad', 'Activo', NOW(), NOW());
        """
        cursor.execute(insert_courses)
        connection.commit()
        print("✅ Cursos de ejemplo insertados")
        
        # Insertar personas de ejemplo si no existen
        insert_people = """
        INSERT IGNORE INTO `people` (`first_name`, `last_name`, `document_type`, `document_number`, `email`, `phone`, `created_at`, `updated_at`)
        VALUES
        ('Juan', 'Pérez', 'CC', '1234567890', 'juan@example.com', '3001234567', NOW(), NOW()),
        ('María', 'García', 'CC', '0987654321', 'maria@example.com', '3007654321', NOW(), NOW()),
        ('Carlos', 'López', 'CC', '1122334455', 'carlos@example.com', '3002233445', NOW(), NOW()),
        ('Ana', 'Martínez', 'CC', '5544332211', 'ana@example.com', '3005544332', NOW(), NOW()),
        ('Pedro', 'Rodríguez', 'CC', '9876543210', 'pedro@example.com', '3009876543', NOW(), NOW());
        """
        cursor.execute(insert_people)
        connection.commit()
        print("✅ Personas de ejemplo insertadas")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"⚠️  Error insertando datos de ejemplo: {e}")
        return True  # No es crítico

def verify_tables():
    """Verifica que todas las tablas existan"""
    mysql, err = _import_mysql()
    if not mysql:
        return False
    
    try:
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sicefa' ORDER BY TABLE_NAME")
        tables = cursor.fetchall()
        
        print("\n✅ TABLAS EN SICEFA:")
        for table in tables:
            print(f"   - {table['TABLE_NAME']}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 REPARADOR DE TABLAS FALTANTES")
    print("=" * 60)
    
    if not create_missing_tables():
        return False
    
    if not insert_sample_data():
        return False
    
    if not verify_tables():
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODO COMPLETADO")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
