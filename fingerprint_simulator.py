#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fingerprint_simulator.py
- Simulador de huellas digitales para pruebas del sistema
- Permite probar la validación sin sensor físico
"""

import sys
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *
from config import *

class FingerprintSimulator:
    """Simulador de huellas digitales para pruebas"""
    
    def __init__(self):
        self.connected = True  # Siempre conectado en simulación
        print("🎭 MODO SIMULACIÓN ACTIVADO - No se requiere sensor físico")
        
    def connect(self) -> bool:
        """Simula conexión al sensor"""
        print("✅ Simulador de huellas conectado")
        return True
    
    def disconnect(self):
        """Simula desconexión"""
        print("🔌 Simulador de huellas desconectado")
    
    def scan_fingerprint(self, timeout: int = DEFAULT_TIMEOUT_S) -> Optional[bytes]:
        """Simula escaneo de huella"""
        print("👆 SIMULANDO ESCANEO DE HUELLA...")
        print("   (En modo simulación, se usa una huella de prueba)")
        
        # Simular delay de escaneo
        time.sleep(2)
        
        # Crear datos simulados de huella
        simulated_fingerprint = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A' * 10
        
        print("✅ Huella simulada escaneada exitosamente")
        return simulated_fingerprint
    
    def validate_fingerprint_against_database(self, scanned_characteristics: bytes) -> Optional[Dict[str, Any]]:
        """Valida la huella simulada contra la base de datos"""
        try:
            # Obtener todas las personas con huellas registradas
            personal_with_fingerprints = get_personal_with_fingerprints()
            
            if not personal_with_fingerprints:
                print("❌ No hay huellas registradas en la base de datos")
                return None
            
            print(f"🔍 Validando huella simulada contra {len(personal_with_fingerprints)} registros...")
            
            # En modo simulación, siempre retornamos el primer usuario con huella
            # Esto permite probar el flujo completo del sistema
            best_match = personal_with_fingerprints[0]
            best_score = 85  # Score simulado alto
            
            if best_match:
                print(f"✅ Huella validada - Usuario: {best_match['nombres']} {best_match['apellidos']}")
                print(f"   Tipo: {best_match['tipo_personal_nombre']}")
                print(f"   Score de similitud: {best_score}")
                print(f"   Documento: {best_match['documento_tipo']} {best_match['documento_numero']}")
                
                # Registrar el acceso exitoso
                log_access(
                    best_match['id'], 
                    'ENTRADA', 
                    f"Acceso biométrico simulado exitoso - Score: {best_score}"
                )
                
                return best_match
            else:
                print("❌ Huella no coincide con ningún usuario registrado")
                return None
                
        except Exception as e:
            print(f"❌ Error validando huella: {e}")
            return None
    
    def get_user_permissions(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene los permisos del usuario basado en su tipo de personal"""
        try:
            permissions = {
                'can_access_keys': False,
                'max_keys_per_day': 0,
                'special_permissions': False,
                'user_type': user.get('tipo_personal_nombre', 'DESCONOCIDO')
            }
            
            # Obtener tipo de personal
            personal_types = get_personal_types()
            for pt in personal_types:
                if pt['id'] == user['tipo_personal_id']:
                    permissions['max_keys_per_day'] = pt['max_llaves_por_dia']
                    permissions['special_permissions'] = bool(pt['permisos_especiales'])
                    permissions['can_access_keys'] = pt['max_llaves_por_dia'] > 0
                    break
            
            return permissions
            
        except Exception as e:
            print(f"❌ Error obteniendo permisos: {e}")
            return {
                'can_access_keys': False,
                'max_keys_per_day': 0,
                'special_permissions': False,
                'user_type': 'ERROR'
            }
    
    def check_daily_key_limit(self, user_id: int) -> Tuple[bool, int, int]:
        """Verifica si el usuario puede recibir más llaves hoy"""
        try:
            # Obtener asignaciones del día
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
                cur.execute(query, (user_id, today))
                result = cur.fetchone()
                current_keys = result[0] if result else 0
                
                # Obtener límite del usuario
                user = get_personal_by_id(user_id)
                if user:
                    user_permissions = self.get_user_permissions(user)
                    max_keys = user_permissions['max_keys_per_day']
                    
                    can_receive = current_keys < max_keys
                    remaining = max_keys - current_keys
                    
                    return can_receive, current_keys, remaining
                
                return False, current_keys, 0
                
        except Exception as e:
            print(f"❌ Error verificando límite diario: {e}")
            return False, 0, 0

def main():
    """Función principal de demostración con simulador"""
    print("🎭 SIMULADOR DE HUELLAS DIGITALES - sistema_llaves_v2")
    print("=" * 70)
    print("💡 Este modo permite probar el sistema sin sensor físico")
    print("=" * 70)
    
    # Crear simulador
    simulator = FingerprintSimulator()
    
    # Conectar al simulador
    if not simulator.connect():
        print("❌ No se pudo conectar al simulador")
        return
    
    try:
        # Escanear huella simulada
        print("\n👆 ESCANEO SIMULADO DE HUELLA")
        print("-" * 50)
        
        scanned_characteristics = simulator.scan_fingerprint()
        if not scanned_characteristics:
            print("❌ No se pudo simular el escaneo de huella")
            return
        
        # Validar contra la base de datos
        print("\n🔍 VALIDACIÓN EN BASE DE DATOS")
        print("-" * 50)
        
        user = simulator.validate_fingerprint_against_database(scanned_characteristics)
        if not user:
            print("❌ Usuario no autorizado")
            return
        
        # Mostrar información del usuario
        print("\n👤 INFORMACIÓN DEL USUARIO")
        print("-" * 50)
        print(f"Nombre: {user['nombres']} {user['apellidos']}")
        print(f"Documento: {user['documento_tipo']} {user['documento_numero']}")
        print(f"Email: {user['email']}")
        print(f"Tipo: {user['tipo_personal_nombre']}")
        
        # Obtener permisos
        permissions = simulator.get_user_permissions(user)
        print(f"\n🔑 PERMISOS:")
        print(f"   • Acceso a llaves: {'✅ Sí' if permissions['can_access_keys'] else '❌ No'}")
        print(f"   • Máximo llaves por día: {permissions['max_keys_per_day']}")
        print(f"   • Permisos especiales: {'✅ Sí' if permissions['special_permissions'] else '❌ No'}")
        
        # Verificar límite diario
        if permissions['can_access_keys']:
            can_receive, current, remaining = simulator.check_daily_key_limit(user['id'])
            print(f"\n📊 ESTADO DIARIO:")
            print(f"   • Llaves recibidas hoy: {current}")
            print(f"   • Llaves restantes: {remaining}")
            print(f"   • Puede recibir más: {'✅ Sí' if can_receive else '❌ No'}")
        
        print("\n✅ VALIDACIÓN SIMULADA COMPLETADA EXITOSAMENTE")
        print("\n💡 Próximos pasos:")
        print("   1. Usar key_manager.py para gestionar llaves")
        print("   2. Integrar con la interfaz principal")
        print("   3. Conectar sensor físico real cuando esté disponible")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulator.disconnect()

if __name__ == "__main__":
    main()
