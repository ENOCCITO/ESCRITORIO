#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_alert_system.py
- Prueba del sistema de alertas para el sistema biométrico
- Demostración de las alertas de acceso denegado y concedido
"""

import time
from alert_system import alert_system
from role_validator import role_validator

def test_alert_system():
    """Prueba el sistema de alertas"""
    print("🧪 PRUEBA DEL SISTEMA DE ALERTAS")
    print("=" * 50)
    
    # Probar alertas de acceso denegado para diferentes roles
    roles = ['admin', 'instructor', 'security', 'cleaning', 'administrative']
    
    print("\n1. Probando alertas de acceso denegado...")
    for role in roles:
        print(f"   - Mostrando alerta para rol: {role}")
        alert_system.show_access_denied_alert(role, "Usuario de Prueba")
        time.sleep(2)  # Esperar un poco entre alertas
    
    print("\n2. Probando alerta de huella no encontrada...")
    alert_system.show_fingerprint_not_found_alert()
    time.sleep(2)
    
    print("\n3. Probando alertas de acceso concedido...")
    for role in roles:
        print(f"   - Mostrando alerta para rol: {role}")
        alert_system.show_access_granted_alert(role, "Usuario Autorizado")
        time.sleep(2)
    
    print("\n4. Probando validador de roles...")
    print(f"   - Roles disponibles: {role_validator.get_all_roles()}")
    
    # Simular validación de roles
    test_cases = [
        (1, 'admin', 'ADMINISTRADOR'),
        (2, 'instructor', 'INSTRUCTOR'),
        (3, 'security', 'SEGURIDAD'),
        (4, 'cleaning', 'LIMPIEZA'),
        (5, 'administrative', 'ADMINISTRATIVO')
    ]
    
    for user_id, requested_role, expected_role in test_cases:
        has_access, user_name, user_role = role_validator.validate_role_access(user_id, requested_role)
        print(f"   - Usuario {user_id} solicitando {requested_role}: {'✅' if has_access else '❌'}")
        if user_name:
            print(f"     Nombre: {user_name}, Rol real: {user_role}")
    
    print("\n✅ Prueba del sistema de alertas completada")
    print("   Las alertas se abrieron en el navegador web")
    print("   Cierra las ventanas del navegador cuando termines de revisarlas")

def test_role_validation():
    """Prueba la validación de roles"""
    print("\n🔍 PRUEBA DE VALIDACIÓN DE ROLES")
    print("=" * 50)
    
    # Probar con diferentes combinaciones de usuario y rol
    test_scenarios = [
        (1, 'admin', 'ADMINISTRADOR'),
        (2, 'instructor', 'INSTRUCTOR'),
        (3, 'security', 'SEGURIDAD'),
        (4, 'cleaning', 'LIMPIEZA'),
        (5, 'administrative', 'ADMINISTRATIVO'),
        (1, 'instructor', 'ADMINISTRADOR'),  # Usuario admin intentando acceder como instructor
        (2, 'admin', 'INSTRUCTOR'),          # Usuario instructor intentando acceder como admin
    ]
    
    for user_id, requested_role, expected_role in test_scenarios:
        has_access, user_name, user_role = role_validator.validate_role_access(user_id, requested_role)
        
        print(f"\n👤 Usuario ID: {user_id}")
        print(f"   Rol solicitado: {requested_role}")
        print(f"   Rol real: {user_role}")
        print(f"   Acceso: {'✅ CONCEDIDO' if has_access else '❌ DENEGADO'}")
        
        if not has_access and user_name:
            print(f"   ⚠️  {user_name} no tiene permisos para acceder como {requested_role}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE ALERTAS")
    print("=" * 60)
    
    try:
        # Probar validación de roles
        test_role_validation()
        
        # Preguntar si quiere probar las alertas visuales
        print("\n" + "=" * 60)
        response = input("¿Deseas probar las alertas visuales? (s/n): ").lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_alert_system()
        else:
            print("⏭️  Saltando pruebas visuales")
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
    finally:
        # Limpiar archivos temporales
        try:
            alert_system.cleanup()
            print("🧹 Archivos temporales limpiados")
        except:
            pass
