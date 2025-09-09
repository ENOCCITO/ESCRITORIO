#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_scanner_connection.py
- Prueba específica para verificar la conexión del lector biométrico
- Diagnostica problemas de conexión y puertos
"""

import tkinter as tk
from biometric_scanner import BiometricScanner

def test_scanner_connection():
    """Prueba la conexión del lector biométrico"""
    print("🔌 PRUEBA DE CONEXIÓN DEL LECTOR BIOMÉTRICO")
    print("=" * 60)
    
    try:
        # Crear instancia del lector
        scanner = BiometricScanner()
        
        print("✅ Instancia del lector creada")
        print("🔌 Intentando conectar al lector biométrico...")
        print("   - Esto puede tomar unos segundos...")
        print("   - El sistema probará múltiples puertos y baudrates")
        
        # Intentar conectar
        if scanner.connect():
            print("✅ ¡CONEXIÓN EXITOSA!")
            print("   - El lector biométrico está conectado y listo")
            print("   - Puedes usar el sistema de registro de huellas")
            
            # Probar funcionalidad básica
            print("\n🧪 Probando funcionalidad básica...")
            try:
                # Verificar que el sensor responde
                if scanner.sensor and scanner.connected:
                    print("✅ Sensor responde correctamente")
                    print("✅ Sistema listo para escanear huellas")
                else:
                    print("⚠️ Sensor no responde correctamente")
            except Exception as e:
                print(f"⚠️ Error probando sensor: {e}")
            
            # Desconectar
            scanner.disconnect()
            print("🔌 Lector desconectado correctamente")
            
        else:
            print("❌ ¡CONEXIÓN FALLIDA!")
            print("   - El lector biométrico no se pudo conectar")
            print("\n🔧 POSIBLES SOLUCIONES:")
            print("   1. Verifique que el lector esté conectado por USB")
            print("   2. Compruebe que el puerto COM esté disponible")
            print("   3. Instale los drivers del lector")
            print("   4. Asegúrese de que el lector esté encendido")
            print("   5. Pruebe con un cable USB diferente")
            print("   6. Verifique que no haya otros programas usando el puerto")
            
            # Mostrar información del sistema
            print("\n📊 INFORMACIÓN DEL SISTEMA:")
            try:
                import serial.tools.list_ports
                ports = serial.tools.list_ports.comports()
                if ports:
                    print("   Puertos COM disponibles:")
                    for port in ports:
                        print(f"   - {port.device}: {port.description}")
                else:
                    print("   No se encontraron puertos COM")
            except Exception as e:
                print(f"   Error listando puertos: {e}")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

def test_with_gui():
    """Prueba con interfaz gráfica"""
    print("\n🖥️ INICIANDO PRUEBA CON INTERFAZ GRÁFICA")
    print("=" * 60)
    
    try:
        # Crear ventana de prueba
        root = tk.Tk()
        root.title("Prueba - Conexión del Lector Biométrico")
        root.geometry("500x400")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🔌 PRUEBA DE CONEXIÓN",
            font=("Segoe UI", 18, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Esta prueba verifica la conexión del lector biométrico:

✅ Prueba múltiples puertos COM
✅ Prueba diferentes baudrates
✅ Verifica la respuesta del sensor
✅ Muestra información de diagnóstico
        """
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=("Segoe UI", 11),
            fg="#cccccc",
            bg="#1a1a2e",
            justify="left"
        )
        info_label.pack(pady=(0, 20))
        
        # Botón para probar conexión
        test_btn = tk.Button(
            main_frame,
            text="🔌 PROBAR CONEXIÓN",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: test_scanner_connection()
        )
        test_btn.pack(pady=20)
        
        # Botón de salir
        exit_btn = tk.Button(
            main_frame,
            text="❌ SALIR",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            activeforeground="#ffffff",
            activebackground="#ff5252",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=root.destroy
        )
        exit_btn.pack(side="bottom", pady=(20, 0))
        
        print("✅ Ventana de prueba creada")
        print("   - Haz clic en 'PROBAR CONEXIÓN'")
        print("   - Revisa la consola para ver los resultados")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CONEXIÓN DEL LECTOR")
    print("=" * 70)
    
    try:
        # Prueba básica
        test_scanner_connection()
        
        # Preguntar si quiere prueba con GUI
        print("\n" + "="*60)
        response = input("¿Desea ejecutar la prueba con interfaz gráfica? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            test_with_gui()
        
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
