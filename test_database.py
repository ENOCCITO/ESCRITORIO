#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_database.py
- Script de prueba para validar la conexión a sistema_llaves_v2
- Verifica el acceso a las tablas personal, tipos_personal, llaves, etc.
"""

import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *

def main():
    """Función principal de prueba"""
    print("🔐 PRUEBA DE CONEXIÓN A LA BASE DE DATOS sistema_llaves_v2")
    print("=" * 60)
    
    # 1. Probar conexión básica
    print("\n1️⃣ Probando conexión básica...")
    if test_database_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Error de conexión")
        return
    
    # 2. Obtener información general de la base de datos
    print("\n2️⃣ Obteniendo información general...")
    db_info = get_database_info()
    if db_info:
        print("📊 Información de la base de datos:")
        for key, value in db_info.items():
            print(f"   • {key}: {value}")
    else:
        print("❌ No se pudo obtener información de la base de datos")
    
    # 3. Obtener tipos de personal
    print("\n3️⃣ Obteniendo tipos de personal...")
    personal_types = get_personal_types()
    if personal_types:
        print(f"✅ Se encontraron {len(personal_types)} tipos de personal:")
        for pt in personal_types:
            print(f"   • {pt['nombre']}: {pt['descripcion']} (Max llaves: {pt['max_llaves_por_dia']})")
    else:
        print("❌ No se pudieron obtener los tipos de personal")
    
    # 4. Obtener personal con huellas
    print("\n4️⃣ Obteniendo personal con huellas...")
    personal_with_fingerprints = get_personal_with_fingerprints()
    if personal_with_fingerprints:
        print(f"✅ Se encontraron {len(personal_with_fingerprints)} personas con huellas:")
        for person in personal_with_fingerprints[:5]:  # Mostrar solo los primeros 5
            print(f"   • {person['nombres']} {person['apellidos']} ({person['tipo_personal_nombre']})")
        if len(personal_with_fingerprints) > 5:
            print(f"   ... y {len(personal_with_fingerprints) - 5} más")
    else:
        print("❌ No se pudo obtener personal con huellas")
    
    # 5. Obtener ambientes
    print("\n5️⃣ Obteniendo ambientes...")
    environments = get_environments()
    if environments:
        print(f"✅ Se encontraron {len(environments)} ambientes:")
        for env in environments:
            print(f"   • {env['nombre']}: {env['descripcion']} ({env['ubicacion']})")
    else:
        print("❌ No se pudieron obtener los ambientes")
    
    # 6. Obtener llaves disponibles
    print("\n6️⃣ Obteniendo llaves disponibles...")
    available_keys = get_available_keys()
    if available_keys:
        print(f"✅ Se encontraron {len(available_keys)} llaves disponibles:")
        for key in available_keys[:5]:  # Mostrar solo las primeras 5
            print(f"   • {key['codigo_llave']}: {key['descripcion']}")
        if len(available_keys) > 5:
            print(f"   ... y {len(available_keys) - 5} más")
    else:
        print("❌ No se pudieron obtener las llaves disponibles")
    
    # 7. Obtener asignaciones activas
    print("\n7️⃣ Obteniendo asignaciones activas...")
    active_assignments = get_active_key_assignments()
    if active_assignments:
        print(f"✅ Se encontraron {len(active_assignments)} asignaciones activas:")
        for assignment in active_assignments[:3]:  # Mostrar solo las primeras 3
            print(f"   • {assignment['nombres']} {assignment['apellidos']} → {assignment['llave_codigo']} ({assignment['ambiente_nombre']})")
        if len(active_assignments) > 3:
            print(f"   ... y {len(active_assignments) - 3} más")
    else:
        print("ℹ️ No hay asignaciones activas en este momento")
    
    # 8. Obtener logs de acceso
    print("\n8️⃣ Obteniendo logs de acceso...")
    access_logs = get_access_logs(limit=5)
    if access_logs:
        print(f"✅ Se encontraron {len(access_logs)} logs de acceso recientes:")
        for log in access_logs:
            print(f"   • {log['nombres']} {log['apellidos']}: {log['tipo_accion']} - {log['fecha_hora']}")
    else:
        print("ℹ️ No hay logs de acceso registrados")
    
    print("\n" + "=" * 60)
    print("🎯 PRUEBA COMPLETADA")
    
    # Resumen final
    if db_info:
        print(f"\n📋 RESUMEN:")
        print(f"   • Total de personal: {db_info.get('total_personal', 0)}")
        print(f"   • Personal con huellas: {db_info.get('personal_con_huellas', 0)}")
        print(f"   • Tipos de personal: {db_info.get('tipos_personal', 0)}")
        print(f"   • Total de llaves: {db_info.get('total_llaves', 0)}")
        print(f"   • Llaves disponibles: {db_info.get('llaves_disponibles', 0)}")
        print(f"   • Ambientes: {db_info.get('total_ambientes', 0)}")
        print(f"   • Asignaciones activas: {db_info.get('asignaciones_activas', 0)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
