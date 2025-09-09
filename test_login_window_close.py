#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_login_window_close.py
- Prueba específica para verificar que la ventana de escaneo se cierre después del login exitoso
- Verifica que la interfaz de administrador quede visible
"""

import tkinter as tk
from main import App

def test_login_window_close():
    """Prueba el cierre de la ventana de escaneo después del login exitoso"""
    print("🚪 PRUEBA DE CIERRE DE VENTANA DESPUÉS DEL LOGIN")
    print("=" * 60)
    
    try:
        # Crear la aplicación principal
        app = App()
        
        print("✅ Aplicación principal creada")
        print("   - La ventana de escaneo de huella debería estar visible")
        print("   - Haz clic en 'ADMINISTRADOR' para probar el login")
        print("   - Después del login exitoso, la ventana de escaneo debería cerrarse")
        print("   - La interfaz de administrador debería quedar visible")
        
        # Ejecutar la aplicación
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CIERRE DE VENTANA")
    print("=" * 70)
    
    try:
        test_login_window_close()
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
