#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_instructor_interface.py
- Prueba la nueva interfaz del instructor con información directa
"""

import tkinter as tk
from instructor_interface import InstructorInterface

def test_instructor_interface():
    """Prueba la interfaz del instructor con información directa"""
    print("🚀 INICIANDO PRUEBA DE INTERFAZ DE INSTRUCTOR")
    print("=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA - INTERFAZ DE INSTRUCTOR")
    root.geometry("400x300")
    root.configure(bg="#1a1a2e")
    
    # Crear instancia de la interfaz
    instructor_interface = InstructorInterface(root)
    
    # Botón para abrir la interfaz
    def open_instructor_interface():
        print("👨‍🏫 Abriendo interfaz de instructor...")
        instructor_interface.show_instructor_interface()
    
    # Crear botón de prueba
    test_btn = tk.Button(
        root,
        text="👨‍🏫 ABRIR INTERFAZ DE INSTRUCTOR",
        command=open_instructor_interface,
        font=("Arial", 14, "bold"),
        bg="#16213e",
        fg="#00d4ff",
        relief="raised",
        bd=2,
        padx=20,
        pady=10
    )
    test_btn.pack(expand=True)
    
    # Información de prueba
    info_label = tk.Label(
        root,
        text="✅ Interfaz del instructor modificada\n"
             "📋 Ahora muestra información directa:\n"
             "   • Ambiente asignado\n"
             "   • Horario de clases\n"
             "   • Sin botones innecesarios",
        font=("Arial", 10),
        bg="#1a1a2e",
        fg="#ffffff",
        justify="center"
    )
    info_label.pack(pady=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ DE INSTRUCTOR'")
    print("   - Verifica que se muestre la información directa")
    print("   - No debe haber botones 'Ver Horarios' o 'Acceso a Aulas'")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"400x300+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_instructor_interface()
