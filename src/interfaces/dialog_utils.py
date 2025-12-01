#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dialog_utils.py
- Utilidades para diálogos que se cierran limpiamente
"""

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt


class CleanCloseDialog(QDialog):
    """QDialog personalizado que se cierra correctamente sin dejar procesos colgados"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        # Asegurar que el diálogo esté siempre encima
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    
    def keyPressEvent(self, event):
        """Maneja eventos de teclado"""
        if event.key() == Qt.Key_Escape:
            print("🚪 Tecla ESC presionada - Cerrando ventana secundaria...")
            self.close()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Maneja el cierre limpio de la ventana"""
        try:
            print(f"🚪 Cerrando {self.windowTitle()}...")
            event.accept()
            
            # Restaurar la ventana principal si existe el método
            if self.parent_window and hasattr(self.parent_window, 'show_main_window'):
                self.parent_window.show_main_window()
        except Exception as e:
            print(f"⚠️ Error al cerrar ventana: {e}")
            event.accept()
