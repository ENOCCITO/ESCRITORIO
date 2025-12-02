#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_utils import db_connect

cnx = db_connect()
cur = cnx.cursor()

print("Buscando tabla population_groups...")
cur.execute("SHOW TABLES LIKE 'population%'")
result = cur.fetchall()
print(f"Resultado: {result}")

if not result:
    print("\nNo existe. Creando...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `population_groups` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) NOT NULL,
            `description` text,
            `deleted_at` timestamp NULL DEFAULT NULL,
            `created_at` timestamp NULL DEFAULT NULL,
            `updated_at` timestamp NULL DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    cnx.commit()
    print("Tabla creada")
    
    # Insertar un registro por defecto
    cur.execute("INSERT INTO population_groups (name, description) VALUES ('General', 'Población general')")
    cnx.commit()
    print("Registro insertado")

cur.close()
cnx.close()
