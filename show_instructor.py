#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar directamente la interfaz de instructor
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from src.interfaces.instructor_interface import InstructorInterface
from src.utils import styles
from src.utils.utils import init_log_file, log_system_info

class InstructorWindow(QMainWindow):
    """Ventana principal para la interfaz de instructor"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Instructor - Sistema CEFA")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crear un widget central simple
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central_widget)
        
        # Crear la interfaz de instructor con esta ventana como padre
        self.instructor = InstructorInterface(self)
        
        # Mostrar la interfaz de instructor en la siguiente iteración del event loop
        QTimer.singleShot(100, self._show_interface)
    
    def _show_interface(self):
        """Mostrar la interfaz de instructor"""
        try:
            print("👨‍🏫 Mostrando interfaz de instructor...")
            self.instructor.show_instructor_interface()
            print("✅ Interfaz de instructor mostrada")
        except Exception as e:
            print(f"❌ Error mostrando interfaz: {e}")
            import traceback
            traceback.print_exc()
    
    def show_main_window(self):
        """Método requerido por InstructorInterface para restaurar la ventana principal"""
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
    
    print("\n🚀 Iniciando interfaz de instructor...\n")
    
    # Crear y mostrar la ventana principal
    window = InstructorWindow()
    window.show()
    print(f"✅ Ventana principal creada y visible")
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
