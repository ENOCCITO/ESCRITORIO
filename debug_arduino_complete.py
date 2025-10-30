#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
debug_arduino_complete.py
- Diagnóstico completo del Arduino
"""

import serial
import time

def debug_arduino_complete():
    """Diagnóstico completo del Arduino"""
    try:
        print("🔍 DIAGNÓSTICO COMPLETO DEL ARDUINO")
        print("=" * 50)
        
        # 1. Conectar
        print("1️⃣ Conectando al Arduino...")
        ser = serial.Serial('COM4', 115200, timeout=5)
        time.sleep(3)
        print("✅ Arduino conectado")
        
        # 2. Limpiar buffer
        print("\n2️⃣ Limpiando buffer...")
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(1)
        
        # 3. Enviar STATUS
        print("\n3️⃣ Enviando STATUS...")
        ser.write(b"STATUS\n")
        ser.flush()
        time.sleep(2)
        
        print("📥 Respuesta STATUS:")
        status_response = ""
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"  {line}")
                status_response += line + "\n"
        
        # 4. Enviar OPEN 90 5
        print("\n4️⃣ Enviando OPEN 90 5...")
        ser.write(b"OPEN 90 5\n")
        ser.flush()
        time.sleep(3)
        
        print("📥 Respuesta OPEN:")
        open_response = ""
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"  {line}")
                open_response += line + "\n"
        
        # 5. Enviar HOME
        print("\n5️⃣ Enviando HOME...")
        ser.write(b"HOME\n")
        ser.flush()
        time.sleep(3)
        
        print("📥 Respuesta HOME:")
        home_response = ""
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"  {line}")
                home_response += line + "\n"
        
        ser.close()
        
        # 6. Análisis
        print("\n6️⃣ ANÁLISIS:")
        print(f"STATUS responde: {'✅' if 'ESTADO DEL MOTOR' in status_response else '❌'}")
        print(f"OPEN responde: {'✅' if 'Movimiento completado' in open_response else '❌'}")
        print(f"HOME responde: {'✅' if 'HOME completado' in home_response else '❌'}")
        
        if 'Movimiento completado' in open_response:
            print("\n🎉 ¡ARDUINO FUNCIONANDO CORRECTAMENTE!")
            return True
        else:
            print("\n❌ ARDUINO NO ESTÁ FUNCIONANDO")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    debug_arduino_complete()
