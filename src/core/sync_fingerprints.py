#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_fingerprints.py
- Sincroniza las huellas de la base de datos con el sensor físico
- Descarga las huellas registradas al sensor para que las reconozca
"""

import sys
import os
import time
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.db_utils import *
from src.config.config import *

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

class FingerprintSynchronizer:
    """Sincronizador de huellas entre base de datos y sensor físico"""
    
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
                print("💡 Instala con: pip install pyfingerprint")
                return False
            
            PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2 = result[0]
            
            print(f"🔌 Conectando al sensor en {self.port}...")
            self.fingerprint = PyFingerprint(self.port, self.baud, 0xFFFFFFFF, 0x00000000)
            
            if not self.fingerprint.verifyPassword():
                print("❌ Error: Contraseña del sensor incorrecta")
                return False
            
            print(f"✅ Sensor conectado en {self.port}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"❌ Error conectando al sensor: {e}")
            print("💡 Verifica:")
            print("   • Puerto COM correcto en config.py")
            print("   • Sensor conectado y encendido")
            print("   • Driver del sensor instalado")
            return False
    
    def disconnect(self):
        """Desconecta del sensor"""
        if self.fingerprint:
            self.fingerprint = None
        self.connected = False
        print("🔌 Sensor desconectado")
    
    def get_sensor_info(self):
        """Obtiene información del sensor"""
        if not self.connected:
            print("❌ Sensor no conectado")
            return
        
        try:
            print("\n📊 INFORMACIÓN DEL SENSOR:")
            print("-" * 40)
            
            # Obtener capacidad del sensor
            capacity = self.fingerprint.getStorageCapacity()
            print(f"   • Capacidad total: {capacity} huellas")
            
            # Obtener huellas registradas en el sensor
            template_count = self.fingerprint.getTemplateCount()
            print(f"   • Huellas registradas: {template_count}")
            
            # Obtener índice de seguridad
            security_level = self.fingerprint.getSecurityLevel()
            print(f"   • Nivel de seguridad: {security_level}")
            
            return {
                'capacity': capacity,
                'template_count': template_count,
                'security_level': security_level
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo información: {e}")
            return None
    
    def clear_sensor_database(self):
        """Limpia la base de datos del sensor"""
        if not self.connected:
            print("❌ Sensor no conectado")
            return False
        
        try:
            print("\n🗑️ LIMPIANDO BASE DE DATOS DEL SENSOR...")
            print("⚠️  Esto eliminará TODAS las huellas del sensor")
            
            # Confirmar acción
            confirm = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
            if confirm != 'SI':
                print("❌ Operación cancelada")
                return False
            
            # Eliminar todas las plantillas
            self.fingerprint.clearDatabase()
            print("✅ Base de datos del sensor limpiada")
            return True
            
        except Exception as e:
            print(f"❌ Error limpiando sensor: {e}")
            return False
    
    def upload_fingerprint_to_sensor(self, position: int, fingerprint_data: bytes, person_name: str) -> bool:
        """Sube una huella de la base de datos al sensor"""
        if not self.connected:
            print("❌ Sensor no conectado")
            return False
        
        try:
            print(f"📤 Subiendo huella de {person_name} a posición {position}...")
            
            # Importar las constantes necesarias
            from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
            
            # Cargar la huella en el buffer
            self.fingerprint.uploadCharacteristics(FINGERPRINT_CHARBUFFER1, fingerprint_data)
            
            # Guardar en la posición especificada
            self.fingerprint.storeTemplate(position, FINGERPRINT_CHARBUFFER1)
            
            print(f"✅ Huella de {person_name} subida exitosamente a posición {position}")
            return True
            
        except Exception as e:
            print(f"❌ Error subiendo huella de {person_name}: {e}")
            return False
    
    def sync_database_to_sensor(self):
        """Sincroniza todas las huellas de la base de datos al sensor"""
        if not self.connected:
            print("❌ Sensor no conectado")
            return False
        
        try:
            print("\n🔄 SINCRONIZANDO BASE DE DATOS CON SENSOR...")
            print("-" * 50)
            
            # Obtener información del sensor
            sensor_info = self.get_sensor_info()
            if not sensor_info:
                return False
            
            # Obtener huellas de la base de datos
            personal_with_fingerprints = get_personal_with_fingerprints()
            if not personal_with_fingerprints:
                print("❌ No hay huellas en la base de datos")
                return False
            
            print(f"\n📋 Encontradas {len(personal_with_fingerprints)} huellas en la base de datos")
            
            # Verificar capacidad del sensor
            if len(personal_with_fingerprints) > sensor_info['capacity']:
                print(f"❌ Error: El sensor solo puede almacenar {sensor_info['capacity']} huellas")
                print(f"   Pero hay {len(personal_with_fingerprints)} en la base de datos")
                return False
            
            # Limpiar sensor si es necesario
            if sensor_info['template_count'] > 0:
                print(f"\n⚠️  El sensor tiene {sensor_info['template_count']} huellas existentes")
                if not self.clear_sensor_database():
                    return False
            
            # Subir cada huella al sensor
            print(f"\n📤 Subiendo {len(personal_with_fingerprints)} huellas al sensor...")
            success_count = 0
            
            for i, person in enumerate(personal_with_fingerprints):
                if person['huella_digital']:
                    position = i + 1  # Posiciones del sensor empiezan en 1
                    person_name = f"{person['nombres']} {person['apellidos']}"
                    
                    if self.upload_fingerprint_to_sensor(position, person['huella_digital'], person_name):
                        success_count += 1
                        print(f"   ✅ {i+1}/{len(personal_with_fingerprints)}: {person_name}")
                    else:
                        print(f"   ❌ {i+1}/{len(personal_with_fingerprints)}: {person_name}")
                    
                    # Pequeña pausa entre subidas
                    time.sleep(0.5)
            
            print(f"\n🎯 SINCRONIZACIÓN COMPLETADA:")
            print(f"   • Huellas subidas exitosamente: {success_count}/{len(personal_with_fingerprints)}")
            
            if success_count == len(personal_with_fingerprints):
                print("✅ Todas las huellas sincronizadas correctamente")
                print("\n💡 Ahora el sensor debería reconocer las huellas registradas")
                return True
            else:
                print("⚠️  Algunas huellas no se pudieron sincronizar")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la sincronización: {e}")
            return False
    
    def test_fingerprint_recognition(self):
        """Prueba el reconocimiento de huellas después de la sincronización"""
        if not self.connected:
            print("❌ Sensor no conectado")
            return False
        
        try:
            print("\n🧪 PROBANDO RECONOCIMIENTO DE HUELLAS...")
            print("-" * 50)
            print("👆 Coloque su dedo en el sensor para probar...")
            
            # Importar las constantes necesarias
            from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
            
            # Esperar hasta que se detecte una huella
            while not self.fingerprint.readImage():
                time.sleep(0.1)
            
            print("✅ Huella detectada, procesando...")
            
            # Convertir la imagen a características
            self.fingerprint.convertImage(FINGERPRINT_CHARBUFFER1)
            
            # Buscar la huella en la base de datos del sensor
            result = self.fingerprint.searchTemplate()
            position_number = result[0]
            accuracy_score = result[1]
            
            if position_number == -1:
                print("❌ Huella no encontrada en el sensor")
                return False
            
            if accuracy_score < DEFAULT_THRESHOLD:
                print(f"❌ Calidad insuficiente (score: {accuracy_score})")
                return False
            
            print(f"✅ Huella reconocida exitosamente!")
            print(f"   • Posición en sensor: {position_number}")
            print(f"   • Score de calidad: {accuracy_score}")
            
            # Obtener información de la persona
            personal_with_fingerprints = get_personal_with_fingerprints()
            if position_number <= len(personal_with_fingerprints):
                person = personal_with_fingerprints[position_number - 1]
                print(f"   • Usuario: {person['nombres']} {person['apellidos']}")
                print(f"   • Tipo: {person['tipo_personal_nombre']}")
                print(f"   • Documento: {person['documento_tipo']} {person['documento_numero']}")
                
                # Registrar acceso exitoso
                log_access(
                    person['id'], 
                    'ENTRADA', 
                    f"Acceso biométrico exitoso desde sensor - Score: {accuracy_score}"
                )
                
                return True
            else:
                print("❌ Error: Posición no válida")
                return False
                
        except Exception as e:
            print(f"❌ Error probando reconocimiento: {e}")
            return False

def main():
    """Función principal"""
    print("🔄 SINCRONIZADOR DE HUELLAS - Base de Datos ↔ Sensor Físico")
    print("=" * 70)
    
    # Crear sincronizador
    synchronizer = FingerprintSynchronizer()
    
    try:
        # Conectar al sensor
        if not synchronizer.connect():
            print("\n❌ No se pudo conectar al sensor")
            print("\n💡 SOLUCIONES:")
            print("   1. Verifica que el sensor esté conectado al puerto COM3")
            print("   2. Asegúrate de que el sensor esté encendido")
            print("   3. Instala pyfingerprint: pip install pyfingerprint")
            print("   4. Verifica que no haya otro programa usando el puerto")
            return
        
        # Mostrar información del sensor
        synchronizer.get_sensor_info()
        
        # Sincronizar base de datos con sensor
        if synchronizer.sync_database_to_sensor():
            print("\n🎉 ¡SINCRONIZACIÓN EXITOSA!")
            print("\n💡 Ahora puedes probar el reconocimiento:")
            
            # Preguntar si quiere probar
            test = input("\n¿Quieres probar el reconocimiento ahora? (s/n): ").lower()
            if test in ['s', 'si', 'y', 'yes']:
                synchronizer.test_fingerprint_recognition()
        else:
            print("\n❌ La sincronización falló")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        synchronizer.disconnect()

if __name__ == "__main__":
    main()
