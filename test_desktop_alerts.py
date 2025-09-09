#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_desktop_alerts.py
- Prueba del sistema de alertas nativas de escritorio
- Demostración de las alertas sin abrir navegador
"""

import time
import tkinter as tk
from desktop_alerts import desktop_alert_system
from role_validator import role_validator

def test_desktop_alerts():
    """Prueba el sistema de alertas nativas de escritorio"""
    print("🖥️ PRUEBA DEL SISTEMA DE ALERTAS NATIVAS")
    print("=" * 50)
    
    # Crear ventana principal para las pruebas
    root = tk.Tk()
    root.title("Prueba de Alertas Nativas")
    root.geometry("300x200")
    root.configure(bg="#1a1a2e")
    
    # Frame principal
    main_frame = tk.Frame(root, bg="#1a1a2e")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title_label = tk.Label(
        main_frame,
        text="🧪 PRUEBA DE ALERTAS",
        font=("Segoe UI", 16, "bold"),
        fg="#00ffff",
        bg="#1a1a2e"
    )
    title_label.pack(pady=(0, 20))
    
    # Botones de prueba
    buttons_frame = tk.Frame(main_frame, bg="#1a1a2e")
    buttons_frame.pack(fill="x", pady=10)
    
    def test_access_denied():
        desktop_alert_system.show_access_denied_alert("admin", "Usuario de Prueba")
    
    def test_fingerprint_not_found():
        desktop_alert_system.show_fingerprint_not_found_alert()
    
    def test_access_granted():
        desktop_alert_system.show_access_granted_alert("admin", "Usuario Autorizado")
    
    def test_all_roles():
        roles = ['admin', 'instructor', 'security', 'cleaning', 'administrative']
        for i, role in enumerate(roles):
            root.after(i * 2000, lambda r=role: desktop_alert_system.show_access_denied_alert(r, "Usuario de Prueba"))
    
    def close_all():
        desktop_alert_system.close_all_alerts()
    
    # Botón de acceso denegado
    btn_denied = tk.Button(
        buttons_frame,
        text="🚫 Acceso Denegado",
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
        command=test_access_denied
    )
    btn_denied.pack(fill="x", pady=5)
    
    # Botón de huella no encontrada
    btn_not_found = tk.Button(
        buttons_frame,
        text="🔍 Huella No Encontrada",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",
        bg="#ffa726",
        activeforeground="#ffffff",
        activebackground="#ff9800",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_fingerprint_not_found
    )
    btn_not_found.pack(fill="x", pady=5)
    
    # Botón de acceso concedido
    btn_granted = tk.Button(
        buttons_frame,
        text="✅ Acceso Concedido",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",
        bg="#4caf50",
        activeforeground="#ffffff",
        activebackground="#45a049",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_access_granted
    )
    btn_granted.pack(fill="x", pady=5)
    
    # Botón de prueba de todos los roles
    btn_all_roles = tk.Button(
        buttons_frame,
        text="🎭 Probar Todos los Roles",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",
        bg="#9c27b0",
        activeforeground="#ffffff",
        activebackground="#8e24aa",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=test_all_roles
    )
    btn_all_roles.pack(fill="x", pady=5)
    
    # Botón de cerrar todas las alertas
    btn_close_all = tk.Button(
        buttons_frame,
        text="❌ Cerrar Todas las Alertas",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",
        bg="#f44336",
        activeforeground="#ffffff",
        activebackground="#d32f2f",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=close_all
    )
    btn_close_all.pack(fill="x", pady=5)
    
    # Información
    info_label = tk.Label(
        main_frame,
        text="Haz clic en los botones para probar las alertas nativas",
        font=("Segoe UI", 9),
        fg="#888888",
        bg="#1a1a2e"
    )
    info_label.pack(pady=(20, 0))
    
    # Configurar cierre
    def on_closing():
        desktop_alert_system.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en los botones para probar las alertas")
    print("   - Las alertas aparecerán como ventanas nativas de escritorio")
    print("   - Cierra la ventana principal para terminar")
    
    # Ejecutar la ventana
    root.mainloop()

def test_role_validation():
    """Prueba la validación de roles"""
    print("\n🔍 PRUEBA DE VALIDACIÓN DE ROLES")
    print("=" * 50)
    
    # Probar con diferentes combinaciones de usuario y rol
    test_scenarios = [
        (1, 'admin', 'ADMINISTRADOR'),
        (2, 'instructor', 'INSTRUCTOR'),
        (3, 'security', 'SEGURIDAD'),
        (4, 'cleaning', 'LIMPIEZA'),
        (5, 'administrative', 'ADMINISTRATIVO'),
        (1, 'instructor', 'ADMINISTRADOR'),  # Usuario admin intentando acceder como instructor
        (2, 'admin', 'INSTRUCTOR'),          # Usuario instructor intentando acceder como admin
    ]
    
    for user_id, requested_role, expected_role in test_scenarios:
        has_access, user_name, user_role = role_validator.validate_role_access(user_id, requested_role)
        
        print(f"\n👤 Usuario ID: {user_id}")
        print(f"   Rol solicitado: {requested_role}")
        print(f"   Rol real: {user_role}")
        print(f"   Acceso: {'✅ CONCEDIDO' if has_access else '❌ DENEGADO'}")
        
        if not has_access and user_name:
            print(f"   ⚠️  {user_name} no tiene permisos para acceder como {requested_role}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE ALERTAS NATIVAS")
    print("=" * 60)
    
    try:
        # Probar validación de roles
        test_role_validation()
        
        # Preguntar si quiere probar las alertas visuales
        print("\n" + "=" * 60)
        response = input("¿Deseas probar las alertas nativas de escritorio? (s/n): ").lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_desktop_alerts()
        else:
            print("⏭️  Saltando pruebas visuales")
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
    finally:
        # Limpiar alertas
        try:
            desktop_alert_system.cleanup()
            print("🧹 Alertas limpiadas")
        except:
            pass
