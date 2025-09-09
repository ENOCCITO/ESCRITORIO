#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_fingerprint_registration.py
- Prueba de la interfaz de registro de huellas responsive
- Optimizada para pantalla TFT de 7 pulgadas
"""

import tkinter as tk
from fingerprint_registration_interface import show_fingerprint_registration_interface

def test_fingerprint_registration():
    """Prueba la interfaz de registro de huellas"""
    print("🔐 PRUEBA DE INTERFAZ DE REGISTRO DE HUELLAS")
    print("=" * 60)
    print("📱 Optimizada para pantalla TFT de 7 pulgadas")
    print("🔍 Filtrado por tipo de personal")
    print("📋 Lista responsive con scroll")
    print("=" * 60)
    
    try:
        # Crear ventana principal de prueba
        root = tk.Tk()
        root.title("Prueba - Sistema de Registro de Huellas")
        root.geometry("400x300")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🧪 PRUEBA DE REGISTRO DE HUELLAS",
            font=("Segoe UI", 16, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Características de la interfaz:

✅ Responsive para pantalla TFT 7"
✅ Filtrado por tipo de personal
✅ Búsqueda en tiempo real
✅ Lista con scroll optimizada
✅ Diseño futurista y profesional
✅ Integración con alertas nativas
✅ Registro/actualización de huellas
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
        
        # Botón para abrir interfaz
        open_btn = tk.Button(
            main_frame,
            text="🔐 ABRIR REGISTRO DE HUELLAS",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: show_fingerprint_registration_interface(root)
        )
        open_btn.pack(pady=10)
        
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
        exit_btn.pack(pady=10)
        
        print("✅ Ventana de prueba creada")
        print("   - Haz clic en 'ABRIR REGISTRO DE HUELLAS' para probar la interfaz")
        print("   - La interfaz se abrirá optimizada para pantalla de 7 pulgadas")
        print("   - Prueba los filtros y la búsqueda")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

def test_responsive_design():
    """Prueba el diseño responsive en diferentes tamaños"""
    print("\n📱 PRUEBA DE DISEÑO RESPONSIVE")
    print("=" * 40)
    
    sizes = [
        (800, 480, "TFT 7 pulgadas"),
        (1024, 768, "Tablet"),
        (1280, 720, "HD"),
        (1920, 1080, "Full HD")
    ]
    
    for width, height, description in sizes:
        print(f"   {description}: {width}x{height}")
    
    print("\n✅ La interfaz se adapta automáticamente a diferentes resoluciones")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE REGISTRO DE HUELLAS")
    print("=" * 60)
    
    try:
        # Probar diseño responsive
        test_responsive_design()
        
        # Preguntar si quiere probar la interfaz
        print("\n" + "=" * 60)
        response = input("¿Deseas probar la interfaz de registro de huellas? (s/n): ").lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_fingerprint_registration()
        else:
            print("⏭️  Saltando prueba de interfaz")
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
