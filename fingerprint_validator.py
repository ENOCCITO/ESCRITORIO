#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fingerprint_validator.py
- Validador de huellas digitales para el sistema de llaves
- Integra con la base de datos sistema_llaves_v2
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *
from config import *

def _import_pyfingerprint():
    """Importa pyfingerprint de forma diferida"""
    try:
        from pyfingerprint.pyfingerprint import (
            PyFingerprint,
            FINGERPRINT_CHARBUFFER1,
            FINGERPRINT_CHARBUFFER2,
        )
        return (PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2), None
    except ImportError as e:
        return None, e
    except Exception as e:
        return None, e

class FingerprintValidator:
    """Validador de huellas digitales para el sistema de llaves"""
    
    def __init__(self, port: str = FINGERPRINT_PORT_DEFAULT, baud: int = FINGERPRINT_BAUD_DEFAULT):
        self.port = port
        self.baud = baud
        self.fingerprint = None
        self.connected = False
        
    def connect(self) -> bool:
        """Conecta al sensor de huellas"""
        try:
            result = _import_pyfingerprint()
            if result[0] is None:
                print(f"❌ Error: No se pudo importar pyfingerprint: {result[1]}")
                return False
            
            PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2 = result[0]
            
            self.fingerprint = PyFingerprint(self.port, self.baud, 0xFFFFFFFF, 0x00000000)
            
            if not self.fingerprint.verifyPassword():
                print("❌ Error: Contraseña del sensor de huellas incorrecta")
                return False
            
            print(f"✅ Sensor de huellas conectado en {self.port}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"❌ Error conectando al sensor de huellas: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del sensor de huellas"""
        if self.fingerprint:
            self.fingerprint = None
        self.connected = False
        print("🔌 Sensor de huellas desconectado")
    
    def scan_fingerprint(self, timeout: int = DEFAULT_TIMEOUT_S) -> Optional[bytes]:
        """Escanea una huella digital"""
        if not self.connected:
            print("❌ Error: Sensor de huellas no conectado")
            return False
        
        try:
            print("👆 Coloque su dedo en el sensor...")
            
            # Esperar hasta que se detecte una huella
            while not self.fingerprint.readImage():
                time.sleep(0.1)
            
            # Convertir la imagen a características
            self.fingerprint.convertImage(FINGERPRINT_CHARBUFFER1)
            
            # Buscar la huella en la base de datos del sensor
            result = self.fingerprint.searchTemplate()
            position_number = result[0]
            accuracy_score = result[1]
            
            if position_number == -1:
                print("❌ Huella no encontrada en la base de datos del sensor")
                return None
            
            if accuracy_score < DEFAULT_THRESHOLD:
                print(f"❌ Calidad de huella insuficiente (score: {accuracy_score})")
                return None
            
            print(f"✅ Huella detectada - Posición: {position_number}, Calidad: {accuracy_score}")
            
            # Obtener la plantilla de características
            self.fingerprint.loadTemplate(position_number, FINGERPRINT_CHARBUFFER2)
            characteristics = self.fingerprint.downloadCharacteristics(FINGERPRINT_CHARBUFFER2)
            
            return characteristics
            
        except Exception as e:
            print(f"❌ Error escaneando huella: {e}")
            return None
    
    def validate_fingerprint_against_database(self, scanned_characteristics: bytes) -> Optional[Dict[str, Any]]:
        """Valida la huella escaneada contra la base de datos"""
        try:
            # Obtener todas las personas con huellas registradas
            personal_with_fingerprints = get_personal_with_fingerprints()
            
            if not personal_with_fingerprints:
                print("❌ No hay huellas registradas en la base de datos")
                return None
            
            print(f"🔍 Validando huella contra {len(personal_with_fingerprints)} registros...")
            
            best_match = None
            best_score = 0
            
            for person in personal_with_fingerprints:
                if person['huella_digital']:
                    # Comparar características (simulación simple)
                    # En un sistema real, usarías algoritmos de comparación de huellas
                    similarity_score = self._compare_characteristics(
                        scanned_characteristics, 
                        person['huella_digital']
                    )
                    
                    if similarity_score > best_score and similarity_score >= DEFAULT_THRESHOLD:
                        best_score = similarity_score
                        best_match = person
            
            if best_match:
                print(f"✅ Huella validada - Usuario: {best_match['nombres']} {best_match['apellidos']}")
                print(f"   Tipo: {best_match['tipo_personal_nombre']}")
                print(f"   Score de similitud: {best_score}")
                print(f"   Documento: {best_match['documento_tipo']} {best_match['documento_numero']}")
                
                # Registrar el acceso exitoso
                log_access(
                    best_match['id'], 
                    'ENTRADA', 
                    f"Acceso biométrico exitoso - Score: {best_score}"
                )
                
                return best_match
            else:
                print("❌ Huella no coincide con ningún usuario registrado")
                print("💡 Sugerencia: Verifica que la huella esté bien registrada en la base de datos")
                return None
                
        except Exception as e:
            print(f"❌ Error validando huella: {e}")
            return None
    
    def _compare_characteristics(self, scanned: bytes, stored: bytes) -> int:
        """
        Compara características de huellas (simulación)
        En un sistema real, usarías algoritmos especializados
        """
        try:
            # Simulación simple de comparación
            # En la práctica, usarías algoritmos como minutiae matching
            
            if not scanned or not stored:
                return 0
            
            # Convertir a listas para comparación
            scanned_list = list(scanned)
            stored_list = list(stored)
            
            # Calcular similitud básica (esto es solo una simulación)
            common_bytes = 0
            total_bytes = min(len(scanned_list), len(stored_list))
            
            for i in range(total_bytes):
                if scanned_list[i] == stored_list[i]:
                    common_bytes += 1
            
            if total_bytes == 0:
                return 0
            
            similarity = int((common_bytes / total_bytes) * 100)
            
            # Ajustar para que sea más realista
            # En la práctica, los scores suelen estar entre 0-100
            if similarity > 80:
                similarity = 80 + (similarity - 80) * 0.25
            
            return min(similarity, 100)
            
        except Exception as e:
            print(f"❌ Error comparando características: {e}")
            return 0
    
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
    """Función principal de demostración"""
    print("🔐 VALIDADOR DE HUELLAS DIGITALES - sistema_llaves_v2")
    print("=" * 60)
    
    # Crear validador
    validator = FingerprintValidator()
    
    # Conectar al sensor
    if not validator.connect():
        print("❌ No se pudo conectar al sensor de huellas")
        return
    
    try:
        # Escanear huella
        print("\n👆 ESCANEO DE HUELLA")
        print("-" * 40)
        
        scanned_characteristics = validator.scan_fingerprint()
        if not scanned_characteristics:
            print("❌ No se pudo escanear la huella")
            return
        
        # Validar contra la base de datos
        print("\n🔍 VALIDACIÓN EN BASE DE DATOS")
        print("-" * 40)
        
        user = validator.validate_fingerprint_against_database(scanned_characteristics)
        if not user:
            print("❌ Usuario no autorizado")
            return
        
        # Mostrar información del usuario
        print("\n👤 INFORMACIÓN DEL USUARIO")
        print("-" * 40)
        print(f"Nombre: {user['nombres']} {user['apellidos']}")
        print(f"Documento: {user['documento_tipo']} {user['documento_numero']}")
        print(f"Email: {user['email']}")
        print(f"Tipo: {user['tipo_personal_nombre']}")
        
        # Obtener permisos
        permissions = validator.get_user_permissions(user)
        print(f"\n🔑 PERMISOS:")
        print(f"   • Acceso a llaves: {'✅ Sí' if permissions['can_access_keys'] else '❌ No'}")
        print(f"   • Máximo llaves por día: {permissions['max_keys_per_day']}")
        print(f"   • Permisos especiales: {'✅ Sí' if permissions['special_permissions'] else '❌ No'}")
        
        # Verificar límite diario
        if permissions['can_access_keys']:
            can_receive, current, remaining = validator.check_daily_key_limit(user['id'])
            print(f"\n📊 ESTADO DIARIO:")
            print(f"   • Llaves recibidas hoy: {current}")
            print(f"   • Llaves restantes: {remaining}")
            print(f"   • Puede recibir más: {'✅ Sí' if can_receive else '❌ No'}")
        
        print("\n✅ VALIDACIÓN COMPLETADA EXITOSAMENTE")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        validator.disconnect()

if __name__ == "__main__":
    main()
