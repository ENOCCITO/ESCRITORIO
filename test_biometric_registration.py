#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_biometric_registration.py
- Prueba completa del sistema de registro biométrico
- Verificación de lector biométrico y base de datos
"""

import tkinter as tk
from biometric_scanner import biometric_scanner
from fingerprint_registration_interface import show_fingerprint_registration_interface
from desktop_alerts import desktop_alert_system

def test_biometric_scanner():
    """Prueba el lector biométrico"""
    print("🔬 PRUEBA DEL LECTOR BIOMÉTRICO")
    print("=" * 50)
    
    try:
        # Probar conexión
        print("🔌 Conectando al lector biométrico...")
        if biometric_scanner.connect():
            print("✅ Lector biométrico conectado correctamente")
            
            # Probar escaneo
            print("👆 Probando escaneo de huella...")
            print("   Coloque su dedo en el lector cuando esté listo...")
            
            fingerprint_data = biometric_scanner.scan_fingerprint(timeout=10)
            if fingerprint_data:
                print(f"✅ Huella escaneada exitosamente ({len(fingerprint_data)} bytes)")
                
                # Probar guardado en BD (simulado)
                print("💾 Probando guardado en base de datos...")
                success = biometric_scanner.save_fingerprint_to_db(1, fingerprint_data)
                if success:
                    print("✅ Huella guardada en base de datos")
                else:
                    print("❌ Error guardando en base de datos")
            else:
                print("❌ No se pudo escanear la huella")
            
            # Desconectar
            biometric_scanner.disconnect()
            print("🔌 Lector biométrico desconectado")
            
        else:
            print("❌ No se pudo conectar al lector biométrico")
            print("   Verifique que el dispositivo esté conectado y configurado correctamente")
            
    except Exception as e:
        print(f"❌ Error en prueba del lector: {e}")
        import traceback
        traceback.print_exc()

def test_database_integration():
    """Prueba la integración con la base de datos"""
    print("\n💾 PRUEBA DE INTEGRACIÓN CON BASE DE DATOS")
    print("=" * 50)
    
    try:
        from db_utils import get_personal_by_id
        
        # Probar consulta de personal
        print("👤 Consultando personal...")
        person = get_personal_by_id(1)
        if person:
            print(f"✅ Personal encontrado: {person['nombres']} {person['apellidos']}")
            print(f"   ID: {person['id']}")
            print(f"   Tipo: {person['tipo_personal_nombre']}")
            print(f"   Tiene huella: {'Sí' if person.get('huella_digital') else 'No'}")
        else:
            print("❌ No se encontró personal con ID 1")
            
    except Exception as e:
        print(f"❌ Error en prueba de base de datos: {e}")
        import traceback
        traceback.print_exc()

def test_registration_interface():
    """Prueba la interfaz de registro"""
    print("\n🖥️ PRUEBA DE INTERFAZ DE REGISTRO")
    print("=" * 50)
    
    try:
        # Crear ventana principal de prueba
        root = tk.Tk()
        root.title("Prueba - Sistema de Registro Biométrico")
        root.geometry("400x300")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🧪 PRUEBA DE REGISTRO BIOMÉTRICO",
            font=("Segoe UI", 16, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Esta prueba verifica:

✅ Lector biométrico
✅ Base de datos
✅ Interfaz de registro
✅ Alertas del sistema
        """
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#1a1a2e",
            justify="left"
        )
        info_label.pack(pady=(0, 20))
        
        # Botones de prueba
        buttons_frame = tk.Frame(main_frame, bg="#1a1a2e")
        buttons_frame.pack(pady=10)
        
        def test_scanner():
            test_biometric_scanner()
        
        def test_database():
            test_database_integration()
        
        def test_interface():
            show_fingerprint_registration_interface(root)
        
        def test_alerts():
            desktop_alert_system.show_access_granted_alert("test", "Prueba de alerta exitosa")
        
        # Botón para probar lector
        scanner_btn = tk.Button(
            buttons_frame,
            text="🔬 PROBAR LECTOR",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=test_scanner
        )
        scanner_btn.pack(side="left", padx=5)
        
        # Botón para probar BD
        db_btn = tk.Button(
            buttons_frame,
            text="💾 PROBAR BD",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#4caf50",
            activeforeground="#ffffff",
            activebackground="#45a049",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=test_database
        )
        db_btn.pack(side="left", padx=5)
        
        # Botón para probar interfaz
        interface_btn = tk.Button(
            buttons_frame,
            text="🖥️ PROBAR INTERFAZ",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#ffa726",
            activeforeground="#ffffff",
            activebackground="#ff9800",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=test_interface
        )
        interface_btn.pack(side="left", padx=5)
        
        # Botón para probar alertas
        alert_btn = tk.Button(
            buttons_frame,
            text="🚨 PROBAR ALERTAS",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#9c27b0",
            activeforeground="#ffffff",
            activebackground="#8e24aa",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=test_alerts
        )
        alert_btn.pack(side="left", padx=5)
        
        # Botón de salir
        exit_btn = tk.Button(
            main_frame,
            text="❌ SALIR",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            activeforeground="#ffffff",
            activebackground="#ff5252",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=root.destroy
        )
        exit_btn.pack(side="bottom", pady=(20, 0))
        
        print("✅ Ventana de prueba creada")
        print("   - Usa los botones para probar cada componente")
        print("   - La interfaz de registro se abrirá en una nueva ventana")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en prueba de interfaz: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA BIOMÉTRICO")
    print("=" * 60)
    
    try:
        # Ejecutar todas las pruebas
        test_biometric_scanner()
        test_database_integration()
        
        # Preguntar si quiere probar la interfaz
        print("\n" + "=" * 60)
        response = input("¿Deseas probar la interfaz de registro? (s/n): ").lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_registration_interface()
        else:
            print("⏭️  Saltando prueba de interfaz")
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
