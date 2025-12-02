#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_environments_table.py
- Añade la tabla de ambientes a SICEFA
- Inserta datos de ejemplo
"""

import sys

def _import_mysql():
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def create_environments_table():
    """Crea la tabla de ambientes en SICEFA"""
    mysql, err = _import_mysql()
    if not mysql:
        print(f"❌ Error: mysql-connector-python no está instalado")
        return False
    
    try:
        print("📁 Creando tabla de ambientes...")
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sicefa"
        )
        
        cursor = connection.cursor()
        
        # Crear tabla de ambientes
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `ambientes` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `nombre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `ubicacion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `capacidad` int DEFAULT 30,
            `piso` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `edificio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `estado` enum('Disponible','Ocupado','Mantenimiento') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Disponible',
            `activo` tinyint(1) DEFAULT 1,
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        print("✅ Tabla de ambientes creada correctamente")
        
        # Insertar datos de ejemplo
        insert_data_sql = """
        INSERT INTO `ambientes` 
        (`nombre`, `descripcion`, `ubicacion`, `capacidad`, `piso`, `edificio`, `estado`, `activo`, `created_at`, `updated_at`)
        VALUES
        ('Aula 101', 'Sala de capacitación programación básica', 'Piso 1', 30, '1', 'Edificio A', 'Disponible', 1, NOW(), NOW()),
        ('Aula 102', 'Sala de desarrollo web avanzado', 'Piso 1', 25, '1', 'Edificio A', 'Disponible', 1, NOW(), NOW()),
        ('Laboratorio 201', 'Laboratorio de práctica electrónica', 'Piso 2', 20, '2', 'Edificio B', 'Disponible', 1, NOW(), NOW()),
        ('Laboratorio 202', 'Laboratorio de redes y telecomunicaciones', 'Piso 2', 25, '2', 'Edificio B', 'Disponible', 1, NOW(), NOW()),
        ('Aula 301', 'Sala de gestión empresarial', 'Piso 3', 40, '3', 'Edificio C', 'Disponible', 1, NOW(), NOW()),
        ('Aula 302', 'Sala de emprendimiento e innovación', 'Piso 3', 35, '3', 'Edificio C', 'Disponible', 1, NOW(), NOW()),
        ('Auditorio Principal', 'Gran auditorio para eventos y conferencias', 'Piso 0', 200, '0', 'Edificio Principal', 'Disponible', 1, NOW(), NOW()),
        ('Sala de Reuniones A', 'Sala de reuniones ejecutivas', 'Piso 1', 15, '1', 'Edificio A', 'Disponible', 1, NOW(), NOW()),
        ('Sala de Reuniones B', 'Sala de trabajo colaborativo', 'Piso 2', 12, '2', 'Edificio B', 'Disponible', 1, NOW(), NOW()),
        ('Centro de Recursos', 'Centro de aprendizaje con computadores', 'Piso 1', 50, '1', 'Edificio A', 'Disponible', 1, NOW(), NOW()),
        ('Taller de Soldadura', 'Taller especializado en soldadura industrial', 'Sótano', 20, '-1', 'Edificio B', 'Disponible', 1, NOW(), NOW()),
        ('Taller de Mecánica', 'Taller de reparación y mantenimiento mecánico', 'Sótano', 25, '-1', 'Edificio C', 'Disponible', 1, NOW(), NOW());
        """
        
        cursor.execute(insert_data_sql)
        connection.commit()
        print("✅ 12 ambientes de ejemplo insertados correctamente")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando tabla de ambientes: {e}")
        return False

def verify_environments():
    """Verifica que los ambientes se crearon correctamente"""
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
        cursor.execute("SELECT COUNT(*) as count FROM ambientes WHERE activo = 1")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        print(f"\n✅ Total de ambientes activos: {count}")
        
        # Mostrar algunos ambientes
        cursor.execute("SELECT id, nombre, ubicacion, capacidad FROM ambientes WHERE activo = 1 LIMIT 5")
        ambientes = cursor.fetchall()
        print("\n📊 Primeros ambientes:")
        for amb in ambientes:
            print(f"   - {amb['nombre']} (Capacidad: {amb['capacidad']}, Ubicación: {amb['ubicacion']})")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando ambientes: {e}")
        return False

def main():
    print("=" * 60)
    print("📁 CREADOR DE TABLA DE AMBIENTES")
    print("=" * 60)
    
    if not create_environments_table():
        return False
    
    if not verify_environments():
        return False
    
    print("\n" + "=" * 60)
    print("✅ AMBIENTES CONFIGURADOS CORRECTAMENTE")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
