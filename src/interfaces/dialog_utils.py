#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dialog_utils.py
- Utilidades para diálogos que se cierran limpiamente
"""

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon


class CleanCloseDialog(QDialog):
    """QDialog personalizado que se cierra correctamente sin dejar procesos colgados"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        # Configurar como ventana principal sin decoraciones especiales
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self._is_closing = False
    
    def keyPressEvent(self, event):
        """Maneja eventos de teclado"""
        if event.key() == Qt.Key_Escape:
            print("🚪 Tecla ESC presionada - Cerrando ventana secundaria...")
            self.close()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Maneja el cierre limpio de la ventana"""
        # Evitar cierre recursivo
        if self._is_closing:
            event.accept()
            return
        
        self._is_closing = True
        try:
            print(f"🚪 Cerrando {self.windowTitle()}...")
            # Aceptar el evento de cierre
            event.accept()
            
            # Ocultar inmediatamente esta ventana
            self.hide()
            self.setVisible(False)
            
            # Restaurar la ventana principal si existe el método
            if self.parent_window and hasattr(self.parent_window, 'show_main_window'):
                try:
                    # Más corto para que sea más rápido
                    QTimer.singleShot(10, lambda: self.parent_window.show_main_window())
                    print("✅ Restaurando pantalla principal...")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
        except Exception as e:
            print(f"⚠️ Error cerrando: {e}")
            event.accept()
