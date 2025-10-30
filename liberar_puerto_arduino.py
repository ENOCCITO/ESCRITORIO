#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
liberar_puerto_arduino.py
- Script para liberar el puerto Arduino y probar la conexión real
"""

import serial
import time
import serial.tools.list_ports
import subprocess
import sys

def kill_arduino_processes():
    """Mata procesos que puedan estar usando el puerto Arduino"""
    try:
        # Buscar procesos que usen COM4
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'COM4' in line:
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    try:
                        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                        print(f"✅ Proceso {pid} terminado")
                    except:
                        pass
    except Exception as e:
        print(f"⚠️ No se pudieron terminar procesos: {e}")

def force_release_port():
    """Fuerza la liberación del puerto COM4"""
    try:
        print("🔓 Intentando liberar puerto COM4...")
        
        # Método 1: Intentar conectar y cerrar inmediatamente
        try:
            ser = serial.Serial('COM4', 115200, timeout=1)
            ser.close()
            time.sleep(2)
            print("✅ Puerto COM4 liberado (método 1)")
            return True
        except:
            pass
        
        # Método 2: Usar diferentes configuraciones
        try:
            ser = serial.Serial('COM4', 9600, timeout=1)
            ser.close()
            time.sleep(2)
            print("✅ Puerto COM4 liberado (método 2)")
            return True
        except:
            pass
            
        return False
        
    except Exception as e:
        print(f"❌ Error liberando puerto: {e}")
        return False

def test_arduino_real():
    """Prueba la conexión real al Arduino"""
    try:
        print("🔌 Probando conexión REAL al Arduino...")
        ser = serial.Serial('COM4', 115200, timeout=5)
        time.sleep(3)  # Esperar inicialización del Arduino
        
        # Enviar comando STATUS
        print("📤 Enviando comando STATUS...")
        ser.write(b"STATUS\n")
        ser.flush()
        
        # Leer respuesta
        time.sleep(2)
        response = ""
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response += line + "\n"
                print(f"📥 Arduino: {line}")
        
        ser.close()
        
        if "ARDUINO_NEMA17_READY" in response or "ESTADO DEL MOTOR" in response:
            print("✅ ARDUINO REAL FUNCIONANDO CORRECTAMENTE")
            return True
        else:
            print("⚠️ Arduino conectado pero respuesta inesperada")
            print(f"Respuesta recibida: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando al Arduino real: {e}")
        return False

def main():
    print("🤖 LIBERADOR DE PUERTO ARDUINO - VERSIÓN REAL")
    print("=" * 60)
    
    # 1. Matar procesos que usen COM4
    print("🔪 Terminando procesos que usen COM4...")
    kill_arduino_processes()
    time.sleep(3)
    
    # 2. Intentar liberar el puerto
    print("🔓 Liberando puerto COM4...")
    if force_release_port():
        print("✅ Puerto liberado exitosamente")
    else:
        print("⚠️ No se pudo liberar completamente")
    
    # 3. Esperar un momento
    print("⏳ Esperando 5 segundos...")
    time.sleep(5)
    
    # 4. Probar conexión real
    print("🧪 Probando conexión REAL al Arduino...")
    if test_arduino_real():
        print("\n🎉 ¡ARDUINO REAL LISTO!")
        print("💡 Ahora ejecuta: python main.py")
        return True
    else:
        print("\n❌ Arduino no responde")
        print("💡 Verifica:")
        print("   • Arduino IDE completamente cerrado")
        print("   • Código cargado en Arduino")
        print("   • Cable USB conectado")
        print("   • Reinicia el Arduino")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ ¡ARDUINO REAL FUNCIONANDO!")
        print("🚀 El sistema usará el motor físico")
    else:
        print("\n❌ Revisa la configuración del Arduino")
