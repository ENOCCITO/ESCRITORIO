#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biometric_scanner.py
- Módulo para manejo del lector biométrico real
- Integración con el sistema de registro de huellas
"""

import time
import threading
from typing import Optional, Tuple, Any
from datetime import datetime

from utils import _import_pyfingerprint, db_connect, log_file
from desktop_alerts import desktop_alert_system

class BiometricScanner:
    """Manejador del lector biométrico para registro de huellas"""
    
    def __init__(self):
        self.pyfingerprint = None
        self.sensor = None
        self.connected = False
        self.scanning = False
        
    def connect(self) -> bool:
        """Conecta al lector biométrico usando la misma lógica que main.py"""
        try:
            print("🔌 Intentando conectar al lector biométrico...")
            
            # Importar pyfingerprint
            self.pyfingerprint, error = _import_pyfingerprint()
            if not self.pyfingerprint:
                print(f"❌ Error importando pyfingerprint: {error}")
                return False
            
            PyFingerprint, F1, F2 = self.pyfingerprint
            
            # Usar la misma lógica que main.py - probar COM3 primero
            ports_to_try = ["COM3", "COM1", "COM2", "COM4", "COM5", "COM6", "COM7", "COM8"]
            baudrates_to_try = [57600, 9600, 19200, 38400, 115200]
            
            print(f"🔌 Probando conexión usando la lógica de main.py...")
            
            for port in ports_to_try:
                for baudrate in baudrates_to_try:
                    try:
                        print(f"🔌 Probando puerto: {port}, baudrate: {baudrate}")
                        
                        # Usar la misma lógica exacta que main.py
                        self.sensor = PyFingerprint(port.strip(), baudrate, 0xFFFFFFFF, 0x00000000)
                        
                        print("🔌 Verificando contraseña del sensor...")
                        # Verificar conexión usando la misma lógica
                        if self.sensor.verifyPassword():
                            self.connected = True
                            print(f"✅ Lector biométrico conectado en {port} con baudrate {baudrate}")
                            log_file(f"✅ Lector biométrico conectado en {port} con baudrate {baudrate}")
                            return True
                        else:
                            print(f"❌ Contraseña incorrecta en {port}")
                            
                    except Exception as e:
                        print(f"⚠️ Error en {port}: {e}")
                        continue
            
            print("❌ No se pudo conectar al lector biométrico en ningún puerto")
            return False
            
        except Exception as e:
            print(f"❌ Error conectando al lector biométrico: {e}")
            print(f"❌ Tipo de error: {type(e).__name__}")
            log_file(f"❌ Error conectando al lector biométrico: {e}")
            return False
    
    def test_com3_connection(self) -> bool:
        """Prueba específicamente la conexión en COM3 con la lógica de main.py"""
        try:
            print("🔌 Probando conexión específica en COM3...")
            
            # Importar pyfingerprint
            self.pyfingerprint, error = _import_pyfingerprint()
            if not self.pyfingerprint:
                print(f"❌ Error importando pyfingerprint: {error}")
                return False
            
            PyFingerprint, F1, F2 = self.pyfingerprint
            
            # Probar específicamente COM3 con 57600 (como en main.py)
            try:
                print("🔌 Conectando a COM3 con baudrate 57600...")
                self.sensor = PyFingerprint("COM3", 57600, 0xFFFFFFFF, 0x00000000)
                
                print("🔌 Verificando contraseña del sensor...")
                if self.sensor.verifyPassword():
                    self.connected = True
                    print("✅ ¡CONEXIÓN EXITOSA EN COM3!")
                    log_file("✅ Lector biométrico conectado en COM3 con baudrate 57600")
                    return True
                else:
                    print("❌ Contraseña incorrecta en COM3")
                    return False
                    
            except Exception as e:
                print(f"❌ Error conectando a COM3: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error en prueba de COM3: {e}")
            return False
    
    def disconnect(self):
        """Desconecta el lector biométrico"""
        try:
            if self.sensor:
                self.sensor = None
            self.connected = False
            print("🔌 Lector biométrico desconectado")
            log_file("🔌 Lector biométrico desconectado")
        except Exception as e:
            print(f"⚠️ Error desconectando lector: {e}")
    
    def scan_fingerprint(self, timeout: int = 30) -> Optional[bytes]:
        """
        Escanea una huella digital del lector
        
        Args:
            timeout: Tiempo máximo de espera en segundos
            
        Returns:
            bytes: Datos de la huella escaneada o None si hay error
        """
        if not self.connected or not self.sensor:
            print("❌ Lector biométrico no conectado")
            return None
        
        if self.scanning:
            print("⚠️ Ya hay un escaneo en progreso")
            return None
        
        try:
            self.scanning = True
            print("👆 Iniciando escaneo de huella digital...")
            log_file("👆 Iniciando escaneo de huella digital...")
            
            # Esperar a que se coloque el dedo
            print("👆 Coloque su dedo en el lector...")
            while not self.sensor.readImage():
                time.sleep(0.1)
                timeout -= 0.1
                if timeout <= 0:
                    print("⏰ Tiempo de espera agotado")
                    return None
            
            print("✅ Huella capturada, procesando...")
            
            # Convertir la imagen a características
            self.sensor.convertImage(0x01)
            
            # Obtener las características
            characteristics = self.sensor.downloadCharacteristics(0x01)
            
            # Convertir lista a bytes
            fingerprint_data = bytes(characteristics)
            
            print(f"✅ Huella procesada exitosamente ({len(fingerprint_data)} bytes)")
            log_file(f"✅ Huella procesada exitosamente ({len(fingerprint_data)} bytes)")
            
            return fingerprint_data
            
        except Exception as e:
            error_msg = f"Error escaneando huella: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            return None
            
        finally:
            self.scanning = False
    
    def save_fingerprint_to_db(self, person_id: int, fingerprint_data: bytes) -> bool:
        """
        Guarda la huella digital en la base de datos
        
        Args:
            person_id: ID de la persona
            fingerprint_data: Datos binarios de la huella
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            print(f"💾 Guardando huella para persona ID {person_id}...")
            print(f"💾 Tamaño de datos: {len(fingerprint_data)} bytes")
            
            # Verificar que la persona existe
            check_query = "SELECT id, nombres, apellidos FROM personal WHERE id = %s AND activo = 1"
            
            with db_connect() as cnx:
                cur = cnx.cursor()
                
                # Verificar que la persona existe
                cur.execute(check_query, (person_id,))
                person = cur.fetchone()
                
                if not person:
                    print(f"❌ No se encontró persona con ID {person_id}")
                    return False
                
                print(f"✅ Persona encontrada: {person[1]} {person[2]}")
                
                # Actualizar la huella
                update_query = """
                    UPDATE personal 
                    SET huella_digital = %s, 
                        fecha_registro_huella = NOW(),
                        updated_at = NOW()
                    WHERE id = %s AND activo = 1
                """
                
                # Ejecutar la actualización
                cur.execute(update_query, (fingerprint_data, person_id))
                cnx.commit()
                
                if cur.rowcount > 0:
                    print(f"✅ Huella guardada exitosamente para persona ID {person_id}")
                    log_file(f"✅ Huella guardada para persona ID {person_id}")
                    
                    # Verificar que realmente se guardó
                    cur.execute("SELECT huella_digital FROM personal WHERE id = %s", (person_id,))
                    result = cur.fetchone()
                    
                    if result and result[0]:
                        print(f"✅ Verificación exitosa: {len(result[0])} bytes guardados")
                        return True
                    else:
                        print("❌ Los datos no se guardaron correctamente")
                        return False
                else:
                    print(f"❌ No se pudo actualizar la huella para persona ID {person_id}")
                    return False
                    
        except Exception as e:
            error_msg = f"Error guardando huella en BD: {e}"
            print(f"❌ {error_msg}")
            print(f"❌ Tipo de error: {type(e).__name__}")
            print(f"❌ Detalles del error: {str(e)}")
            log_file(f"❌ {error_msg}")
            log_file(f"❌ Tipo: {type(e).__name__}")
            log_file(f"❌ Detalles: {str(e)}")
            return False
    
    def verify_fingerprint_exists(self, person_id: int) -> bool:
        """
        Verifica si una persona ya tiene huella registrada
        
        Args:
            person_id: ID de la persona
            
        Returns:
            bool: True si ya tiene huella registrada
        """
        try:
            query = """
                SELECT huella_digital 
                FROM personal 
                WHERE id = %s AND activo = 1 AND huella_digital IS NOT NULL
            """
            
            with db_connect() as cnx:
                cur = cnx.cursor()
                cur.execute(query, (person_id,))
                result = cur.fetchone()
                
                return result is not None and result[0] is not None
                
        except Exception as e:
            print(f"❌ Error verificando huella existente: {e}")
            return False
    
    def register_fingerprint_for_person(self, person_id: int, person_name: str) -> Tuple[bool, str]:
        """
        Registra una huella para una persona específica
        
        Args:
            person_id: ID de la persona
            person_name: Nombre de la persona
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Verificar si ya tiene huella
            if self.verify_fingerprint_exists(person_id):
                return False, f"{person_name} ya tiene una huella registrada"
            
            # Escanear huella
            fingerprint_data = self.scan_fingerprint()
            if not fingerprint_data:
                return False, "No se pudo escanear la huella"
            
            # Guardar en base de datos
            if self.save_fingerprint_to_db(person_id, fingerprint_data):
                return True, f"Huella registrada exitosamente para {person_name}"
            else:
                return False, "Error guardando la huella en la base de datos"
                
        except Exception as e:
            error_msg = f"Error registrando huella: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            return False, error_msg
    
    def update_fingerprint_for_person(self, person_id: int, person_name: str) -> Tuple[bool, str]:
        """
        Actualiza una huella para una persona específica
        
        Args:
            person_id: ID de la persona
            person_name: Nombre de la persona
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Escanear nueva huella
            fingerprint_data = self.scan_fingerprint()
            if not fingerprint_data:
                return False, "No se pudo escanear la nueva huella"
            
            # Guardar en base de datos (actualizar)
            if self.save_fingerprint_to_db(person_id, fingerprint_data):
                return True, f"Huella actualizada exitosamente para {person_name}"
            else:
                return False, "Error actualizando la huella en la base de datos"
                
        except Exception as e:
            error_msg = f"Error actualizando huella: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            return False, error_msg
    
    def test_database_save(self, person_id: int) -> Tuple[bool, str]:
        """
        Prueba el guardado en la base de datos con datos de prueba
        
        Args:
            person_id: ID de la persona a probar
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            print(f"🧪 Probando guardado en BD para persona ID {person_id}...")
            
            # Crear datos de prueba
            test_data = b"TEST_FINGERPRINT_DATA_" + str(person_id).encode() + b"_" + str(int(time.time())).encode()
            
            print(f"🧪 Datos de prueba creados: {len(test_data)} bytes")
            
            # Probar guardado
            if self.save_fingerprint_to_db(person_id, test_data):
                print("✅ Prueba de guardado exitosa")
                return True, "Prueba de guardado exitosa"
            else:
                print("❌ Prueba de guardado falló")
                return False, "Prueba de guardado falló"
                
        except Exception as e:
            error_msg = f"Error en prueba de BD: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg

# Instancia global del escáner biométrico
biometric_scanner = BiometricScanner()
