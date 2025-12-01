#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
explore_tables.py
- Script para explorar la estructura exacta de las tablas en sistema_llaves_v2
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.db_utils import db_connect

def explore_table_structure(table_name):
    """Explora la estructura de una tabla específica"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Obtener estructura de la tabla
            cur.execute(f"DESCRIBE {table_name}")
            columns = cur.fetchall()
            
            print(f"\n📋 ESTRUCTURA DE LA TABLA: {table_name}")
            print("-" * 80)
            print(f"{'Campo':<25} {'Tipo':<20} {'Nulo':<8} {'Llave':<8} {'Default':<15} {'Extra':<10}")
            print("-" * 80)
            
            for col in columns:
                field, type_name, null, key, default, extra = col
                print(f"{field:<25} {type_name:<20} {null:<8} {key:<8} {str(default):<15} {extra:<10}")
            
            # Obtener algunos registros de ejemplo
            cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_data = cur.fetchall()
            
            if sample_data:
                print(f"\n📊 MUESTRA DE DATOS (primeros 3 registros):")
                print("-" * 80)
                
                # Obtener nombres de columnas
                cur.execute(f"SHOW COLUMNS FROM {table_name}")
                column_names = [col[0] for col in cur.fetchall()]
                
                for i, row in enumerate(sample_data, 1):
                    print(f"\nRegistro {i}:")
                    for j, value in enumerate(row):
                        if value is not None:
                            # Truncar valores muy largos
                            display_value = str(value)
                            if len(display_value) > 50:
                                display_value = display_value[:47] + "..."
                            print(f"  {column_names[j]}: {display_value}")
                        else:
                            print(f"  {column_names[j]}: NULL")
            
            cur.close()
            
    except Exception as e:
        print(f"❌ Error explorando tabla {table_name}: {e}")

def main():
    """Función principal"""
    print("🔍 EXPLORANDO ESTRUCTURA DE TABLAS EN sistema_llaves_v2")
    print("=" * 80)
    
    # Tablas principales a explorar
    tables = [
        'personal',
        'tipos_personal', 
        'llaves',
        'ambientes',
        'asignaciones_llaves',
        'logs_acceso'
    ]
    
    for table in tables:
        try:
            explore_table_structure(table)
        except Exception as e:
            print(f"❌ No se pudo explorar la tabla {table}: {e}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Exploración interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la exploración: {e}")
        import traceback
        traceback.print_exc()
