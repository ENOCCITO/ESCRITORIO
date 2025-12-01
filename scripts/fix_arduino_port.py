#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_arduino_port.py
- Script para liberar el puerto Arduino y probar la conexión
"""

import serial
import time
import serial.tools.list_ports

def find_arduino_port():
    """Encuentra el puerto del Arduino"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB" in port.description:
            return port.device
    return None

def force_close_port(port_name):
    """Intenta cerrar cualquier conexión al puerto"""
    try:
        # Intentar conectar y cerrar inmediatamente
        ser = serial.Serial(port_name, 115200, timeout=1)
        ser.close()
        time.sleep(1)
        print(f"✅ Puerto {port_name} liberado")
        return True
    except Exception as e:
        print(f"⚠️ No se pudo liberar {port_name}: {e}")
        return False

def test_arduino_connection(port_name):
    """Prueba la conexión al Arduino"""
    try:
        print(f"🔌 Probando conexión a {port_name}...")
        ser = serial.Serial(port_name, 115200, timeout=3)
        time.sleep(2)  # Esperar inicialización
        
        # Enviar comando STATUS
        ser.write(b"STATUS\n")
        ser.flush()
        
        # Leer respuesta
        time.sleep(1)
        response = ""
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response += line + "\n"
                print(f"📥 Arduino: {line}")
        
        ser.close()
        
        if "ARDUINO_NEMA17_READY" in response or "ESTADO DEL MOTOR" in response:
            print("✅ Arduino funcionando correctamente")
            return True
        else:
            print("⚠️ Arduino conectado pero respuesta inesperada")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando a {port_name}: {e}")
        return False

def main():
    print("🔧 REPARADOR DE CONEXIÓN ARDUINO")
    print("=" * 50)
    
    # 1. Encontrar puerto Arduino
    arduino_port = find_arduino_port()
    if not arduino_port:
        print("❌ No se encontró Arduino conectado")
        return False
    
    print(f"🔍 Arduino encontrado en: {arduino_port}")
    
    # 2. Intentar liberar el puerto
    print(f"🔓 Liberando puerto {arduino_port}...")
    force_close_port(arduino_port)
    
    # 3. Esperar un momento
    print("⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    # 4. Probar conexión
    print(f"🧪 Probando conexión...")
    if test_arduino_connection(arduino_port):
        print("\n🎉 ¡ARDUINO LISTO PARA USAR!")
        print(f"💡 Usa el puerto: {arduino_port}")
        return True
    else:
        print("\n❌ Arduino no responde correctamente")
        print("💡 Verifica:")
        print("   • Código cargado en Arduino")
        print("   • Cable USB conectado")
        print("   • Arduino IDE cerrado")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Ahora puedes ejecutar: python main.py")
    else:
        print("\n❌ Revisa la configuración del Arduino")
