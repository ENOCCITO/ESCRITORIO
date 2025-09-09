#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_security_interface.py
- Prueba la interfaz de seguridad con ambientes de la base de datos
"""

import tkinter as tk
from security_interface import SecurityInterface
from utils import get_available_environments

def test_security_interface():
    """Prueba la interfaz de seguridad con ambientes de la base de datos"""
    print("🚀 INICIANDO PRUEBA DE INTERFAZ DE SEGURIDAD")
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
    root.title("PRUEBA - INTERFAZ DE SEGURIDAD")
    root.geometry("500x400")
    root.configure(bg="#0a0a0a")
    
    # Crear instancia de la interfaz
    security_interface = SecurityInterface(root)
    
    # Botón para abrir la interfaz
    def open_security_interface():
        print("🛡️ Abriendo interfaz de seguridad...")
        security_interface.show_security_interface()
    
    # Crear botón de prueba futurista
    test_btn = tk.Button(
        root,
        text="🛡️ ABRIR INTERFAZ DE SEGURIDAD",
        command=open_security_interface,
        font=("Arial", 18, "bold"),
        bg="#ff6b35",
        fg="#ffffff",
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
        text="🛡️ INTERFAZ DE SEGURIDAD CON AMBIENTES REALES\n\n"
             "✨ NUEVAS CARACTERÍSTICAS:\n"
             "   • 🏢 Ambientes reales de la base de datos\n"
             "   • 🚪 Botones de ENTRADA y SALIDA para cada ambiente\n"
             "   • 📱 Diseño optimizado para pantalla de 7 pulgadas\n"
             "   • 🎨 Interfaz futurista con colores naranja y azul\n"
             "   • 📊 Información detallada de cada ambiente\n"
             "   • 🔄 Scroll para múltiples ambientes\n\n"
             "🎯 FUNCIONALIDAD:\n"
             "   • Control de entrada y salida por ambiente\n"
             "   • Información de ubicación, tipo y edificio\n"
             "   • Efectos hover diferenciados por tipo de acceso\n"
             "   • Integración completa con base de datos",
        font=("Arial", 10),
        bg="#0a0a0a",
        fg="#ff6b35",
        justify="left"
    )
    info_label.pack(pady=20, padx=20)
    
    print("✅ Ventana de prueba creada")
    print("   - Haz clic en 'ABRIR INTERFAZ DE SEGURIDAD'")
    print("   - Verifica que se muestren los ambientes de la BD")
    print("   - Prueba los botones de ENTRADA y SALIDA")
    print("   - Verifica el diseño futurista y responsive")
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    test_security_interface()
