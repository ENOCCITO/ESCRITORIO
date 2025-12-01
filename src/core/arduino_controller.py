#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arduino_controller.py
- Controlador mejorado para Arduino con motor NEMA17
- Integra con la base de datos para obtener grados de llaves
- Manejo de comunicación serial y control del dispensador
"""

import time
import threading
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT, DEFAULT_DWELL
from src.utils.db_utils import get_available_keys, get_environments, db_connect
from src.utils.utils import _import_serial, log_file

class ArduinoController:
    """Controlador para Arduino con motor NEMA17"""
    
    def __init__(self, port: str = ARDUINO_PORT_DEFAULT, baud: int = ARDUINO_BAUD_DEFAULT):
        self.port = port
        self.baud = baud
        self.connected = False
        self.serial_connection = None
        self.current_position = 0
        self.is_moving = False
        
    def connect(self) -> bool:
        """Conecta al Arduino por puerto serial"""
        try:
            serial, err = _import_serial()
            if not serial:
                print(f"❌ Error: PySerial no disponible: {err}")
                return False
            
            print(f"🔌 Conectando al Arduino en {self.port}...")
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=5.0
            )
            
            # Esperar a que Arduino esté listo
            time.sleep(2)
            
            # Verificar conexión
            if self._test_connection():
                self.connected = True
                print(f"✅ Arduino conectado en {self.port}")
                log_file(f"✅ Arduino conectado en {self.port}")
                return True
            else:
                print("❌ Error: No se pudo establecer comunicación con Arduino")
                return False
                
        except Exception as e:
            print(f"❌ Error conectando al Arduino: {e}")
            log_file(f"❌ Error conectando al Arduino: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del Arduino"""
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            self.connected = False
            print("🔌 Arduino desconectado")
            log_file("🔌 Arduino desconectado")
        except Exception as e:
            print(f"⚠️ Error desconectando Arduino: {e}")
    
    def _test_connection(self) -> bool:
        """Prueba la conexión con Arduino"""
        try:
            if not self.serial_connection:
                return False
            
            # Enviar comando de estado
            self._send_command("STATUS")
            response = self._read_response()
            
            if "ESTADO DEL MOTOR" in response:
                return True
            return False
            
        except Exception as e:
            print(f"⚠️ Error probando conexión: {e}")
            return False
    
    def _send_command(self, command: str) -> bool:
        """Envía comando al Arduino"""
        try:
            if not self.connected or not self.serial_connection:
                print("❌ Arduino no conectado")
                return False
            
            # Limpiar buffer de entrada
            self.serial_connection.reset_input_buffer()
            self.serial_connection.reset_output_buffer()
            
            # Enviar comando
            command_bytes = f"{command}\n".encode('utf-8')
            self.serial_connection.write(command_bytes)
            self.serial_connection.flush()
            
            print(f"📤 Comando enviado: {command}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando comando: {e}")
            return False
    
    def _read_response(self, timeout: float = 5.0) -> str:
        """Lee respuesta del Arduino"""
        try:
            if not self.connected or not self.serial_connection:
                return ""
            
            response = ""
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        response += line + "\n"
                        print(f"📥 Respuesta: {line}")
                time.sleep(0.1)
            
            return response
            
        except Exception as e:
            print(f"❌ Error leyendo respuesta: {e}")
            return ""
    
    def home_motor(self) -> bool:
        """Mueve el motor a posición inicial (0 grados)"""
        try:
            print("🏠 Enviando comando HOME...")
            if self._send_command("HOME"):
                response = self._read_response(10.0)
                if "HOME completado" in response:
                    self.current_position = 0
                    print("✅ Motor en posición inicial")
                    log_file("✅ Motor NEMA17 en posición inicial")
                    return True
                else:
                    print("❌ Error en comando HOME")
                    return False
            return False
            
        except Exception as e:
            print(f"❌ Error en HOME: {e}")
            return False
    
    def move_to_key_position(self, key_id: int, dwell_seconds: int = None) -> bool:
        """Mueve el motor a la posición de una llave específica"""
        try:
            # Obtener información de la llave desde la base de datos
            key_info = self._get_key_info(key_id)
            if not key_info:
                print(f"❌ Llave {key_id} no encontrada en la base de datos")
                return False
            
            degrees = key_info.get('angulo_grados', 0)
            if degrees is None or degrees < 0 or degrees > 360:
                print(f"❌ Ángulo inválido para llave {key_id}: {degrees}")
                return False
            
            # Usar tiempo por defecto si no se especifica
            if dwell_seconds is None:
                dwell_seconds = DEFAULT_DWELL
            
            print(f"🔑 Moviendo a llave {key_id} - Ángulo: {degrees}°")
            print(f"📋 Código: {key_info.get('codigo_llave', 'N/A')}")
            print(f"📝 Descripción: {key_info.get('descripcion', 'N/A')}")
            
            # Enviar comando al Arduino
            command = f"OPEN {degrees} {dwell_seconds}"
            if self._send_command(command):
                response = self._read_response(15.0)
                if "Movimiento completado" in response:
                    self.current_position = degrees
                    print(f"✅ Motor movido a {degrees}° - Llave {key_id} disponible")
                    log_file(f"✅ Motor movido a {degrees}° para llave {key_id}")
                    return True
                else:
                    print("❌ Error en movimiento del motor")
                    return False
            return False
            
        except Exception as e:
            print(f"❌ Error moviendo a llave {key_id}: {e}")
            return False
    
    def move_to_environment(self, environment_id: int, dwell_seconds: int = None) -> bool:
        """Mueve el motor a la posición de un ambiente específico"""
        try:
            # Obtener llaves del ambiente
            keys = self._get_keys_for_environment(environment_id)
            if not keys:
                print(f"❌ No hay llaves disponibles para ambiente {environment_id}")
                return False
            
            # Usar la primera llave disponible del ambiente
            key = keys[0]
            key_id = key['id']
            degrees = key.get('angulo_grados', 0)
            
            print(f"🏢 Moviendo a ambiente {environment_id} - Llave: {key['codigo_llave']}")
            print(f"📐 Ángulo: {degrees}°")
            
            return self.move_to_key_position(key_id, dwell_seconds)
            
        except Exception as e:
            print(f"❌ Error moviendo a ambiente {environment_id}: {e}")
            return False
    
    def get_motor_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del motor"""
        try:
            if self._send_command("STATUS"):
                response = self._read_response(5.0)
                
                status = {
                    'connected': self.connected,
                    'position': self.current_position,
                    'moving': self.is_moving,
                    'response': response
                }
                
                # Parsear información de la respuesta
                if "Posición actual:" in response:
                    try:
                        pos_line = [line for line in response.split('\n') if 'Posición actual:' in line][0]
                        pos_value = pos_line.split(':')[1].strip().split()[0]
                        status['position'] = int(pos_value)
                    except:
                        pass
                
                if "Estado:" in response:
                    try:
                        state_line = [line for line in response.split('\n') if 'Estado:' in line][0]
                        state_value = state_line.split(':')[1].strip()
                        status['moving'] = 'MOVIÉNDOSE' in state_value
                    except:
                        pass
                
                return status
            else:
                return {'connected': False, 'error': 'No se pudo obtener estado'}
                
        except Exception as e:
            print(f"❌ Error obteniendo estado: {e}")
            return {'connected': False, 'error': str(e)}
    
    def reset_motor(self) -> bool:
        """Resetea el motor a posición inicial"""
        try:
            print("🔄 Reseteando motor...")
            if self._send_command("RESET"):
                response = self._read_response(5.0)
                if "Motor reseteado" in response:
                    self.current_position = 0
                    self.is_moving = False
                    print("✅ Motor reseteado")
                    return True
            return False
            
        except Exception as e:
            print(f"❌ Error reseteando motor: {e}")
            return False
    
    def _get_key_info(self, key_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene información de una llave desde la base de datos"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                query = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE id = %s AND activo = 1
                """
                cur.execute(query, (key_id,))
                key = cur.fetchone()
                cur.close()
                return key
                
        except Exception as e:
            print(f"❌ Error obteniendo información de llave {key_id}: {e}")
            return None
    
    def _get_keys_for_environment(self, environment_id: int) -> list:
        """Obtiene llaves disponibles para un ambiente"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                query = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE ambiente_id = %s AND activo = 1 AND estado = 'DISPONIBLE'
                    ORDER BY codigo_llave
                """
                cur.execute(query, (environment_id,))
                keys = cur.fetchall()
                cur.close()
                return keys
                
        except Exception as e:
            print(f"❌ Error obteniendo llaves para ambiente {environment_id}: {e}")
            return []
    
    def show_available_keys_with_angles(self) -> None:
        """Muestra llaves disponibles con sus ángulos"""
        try:
            keys = get_available_keys()
            if not keys:
                print("ℹ️ No hay llaves disponibles")
                return
            
            print(f"\n🔑 LLAVES DISPONIBLES CON ÁNGULOS ({len(keys)}):")
            print("-" * 90)
            print(f"{'ID':<5} {'CÓDIGO':<15} {'DESCRIPCIÓN':<30} {'AMBIENTE':<15} {'ÁNGULO':<10} {'MÓDULO':<10}")
            print("-" * 90)
            
            for key in keys:
                ambiente = "N/A"
                if key['ambiente_id']:
                    environments = get_environments()
                    for env in environments:
                        if env['id'] == key['ambiente_id']:
                            ambiente = env['nombre'][:14]
                            break
                
                print(f"{key['id']:<5} {key['codigo_llave']:<15} {key['descripcion'][:29]:<30} {ambiente:<15} {key['angulo_grados']:<10} {key.get('modulo', 'N/A'):<10}")
            
        except Exception as e:
            print(f"❌ Error mostrando llaves: {e}")
    
    def test_motor_sequence(self) -> bool:
        """Prueba una secuencia completa del motor"""
        try:
            print("🧪 INICIANDO PRUEBA DEL MOTOR NEMA17")
            print("=" * 50)
            
            # 1. Home
            print("1️⃣ Enviando HOME...")
            if not self.home_motor():
                return False
            
            time.sleep(2)
            
            # 2. Mover a 90 grados
            print("2️⃣ Moviendo a 90 grados...")
            if self._send_command("OPEN 90 3"):
                response = self._read_response(10.0)
                if "Movimiento completado" not in response:
                    print("❌ Error en movimiento a 90°")
                    return False
            
            time.sleep(2)
            
            # 3. Mover a 180 grados
            print("3️⃣ Moviendo a 180 grados...")
            if self._send_command("OPEN 180 3"):
                response = self._read_response(10.0)
                if "Movimiento completado" not in response:
                    print("❌ Error en movimiento a 180°")
                    return False
            
            time.sleep(2)
            
            # 4. Volver a HOME
            print("4️⃣ Volviendo a HOME...")
            if not self.home_motor():
                return False
            
            print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
            return True
            
        except Exception as e:
            print(f"❌ Error en prueba del motor: {e}")
            return False


def main():
    """Función principal de demostración"""
    print("🤖 CONTROLADOR ARDUINO NEMA17 - Sistema de Llaves CEFA")
    print("=" * 60)
    
    # Crear controlador
    controller = ArduinoController()
    
    try:
        # Conectar al Arduino
        if not controller.connect():
            print("❌ No se pudo conectar al Arduino")
            print("💡 Verifica:")
            print("   • Puerto COM correcto en config.py")
            print("   • Arduino conectado y encendido")
            print("   • Código Arduino cargado")
            return
        
        # Mostrar estado inicial
        print("\n📊 ESTADO INICIAL DEL MOTOR")
        status = controller.get_motor_status()
        print(f"   • Conectado: {status.get('connected', False)}")
        print(f"   • Posición: {status.get('position', 'N/A')} grados")
        print(f"   • Moviéndose: {status.get('moving', False)}")
        
        # Mostrar llaves disponibles
        print("\n🔑 LLAVES DISPONIBLES EN LA BASE DE DATOS")
        controller.show_available_keys_with_angles()
        
        # Prueba del motor
        print("\n🧪 PRUEBA DEL MOTOR")
        if controller.test_motor_sequence():
            print("✅ Motor funcionando correctamente")
        else:
            print("❌ Error en prueba del motor")
        
        # Mostrar estado final
        print("\n📊 ESTADO FINAL DEL MOTOR")
        final_status = controller.get_motor_status()
        print(f"   • Posición final: {final_status.get('position', 'N/A')} grados")
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA")
        print("\n💡 Para usar en producción:")
        print("   1. Integra con el sistema principal")
        print("   2. Usa move_to_key_position() para llaves específicas")
        print("   3. Usa move_to_environment() para ambientes")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()
