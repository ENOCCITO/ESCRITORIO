#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_registration_fix.py
- Prueba específica para verificar que el error de acceso denegado esté corregido
- Verifica que las alertas de registro funcionen correctamente
"""

import tkinter as tk
from fingerprint_registration_interface import show_fingerprint_registration_interface

def test_registration_alerts():
    """Prueba las alertas de registro sin lector biométrico"""
    print("🔧 PRUEBA DE CORRECCIÓN DE ALERTAS")
    print("=" * 50)
    
    try:
        # Crear ventana principal de prueba
        root = tk.Tk()
        root.title("Prueba - Corrección de Alertas de Registro")
        root.geometry("400x300")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🔧 PRUEBA DE CORRECCIÓN",
            font=("Segoe UI", 16, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Esta prueba verifica que:

✅ No aparezca "ACCESO DENEGADO" al hacer clic en Registrar
✅ Las alertas de error sean específicas para registro
✅ Las alertas de advertencia funcionen correctamente
✅ El flujo de registro sea fluido
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
        
        # Botón para probar interfaz
        test_btn = tk.Button(
            main_frame,
            text="🔧 PROBAR INTERFAZ CORREGIDA",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=20,
            pady=15,
            cursor="hand2",
            command=lambda: show_fingerprint_registration_interface(root)
        )
        test_btn.pack(pady=10)
        
        # Instrucciones
        instructions_text = """
INSTRUCCIONES:
1. Haz clic en "PROBAR INTERFAZ CORREGIDA"
2. En la interfaz de registro, haz clic en "Registrar" de cualquier persona
3. Verifica que NO aparezca "ACCESO DENEGADO"
4. Debería aparecer una alerta de error específica para registro
5. La alerta debe tener el título correcto y ser clara
        """
        
        instructions_label = tk.Label(
            main_frame,
            text=instructions_text,
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#1a1a2e",
            justify="left"
        )
        instructions_label.pack(pady=(10, 0))
        
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
        print("   - Haz clic en 'PROBAR INTERFAZ CORREGIDA'")
        print("   - Prueba hacer clic en 'Registrar' de cualquier persona")
        print("   - Verifica que las alertas sean correctas")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CORRECCIÓN")
    print("=" * 60)
    
    try:
        test_registration_alerts()
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
