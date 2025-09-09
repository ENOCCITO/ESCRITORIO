#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_instructor_integration.py
- Prueba la integración completa del instructor con el sistema principal
"""

import tkinter as tk
from instructor_interface import InstructorInterface

def test_instructor_integration():
    """Prueba la integración completa del instructor"""
    print("🚀 INICIANDO PRUEBA DE INTEGRACIÓN DE INSTRUCTOR")
    print("=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA - INTEGRACIÓN INSTRUCTOR")
    root.geometry("500x400")
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
        text="🚀 INTERFAZ DE INSTRUCTOR FUTURISTA\n\n"
             "✨ MEJORAS IMPLEMENTADAS:\n"
             "   • 🎨 Diseño futurista con colores neón\n"
             "   • 📱 Optimizada para pantalla de 7 pulgadas\n"
             "   • 🔥 Iconos profesionales y animaciones\n"
             "   • 📊 Información directa sin botones innecesarios\n"
             "   • 🌟 Efectos visuales y bordes brillantes\n\n"
             "🎯 CARACTERÍSTICAS:\n"
             "   • Header con icono grande y efectos\n"
             "   • Ambiente asignado con iconos temáticos\n"
             "   • Horario con scroll y formato mejorado\n"
             "   • Footer con botón de cerrar sesión\n"
             "   • Responsive para pantalla táctil",
        font=("Arial", 10),
        bg="#1a1a2e",
        fg="#00d4ff",
        justify="left"
    )
    info_label.pack(pady=20, padx=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ DE INSTRUCTOR'")
    print("   - Verifica que se muestre la información directa")
    print("   - No debe haber botones 'Ver Horarios' o 'Acceso a Aulas'")
    print("   - Debe mostrar ambiente asignado y horario directamente")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_instructor_integration()
