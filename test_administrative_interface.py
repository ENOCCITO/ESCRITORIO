#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_administrative_interface.py
- Prueba la interfaz administrativa con ambientes asignados
"""

import tkinter as tk
from administrative_interface import AdministrativeInterface
from utils import get_available_environments

def test_administrative_interface():
    """Prueba la interfaz administrativa con ambientes asignados"""
    print("🚀 INICIANDO PRUEBA DE INTERFAZ ADMINISTRATIVA")
    print("=" * 60)
    
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
    
    print("\n" + "=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("PRUEBA - INTERFAZ ADMINISTRATIVA")
    root.geometry("500x400")
    root.configure(bg="#0a0a0a")
    
    # Crear instancia de la interfaz
    admin_interface = AdministrativeInterface(root)
    
    # Botón para abrir la interfaz
    def open_admin_interface():
        print("📋 Abriendo interfaz administrativa...")
        admin_interface.show_administrative_interface()
    
    # Crear botón de prueba futurista
    test_btn = tk.Button(
        root,
        text="📋 ABRIR INTERFAZ ADMINISTRATIVA",
        command=open_admin_interface,
        font=("Arial", 18, "bold"),
        bg="#00d4ff",
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
        text="📋 INTERFAZ ADMINISTRATIVA CON AMBIENTES ASIGNADOS\n\n"
             "✨ NUEVAS CARACTERÍSTICAS:\n"
             "   • 🏢 Ambientes reales de la base de datos\n"
             "   • 📋 Tarjetas detalladas para cada ambiente\n"
             "   • 📱 Diseño optimizado para pantalla de 7 pulgadas\n"
             "   • 🎨 Interfaz futurista con colores azul y verde\n"
             "   • 📊 Información completa de cada ambiente\n"
             "   • 🔄 Scroll para múltiples ambientes\n\n"
             "🎯 FUNCIONALIDAD:\n"
             "   • Visualización de ambientes asignados\n"
             "   • Información de ubicación, tipo y edificio\n"
             "   • Botón de acceso para cada ambiente\n"
             "   • Efectos hover en botones\n"
             "   • Integración completa con base de datos",
        font=("Arial", 10),
        bg="#0a0a0a",
        fg="#00d4ff",
        justify="left"
    )
    info_label.pack(pady=20, padx=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ ADMINISTRATIVA'")
    print("   - Verifica que se muestren los ambientes de la BD")
    print("   - Prueba los botones de acceso a ambientes")
    print("   - Verifica el diseño futurista y responsive")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_administrative_interface()
