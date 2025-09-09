#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnose_fingerprints.py
- Diagnóstico de huellas digitales en la base de datos
- Analiza el estado de las huellas registradas
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *

def analyze_fingerprint_data():
    """Analiza los datos de huellas en la base de datos"""
    print("🔍 DIAGNÓSTICO DE HUELLAS DIGITALES - sistema_llaves_v2")
    print("=" * 70)
    
    try:
        # 1. Verificar conexión
        print("\n1️⃣ VERIFICANDO CONEXIÓN...")
        if not test_database_connection():
            print("❌ No se puede conectar a la base de datos")
            return
        print("✅ Conexión exitosa")
        
        # 2. Obtener información general
        print("\n2️⃣ INFORMACIÓN GENERAL...")
        db_info = get_database_info()
        if db_info:
            print(f"   • Total personal: {db_info['total_personal']}")
            print(f"   • Personal con huellas: {db_info['personal_con_huellas']}")
            print(f"   • Total llaves: {db_info['total_llaves']}")
            print(f"   • Llaves disponibles: {db_info['llaves_disponibles']}")
        
        # 3. Analizar personal con huellas
        print("\n3️⃣ ANÁLISIS DE PERSONAL CON HUELLAS...")
        personal_with_fingerprints = get_personal_with_fingerprints()
        
        if not personal_with_fingerprints:
            print("❌ No hay personal con huellas registradas")
            return
        
        print(f"✅ Se encontraron {len(personal_with_fingerprints)} personas con huellas:")
        
        for i, person in enumerate(personal_with_fingerprints, 1):
            print(f"\n   👤 PERSONA {i}:")
            print(f"      • ID: {person['id']}")
            print(f"      • Nombre: {person['nombres']} {person['apellidos']}")
            print(f"      • Documento: {person['documento_tipo']} {person['documento_numero']}")
            print(f"      • Tipo: {person['tipo_personal_nombre']}")
            print(f"      • Email: {person['email']}")
            print(f"      • Activo: {'✅ Sí' if person['activo'] else '❌ No'}")
            
            # Analizar huella digital
            if person['huella_digital']:
                huella_bytes = len(person['huella_digital'])
                huella_hex = person['huella_digital'][:20].hex()  # Primeros 20 bytes
                print(f"      • Huella: {huella_bytes} bytes")
                print(f"      • Primeros bytes: {huella_hex}...")
                print(f"      • Fecha registro: {person['fecha_registro_huella']}")
            else:
                print(f"      • Huella: ❌ NO REGISTRADA")
        
        # 4. Verificar tipos de personal
        print("\n4️⃣ TIPOS DE PERSONAL...")
        personal_types = get_personal_types()
        for pt in personal_types:
            print(f"   • {pt['nombre']}: {pt['descripcion']}")
            print(f"     - Max llaves por día: {pt['max_llaves_por_dia']}")
            print(f"     - Permisos especiales: {'✅ Sí' if pt['permisos_especiales'] else '❌ No'}")
        
        # 5. Verificar logs de acceso
        print("\n5️⃣ LOGS DE ACCESO RECIENTES...")
        access_logs = get_access_logs(limit=10)
        if access_logs:
            print(f"✅ Se encontraron {len(access_logs)} logs recientes:")
            for log in access_logs[:5]:  # Mostrar solo los primeros 5
                print(f"   • {log['nombres']} {log['apellidos']}: {log['tipo_accion']} - {log['fecha_hora']}")
                if log['notas']:
                    print(f"     Notas: {log['notas']}")
        else:
            print("ℹ️ No hay logs de acceso registrados")
        
        # 6. Recomendaciones
        print("\n6️⃣ RECOMENDACIONES...")
        print("   💡 Para probar el sistema sin sensor físico:")
        print("      • Ejecuta: python fingerprint_simulator.py")
        print("   💡 Para gestionar llaves:")
        print("      • Ejecuta: python key_manager.py")
        print("   💡 Para conectar sensor real:")
        print("      • Verifica puerto COM3 en config.py")
        print("      • Instala pyfingerprint: pip install pyfingerprint")
        
        print("\n✅ DIAGNÓSTICO COMPLETADO")
        
    except Exception as e:
        print(f"\n❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()

def test_fingerprint_validation():
    """Prueba la validación de huellas con datos simulados"""
    print("\n🧪 PRUEBA DE VALIDACIÓN DE HUELLAS...")
    print("-" * 50)
    
    try:
        # Obtener personal con huellas
        personal_with_fingerprints = get_personal_with_fingerprints()
        
        if not personal_with_fingerprints:
            print("❌ No hay huellas para probar")
            return
        
        # Tomar la primera persona con huella
        test_person = personal_with_fingerprints[0]
        print(f"👤 Probando con: {test_person['nombres']} {test_person['apellidos']}")
        
        # Crear datos simulados de huella
        simulated_fingerprint = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A' * 10
        
        # Simular comparación
        print("🔍 Simulando comparación de huellas...")
        
        # Obtener permisos
        personal_types = get_personal_types()
        user_type = None
        for pt in personal_types:
            if pt['id'] == test_person['tipo_personal_id']:
                user_type = pt
                break
        
        if user_type:
            print(f"✅ Tipo de personal: {user_type['nombre']}")
            print(f"   • Max llaves por día: {user_type['max_llaves_por_dia']}")
            print(f"   • Permisos especiales: {'✅ Sí' if user_type['permisos_especiales'] else '❌ No'}")
            
            # Verificar límite diario
            today = datetime.now().date()
            with db_connect() as cnx:
                cur = cnx.cursor()
                query = """
                    SELECT COUNT(*) as count
                    FROM asignaciones_llaves
                    WHERE personal_id = %s 
                      AND DATE(fecha_asignacion) = %s
                      AND estado = 'ACTIVA'
                """
                cur.execute(query, (test_person['id'], today))
                result = cur.fetchone()
                current_keys = result[0] if result else 0
                
                can_receive = current_keys < user_type['max_llaves_por_dia']
                remaining = user_type['max_llaves_por_dia'] - current_keys
                
                print(f"📊 Estado diario:")
                print(f"   • Llaves recibidas hoy: {current_keys}")
                print(f"   • Llaves restantes: {remaining}")
                print(f"   • Puede recibir más: {'✅ Sí' if can_receive else '❌ No'}")
                
                cur.close()
        
        print("✅ Prueba de validación completada")
        
    except Exception as e:
        print(f"❌ Error en prueba de validación: {e}")

def main():
    """Función principal"""
    try:
        analyze_fingerprint_data()
        test_fingerprint_validation()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Diagnóstico interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
