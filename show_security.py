#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar directamente la interfaz de seguridad
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from src.interfaces.security_interface import SecurityInterface
from src.utils import styles
from src.utils.utils import init_log_file, log_system_info

class SecurityWindow(QMainWindow):
    """Ventana principal para la interfaz de seguridad"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Seguridad - Sistema CEFA")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crear un widget central simple
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f6f7f8;")
        self.setCentralWidget(central_widget)
        
        # Crear la interfaz de seguridad con esta ventana como padre
        self.security = SecurityInterface(self, None)
        
        # Mostrar la interfaz de seguridad en la siguiente iteración del event loop
        QTimer.singleShot(100, self._show_interface)
    
    def _show_interface(self):
        """Mostrar la interfaz de seguridad"""
        try:
            print("📱 Mostrando interfaz de seguridad...")
            self.security.show_security_interface()
            print("✅ Interfaz de seguridad mostrada")
        except Exception as e:
            print(f"❌ Error mostrando interfaz: {e}")
            import traceback
            traceback.print_exc()
    
    def show_main_window(self):
        """Método requerido por SecurityInterface para restaurar la ventana principal"""
        self.show()
        self.raise_()
        self.activateWindow()
        print("🔄 Ventana principal restaurada")

def main():
    # Crear la aplicación Qt
    app = QApplication.instance() or QApplication(sys.argv)
    styles.setup_futuristic_styles(app)
    
    # Inicializar logs
    init_log_file()
    log_system_info()
    
    print("\n🚀 Iniciando interfaz de seguridad...\n")
    
    # Crear y mostrar la ventana principal
    window = SecurityWindow()
    window.show()
    print(f"✅ Ventana principal creada y visible")
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
