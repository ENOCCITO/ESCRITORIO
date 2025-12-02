#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_missing_tables.py
- Script para crear las tablas faltantes en SICEFA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

def create_missing_tables():
    """Crea las tablas faltantes en SICEFA"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            print("🔄 Creando tablas faltantes en SICEFA...\n")
            
            # 1. Tabla EPS
            print("📋 Creando tabla eps...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `eps` (
                    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                    `nombre` varchar(255) NOT NULL,
                    `sigla` varchar(50),
                    `deleted_at` timestamp NULL DEFAULT NULL,
                    `created_at` timestamp NULL DEFAULT NULL,
                    `updated_at` timestamp NULL DEFAULT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            print("   ✅ Tabla eps creada")
            
            # 2. Tabla Pension Entities
            print("📋 Creando tabla pension_entities...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `pension_entities` (
                    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                    `nombre` varchar(255) NOT NULL,
                    `sigla` varchar(50),
                    `deleted_at` timestamp NULL DEFAULT NULL,
                    `created_at` timestamp NULL DEFAULT NULL,
                    `updated_at` timestamp NULL DEFAULT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            print("   ✅ Tabla pension_entities creada")
            
            # 3. Tabla Population Groups
            print("📋 Creando tabla population_groups...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `population_groups` (
                    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
                    `nombre` varchar(255) NOT NULL,
                    `descripcion` text,
                    `deleted_at` timestamp NULL DEFAULT NULL,
                    `created_at` timestamp NULL DEFAULT NULL,
                    `updated_at` timestamp NULL DEFAULT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            print("   ✅ Tabla population_groups creada")
            
            cnx.commit()
            print("\n✅ ¡Todas las tablas fueron creadas correctamente!")
            
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_missing_tables()
