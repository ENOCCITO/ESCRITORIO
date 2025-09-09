#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_cleaning_interface.py
- Prueba la interfaz de aseo con selección de ambientes de la base de datos
"""

import tkinter as tk
from cleaning_interface import CleaningInterface

def test_cleaning_interface():
    """Prueba la interfaz de aseo con ambientes de la base de datos"""
    print("🚀 INICIANDO PRUEBA DE INTERFAZ DE ASEO")
    print("=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA - INTERFAZ DE ASEO")
    root.geometry("400x300")
    root.configure(bg="#0a0a0a")
    
    # Crear instancia de la interfaz
    cleaning_interface = CleaningInterface(root)
    
    # Botón para abrir la interfaz
    def open_cleaning_interface():
        print("🧹 Abriendo interfaz de aseo con ambientes...")
        cleaning_interface.show_cleaning_interface()
    
    # Crear botón de prueba futurista
    test_btn = tk.Button(
        root,
        text="🧹 ABRIR INTERFAZ DE ASEO",
        command=open_cleaning_interface,
        font=("Arial", 16, "bold"),
        bg="#00ff88",
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
        text="🧹 INTERFAZ DE ASEO CON AMBIENTES\n\n"
             "✨ NUEVAS CARACTERÍSTICAS:\n"
             "   • 🏢 Ambientes reales de la base de datos\n"
             "   • 📱 Diseño optimizado para 7 pulgadas\n"
             "   • 🎨 Interfaz futurista con colores neón\n"
             "   • 📊 Información detallada de cada ambiente\n"
             "   • 🔄 Scroll para múltiples ambientes\n\n"
             "🎯 FUNCIONALIDAD:\n"
             "   • Selección de ambiente para limpieza\n"
             "   • Información de ubicación y tipo\n"
             "   • Efectos hover en botones\n"
             "   • Integración con base de datos",
        font=("Arial", 10),
        bg="#0a0a0a",
        fg="#00ff88",
        justify="left"
    )
    info_label.pack(pady=20, padx=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ DE ASEO'")
    print("   - Verifica que se muestren los ambientes de la BD")
    print("   - Prueba la selección de ambientes")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"400x300+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_cleaning_interface()
