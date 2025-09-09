#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_window_visibility.py
- Prueba específica para verificar que la ventana de registro se mantenga visible
- Simula el flujo completo desde administrador
"""

import tkinter as tk
import time
from admin_interface import AdminInterface
from fingerprint_registration_interface import show_fingerprint_registration_interface

def test_window_visibility():
    """Prueba que la ventana de registro se mantenga visible"""
    print("🔍 PRUEBA DE VISIBILIDAD DE VENTANAS")
    print("=" * 50)
    
    # Crear ventana principal simulada
    root = tk.Tk()
    root.title("SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA")
    root.geometry("800x600")
    root.configure(bg="#0a0a0a")
    
    # Frame principal
    main_frame = tk.Frame(root, bg="#0a0a0a")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title_label = tk.Label(
        main_frame,
        text="🧪 PRUEBA DE VISIBILIDAD",
        font=("Segoe UI", 20, "bold"),
        fg="#00ffff",
        bg="#0a0a0a"
    )
    title_label.pack(pady=(0, 20))
    
    # Información
    info_text = """
Esta prueba simula el flujo completo:

1. Abrir interfaz de administrador
2. Hacer clic en "Registrar Huella"
3. Verificar que la ventana se mantenga visible
4. Cerrar y verificar que regrese al administrador
    """
    
    info_label = tk.Label(
        main_frame,
        text=info_text,
        font=("Segoe UI", 12),
        fg="#cccccc",
        bg="#0a0a0a",
        justify="left"
    )
    info_label.pack(pady=(0, 30))
    
    # Botones de prueba
    buttons_frame = tk.Frame(main_frame, bg="#0a0a0a")
    buttons_frame.pack(pady=20)
    
    # Crear interfaz de administrador
    admin_interface = AdminInterface(root)
    
    def test_admin_interface():
        print("🔐 Abriendo interfaz de administrador...")
        admin_interface.show_admin_interface()
    
    def test_direct_registration():
        print("👆 Abriendo registro de huellas directamente...")
        show_fingerprint_registration_interface(root)
    
    def test_window_states():
        print("📊 Verificando estados de ventanas...")
        windows = root.winfo_children()
        print(f"   Ventanas hijas: {len(windows)}")
        for i, window in enumerate(windows):
            if hasattr(window, 'winfo_exists') and window.winfo_exists():
                print(f"   Ventana {i+1}: {window.winfo_class()} - Visible: {window.winfo_viewable()}")
    
    # Botón para probar interfaz de administrador
    admin_btn = tk.Button(
        buttons_frame,
        text="🔐 ABRIR ADMINISTRADOR",
        font=("Segoe UI", 12, "bold"),
        fg="#ffffff",
        bg="#00ffff",
        activeforeground="#ffffff",
        activebackground="#00cccc",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_admin_interface
    )
    admin_btn.pack(side="left", padx=10)
    
    # Botón para probar registro directo
    reg_btn = tk.Button(
        buttons_frame,
        text="👆 REGISTRO DIRECTO",
        font=("Segoe UI", 12, "bold"),
        fg="#ffffff",
        bg="#4caf50",
        activeforeground="#ffffff",
        activebackground="#45a049",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_direct_registration
    )
    reg_btn.pack(side="left", padx=10)
    
    # Botón para verificar estados
    state_btn = tk.Button(
        buttons_frame,
        text="📊 VERIFICAR ESTADOS",
        font=("Segoe UI", 12, "bold"),
        fg="#ffffff",
        bg="#ffa726",
        activeforeground="#ffffff",
        activebackground="#ff9800",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_window_states
    )
    state_btn.pack(side="left", padx=10)
    
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
    exit_btn.pack(side="bottom", pady=(30, 0))
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR ADMINISTRADOR' para probar el flujo completo")
    print("   - Haz clic en 'REGISTRO DIRECTO' para probar la ventana directamente")
    print("   - Usa 'VERIFICAR ESTADOS' para ver el estado de las ventanas")
    
    # Ejecutar
    root.mainloop()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE VISIBILIDAD DE VENTANAS")
    print("=" * 60)
    
    try:
        test_window_visibility()
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
