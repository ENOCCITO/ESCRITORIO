#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_modal_close_only.py
- Prueba específica para verificar que solo se cierre el modal de escaneo
- Verifica que la aplicación principal permanezca abierta
"""

import tkinter as tk
from main import App

def test_modal_close_only():
    """Prueba que solo se cierre el modal de escaneo, no toda la aplicación"""
    print("🚪 PRUEBA DE CIERRE SOLO DEL MODAL DE ESCANEO")
    print("=" * 60)
    
    try:
        # Crear la aplicación principal
        app = App()
        
        print("✅ Aplicación principal creada")
        print("   - La ventana principal debería estar visible")
        print("   - Haz clic en 'ADMINISTRADOR' para abrir el modal de escaneo")
        print("   - Después del login exitoso:")
        print("     ✅ Solo el modal de escaneo debería cerrarse")
        print("     ✅ La ventana principal debería permanecer abierta")
        print("     ✅ La interfaz de administrador debería abrirse")
        print("   - Si cancelas el escaneo:")
        print("     ✅ Solo el modal debería cerrarse")
        print("     ✅ La ventana principal debería permanecer abierta")
        
        # Ejecutar la aplicación
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CIERRE SOLO DEL MODAL")
    print("=" * 70)
    
    try:
        test_modal_close_only()
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
