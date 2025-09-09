#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_aseo_environments.py
- Prueba completa de la interfaz de aseo con ambientes de la base de datos
"""

import tkinter as tk
from cleaning_interface import CleaningInterface
from utils import get_available_environments

def test_aseo_environments():
    """Prueba completa de la interfaz de aseo con ambientes"""
    print("🚀 INICIANDO PRUEBA COMPLETA DE INTERFAZ DE ASEO")
    print("=" * 70)
    
    # Verificar ambientes en la base de datos
    print("🔍 Verificando ambientes en la base de datos...")
    environments = get_available_environments()
    
    if environments:
        print(f"✅ Se encontraron {len(environments)} ambientes disponibles:")
        for i, env in enumerate(environments, 1):
            env_id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio = env
            print(f"   {i}. {nombre} - {tipo_ambiente} ({ubicacion})")
    else:
        print("❌ No se encontraron ambientes en la base de datos")
    
    print("\n" + "=" * 70)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA COMPLETA - INTERFAZ DE ASEO")
    root.geometry("500x400")
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
        font=("Arial", 18, "bold"),
        bg="#00ff88",
        fg="#000000",
        relief="raised",
        bd=3,
        padx=30,
        pady=20,
        cursor="hand2"
    )
    test_btn.pack(expand=True, pady=30)
    
    # Información de prueba
    info_label = tk.Label(
        root,
        text="🧹 INTERFAZ DE ASEO CON AMBIENTES REALES\n\n"
             "✨ CARACTERÍSTICAS IMPLEMENTADAS:\n"
             "   • 🏢 Ambientes reales de la base de datos\n"
             "   • 📱 Diseño optimizado para pantalla de 7 pulgadas\n"
             "   • 🎨 Interfaz futurista con colores neón\n"
             "   • 📊 Información detallada de cada ambiente\n"
             "   • 🔄 Scroll para múltiples ambientes\n"
             "   • 🖱️ Efectos hover en botones\n\n"
             "🎯 FUNCIONALIDAD:\n"
             "   • Selección de ambiente para limpieza\n"
             "   • Información de ubicación, tipo y edificio\n"
             "   • Integración completa con base de datos\n"
             "   • Diseño responsive y profesional",
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
    print("   - Verifica el diseño futurista y responsive")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_aseo_environments()
