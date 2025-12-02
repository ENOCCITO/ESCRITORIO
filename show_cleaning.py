#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar directamente la interfaz de aseo/limpieza
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from src.interfaces.cleaning_interface import CleaningInterface
from src.utils import styles
from src.utils.utils import init_log_file, log_system_info

class CleaningWindow(QMainWindow):
    """Ventana principal para la interfaz de aseo"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Aseo - Sistema CEFA")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crear un widget central simple
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f6f7f8;")
        self.setCentralWidget(central_widget)
        
        # Crear la interfaz de aseo con esta ventana como padre
        self.cleaning = CleaningInterface(self)
        
        # Mostrar la interfaz de aseo en la siguiente iteración del event loop
        QTimer.singleShot(100, self._show_interface)
    
    def _show_interface(self):
        """Mostrar la interfaz de aseo"""
        try:
            print("🧹 Mostrando interfaz de aseo...")
            self.cleaning.show_cleaning_interface()
            print("✅ Interfaz de aseo mostrada")
        except Exception as e:
            print(f"❌ Error mostrando interfaz: {e}")
            import traceback
            traceback.print_exc()
    
    def show_main_window(self):
        """Método requerido por CleaningInterface para restaurar la ventana principal"""
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
    
    print("\n🚀 Iniciando interfaz de aseo...\n")
    
    # Crear y mostrar la ventana principal
    window = CleaningWindow()
    window.show()
    print(f"✅ Ventana principal creada y visible")
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
