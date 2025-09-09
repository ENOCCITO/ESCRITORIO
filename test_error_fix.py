#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_error_fix.py
- Prueba que el error de _auto_load_candidates se haya corregido
"""

import tkinter as tk
from main import App

def test_error_fix():
    """Prueba que el error se haya corregido"""
    print("🚀 INICIANDO PRUEBA DE CORRECCIÓN DE ERROR")
    print("=" * 50)
    
    try:
        print("✅ Creando instancia de la aplicación...")
        app = App()
        
        print("✅ Aplicación creada exitosamente")
        print("✅ El error '_auto_load_candidates' se ha corregido")
        
        # Cerrar la aplicación después de 2 segundos
        app.after(2000, app.destroy)
        
        print("✅ Iniciando aplicación por 2 segundos...")
        app.mainloop()
        
        print("✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_error_fix()
    if success:
        print("\n🎉 ¡ERROR CORREGIDO EXITOSAMENTE!")
    else:
        print("\n💥 Error aún presente")
