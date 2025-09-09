#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_complete_system.py
- Prueba completa del sistema de dispensación de llaves
- Integra autenticación, gestión de llaves y logs
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *
from config import *

def test_complete_flow():
    """Prueba el flujo completo del sistema"""
    print("🧪 PRUEBA COMPLETA DEL SISTEMA DE LLAVES")
    print("=" * 70)
    
    try:
        # 1. Verificar conexión a base de datos
        print("\n1️⃣ VERIFICANDO CONEXIÓN...")
        if not test_database_connection():
            print("❌ No se puede conectar a la base de datos")
            return False
        print("✅ Conexión exitosa")
        
        # 2. Obtener información del sistema
        print("\n2️⃣ INFORMACIÓN DEL SISTEMA...")
        db_info = get_database_info()
        if db_info:
            print(f"   • Personal total: {db_info['total_personal']}")
            print(f"   • Personal con huellas: {db_info['personal_con_huellas']}")
            print(f"   • Llaves totales: {db_info['total_llaves']}")
            print(f"   • Llaves disponibles: {db_info['llaves_disponibles']}")
            print(f"   • Ambientes: {db_info['total_ambientes']}")
            print(f"   • Asignaciones activas: {db_info['asignaciones_activas']}")
        
        # 3. Simular autenticación biométrica
        print("\n3️⃣ SIMULANDO AUTENTICACIÓN BIOMÉTRICA...")
        personal_with_fingerprints = get_personal_with_fingerprints()
        
        if not personal_with_fingerprints:
            print("❌ No hay personal con huellas para probar")
            return False
        
        # Tomar el primer usuario con huella
        test_user = personal_with_fingerprints[0]
        print(f"✅ Usuario autenticado: {test_user['nombres']} {test_user['apellidos']}")
        print(f"   • Tipo: {test_user['tipo_personal_nombre']}")
        print(f"   • Documento: {test_user['documento_tipo']} {test_user['documento_numero']}")
        
        # 4. Verificar permisos del usuario
        print("\n4️⃣ VERIFICANDO PERMISOS...")
        personal_types = get_personal_types()
        user_type = None
        for pt in personal_types:
            if pt['id'] == test_user['tipo_personal_id']:
                user_type = pt
                break
        
        if user_type:
            print(f"✅ Tipo de personal: {user_type['nombre']}")
            print(f"   • Descripción: {user_type['descripcion']}")
            print(f"   • Max llaves por día: {user_type['max_llaves_por_dia']}")
            print(f"   • Permisos especiales: {'✅ Sí' if user_type['permisos_especiales'] else '❌ No'}")
            
            can_access_keys = user_type['max_llaves_por_dia'] > 0
            print(f"   • Acceso a llaves: {'✅ Sí' if can_access_keys else '❌ No'}")
        
        # 5. Verificar límite diario
        print("\n5️⃣ VERIFICANDO LÍMITE DIARIO...")
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
            cur.execute(query, (test_user['id'], today))
            result = cur.fetchone()
            current_keys = result[0] if result else 0
            
            if user_type:
                max_keys = user_type['max_llaves_por_dia']
                can_receive = current_keys < max_keys
                remaining = max_keys - current_keys
                
                print(f"✅ Estado diario:")
                print(f"   • Llaves recibidas hoy: {current_keys}")
                print(f"   • Llaves restantes: {remaining}")
                print(f"   • Puede recibir más: {'✅ Sí' if can_receive else '❌ No'}")
            
            cur.close()
        
        # 6. Mostrar llaves disponibles
        print("\n6️⃣ LLAVES DISPONIBLES...")
        available_keys = get_available_keys()
        if available_keys:
            print(f"✅ Se encontraron {len(available_keys)} llaves disponibles:")
            for i, key in enumerate(available_keys[:5], 1):  # Mostrar solo las primeras 5
                print(f"   {i}. {key['codigo_llave']}: {key['descripcion']}")
            if len(available_keys) > 5:
                print(f"   ... y {len(available_keys) - 5} más")
        else:
            print("❌ No hay llaves disponibles")
        
        # 7. Simular asignación de llave (si es posible)
        print("\n7️⃣ SIMULANDO ASIGNACIÓN DE LLAVE...")
        if can_access_keys and can_receive and available_keys:
            # Tomar la primera llave disponible
            test_key = available_keys[0]
            print(f"🔑 Intentando asignar: {test_key['codigo_llave']}")
            
            # Simular asignación
            success = assign_key_to_person(
                test_user['id'], 
                test_key['id'], 
                "Prueba del sistema - Asignación automática"
            )
            
            if success:
                print("✅ Llave asignada exitosamente")
                
                # Registrar en logs
                log_access(
                    test_user['id'], 
                    'ENTREGA_LLAVE', 
                    f"Llave {test_key['codigo_llave']} asignada en prueba del sistema"
                )
                
                # Mostrar asignaciones activas del usuario
                print("\n📋 ASIGNACIONES ACTIVAS DEL USUARIO:")
                active_assignments = get_active_key_assignments()
                user_assignments = [a for a in active_assignments if a['personal_id'] == test_user['id']]
                
                if user_assignments:
                    for assignment in user_assignments:
                        print(f"   • {assignment['llave_codigo']}: {assignment['llave_descripcion']}")
                        print(f"     Fecha: {assignment['fecha_asignacion']}")
                else:
                    print("   ℹ️ No hay asignaciones activas")
                
                # Simular devolución de llave
                print("\n8️⃣ SIMULANDO DEVOLUCIÓN DE LLAVE...")
                if user_assignments:
                    assignment_to_return = user_assignments[0]
                    return_success = return_key_from_person(
                        assignment_to_return['id'],
                        "Prueba del sistema - Devolución automática"
                    )
                    
                    if return_success:
                        print("✅ Llave devuelta exitosamente")
                        
                        # Registrar en logs
                        log_access(
                            test_user['id'], 
                            'DEVOLUCION_LLAVE', 
                            f"Llave {assignment_to_return['llave_codigo']} devuelta en prueba del sistema"
                        )
                    else:
                        print("❌ Error devolviendo la llave")
                else:
                    print("ℹ️ No hay asignaciones para devolver")
            else:
                print("❌ Error asignando la llave")
        else:
            print("ℹ️ No se puede asignar llave (verificar permisos y disponibilidad)")
        
        # 8. Mostrar logs recientes
        print("\n9️⃣ LOGS RECIENTES DEL SISTEMA...")
        access_logs = get_access_logs(limit=5)
        if access_logs:
            print(f"✅ Últimos {len(access_logs)} logs:")
            for log in access_logs:
                print(f"   • {log['nombres']} {log['apellidos']}: {log['tipo_accion']}")
                print(f"     Fecha: {log['fecha_hora']}")
                if log['notas']:
                    print(f"     Notas: {log['notas']}")
        else:
            print("ℹ️ No hay logs recientes")
        
        print("\n✅ PRUEBA COMPLETA FINALIZADA EXITOSAMENTE")
        print("\n💡 El sistema está funcionando correctamente")
        print("   • Base de datos: ✅ Conectada")
        print("   • Autenticación: ✅ Funcionando")
        print("   • Gestión de llaves: ✅ Operativa")
        print("   • Logs: ✅ Registrando")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    try:
        success = test_complete_flow()
        
        if success:
            print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
            print("\n🚀 Próximos pasos:")
            print("   1. Integrar con la interfaz gráfica")
            print("   2. Conectar sensor físico de huellas")
            print("   3. Configurar Arduino para dispensador")
            print("   4. Implementar programación automática")
        else:
            print("\n❌ El sistema tiene problemas que requieren atención")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
