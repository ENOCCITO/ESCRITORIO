#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_7inch_interface.py
- Prueba la interfaz del instructor optimizada para pantalla de 7 pulgadas
"""

import tkinter as tk
from instructor_interface import InstructorInterface

def test_7inch_interface():
    """Prueba la interfaz optimizada para 7 pulgadas"""
    print("🚀 INICIANDO PRUEBA PARA PANTALLA DE 7 PULGADAS")
    print("=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA - PANTALLA 7 PULGADAS")
    root.geometry("400x300")
    root.configure(bg="#0a0a0a")
    
    # Crear instancia de la interfaz
    instructor_interface = InstructorInterface(root)
    
    # Botón para abrir la interfaz
    def open_instructor_interface():
        print("👨‍🏫 Abriendo interfaz optimizada para 7 pulgadas...")
        instructor_interface.show_instructor_interface()
    
    # Crear botón de prueba futurista
    test_btn = tk.Button(
        root,
        text="🚀 ABRIR INTERFAZ 7 PULGADAS",
        command=open_instructor_interface,
        font=("Arial", 16, "bold"),
        bg="#00d4ff",
        fg="#000000",
        relief="raised",
        bd=3,
        padx=25,
        pady=15,
        cursor="hand2"
    )
    test_btn.pack(expand=True, pady=50)
    
    # Información de prueba
    info_label = tk.Label(
        root,
        text="📱 INTERFAZ OPTIMIZADA PARA 7 PULGADAS\n\n"
             "✨ CARACTERÍSTICAS:\n"
             "   • 🎨 Diseño futurista con colores neón\n"
             "   • 📏 Tamaño optimizado: 800x600px\n"
             "   • 🔥 Iconos grandes y visibles\n"
             "   • 📊 Layout responsive\n"
             "   • 🌟 Efectos visuales mejorados\n\n"
             "🎯 IDEAL PARA:\n"
             "   • Pantallas táctiles pequeñas\n"
             "   • Tablets de 7 pulgadas\n"
             "   • Interfaces de kiosco\n"
             "   • Sistemas embebidos",
        font=("Arial", 10),
        bg="#0a0a0a",
        fg="#00ff88",
        justify="left"
    )
    info_label.pack(pady=20, padx=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ 7 PULGADAS'")
    print("   - Verifica el diseño futurista y responsive")
    print("   - Comprueba que se vea bien en pantalla pequeña")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"400x300+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_7inch_interface()
