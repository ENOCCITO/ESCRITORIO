#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_scanner_activation.py
- Prueba específica para verificar que el lector biométrico se active correctamente
- Verifica que la interfaz no se cierre y maneje bien la conexión
"""

import tkinter as tk
from fingerprint_registration_interface import show_fingerprint_registration_interface

def test_scanner_activation():
    """Prueba la activación del lector biométrico"""
    print("🔌 PRUEBA DE ACTIVACIÓN DEL LECTOR BIOMÉTRICO")
    print("=" * 60)
    
    try:
        # Crear ventana principal de prueba
        root = tk.Tk()
        root.title("Prueba - Activación del Lector Biométrico")
        root.geometry("500x400")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🔌 PRUEBA DE ACTIVACIÓN DEL LECTOR",
            font=("Segoe UI", 18, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Esta prueba verifica que:

✅ El lector biométrico se active correctamente
✅ La interfaz de registro no se cierre
✅ Las alertas sean específicas y claras
✅ El botón de verificación funcione
✅ La conexión se maneje en tiempo real
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
        
        # Botón para probar interfaz
        test_btn = tk.Button(
            main_frame,
            text="🔌 PROBAR ACTIVACIÓN DEL LECTOR",
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
            command=lambda: show_fingerprint_registration_interface(root)
        )
        test_btn.pack(pady=20)
        
        # Instrucciones
        instructions_text = """
INSTRUCCIONES:
1. Haz clic en "PROBAR ACTIVACIÓN DEL LECTOR"
2. En la interfaz de registro, observa el estado del lector
3. Haz clic en el botón 🔌 para verificar la conexión
4. Intenta registrar una huella de cualquier persona
5. Verifica que las alertas sean específicas y claras
6. La interfaz NO debe cerrarse automáticamente
        """
        
        instructions_label = tk.Label(
            main_frame,
            text=instructions_text,
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e",
            justify="left"
        )
        instructions_label.pack(pady=(10, 0))
        
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
        print("   - Haz clic en 'PROBAR ACTIVACIÓN DEL LECTOR'")
        print("   - Observa el estado del lector en la interfaz")
        print("   - Usa el botón 🔌 para verificar la conexión")
        print("   - Intenta registrar una huella")
        print("   - Verifica que la interfaz no se cierre")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE ACTIVACIÓN DEL LECTOR")
    print("=" * 70)
    
    try:
        test_scanner_activation()
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
