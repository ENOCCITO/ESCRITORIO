#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleaning_interface.py
- Interfaz de aseo (PySide6)
"""

from src.utils import styles
from src.config.config import *
from src.utils.utils import *
from src.utils.db_utils import get_available_keys, get_environments
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QMessageBox,
    QPushButton,
    QDialog,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QGridLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QFont, QPixmap
import os
from src.interfaces.dialog_utils import CleanCloseDialog

class CleaningInterface:
    def __init__(self, parent):
        self.parent = parent
        self.cleaning_window = None  # Referencia a la ventana de aseo

    def show_cleaning_interface(self):
        """Abre directamente el selector de ambientes"""
        try:
            # Ir directamente a la selección de ambientes
            self._open_environment_selector()
            print("✅ Interfaz de aseo - Selector de ambientes mostrado")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error al mostrar la interfaz de aseo:\n{e}")
            import traceback
            traceback.print_exc()

    def _open_environment_selector(self):
        try:
            # Colores del diseño Stitch
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            CARD_BG = "#ffffff"
            
            # Crear ventana en pantalla completa
            dlg = CleanCloseDialog(self.parent)
            self.cleaning_window = dlg  # Guardar referencia
            dlg.setModal(False)
            dlg.setWindowTitle("AMBIENTES DISPONIBLES")
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            dlg.showFullScreen()
            dlg.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            
            # Layout principal
            root_layout = QVBoxLayout(dlg)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)
            
            # Header con botón de cierre
            header = QWidget(dlg)
            header.setFixedHeight(60)
            header.setStyleSheet(f"background-color: {CARD_BG}; border-bottom: 1px solid {BORDER_COLOR};")
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(16, 12, 16, 12)
            header_layout.setSpacing(16)
            
            header_title = QLabel("🎟️ ASEO - GESTIÓN DE AMBIENTES", header)
            header_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 18px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            header_layout.addWidget(header_title)
            header_layout.addStretch()
            
            # Botón cerrar
            close_btn = QPushButton("✕", header)
            close_btn.setFixedSize(40, 40)
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setStyleSheet(
                f"QPushButton {{"
                f"background-color: #f0f2f4; "
                f"color: {TEXT_GRAY_DARK}; "
                f"border: none; "
                f"border-radius: 8px; "
                f"font-size: 20px; "
                f"font-weight: 600;"
                f"}}"
                f"QPushButton:hover {{"
                f"background-color: #E5E7EB; "
                f"}}"
            )
            close_btn.clicked.connect(dlg.close)
            header_layout.addWidget(close_btn)
            
            root_layout.addWidget(header)
            
            # Header simplificado (oculto para mantener la interfaz limpia)
            # header = QWidget(dlg)
            # header.setFixedHeight(60)
            # header.setStyleSheet(
            #     f"background-color: {CARD_BG}; "
            #     f"border-bottom: 1px solid {BORDER_COLOR};"
            # )
            # header_layout = QHBoxLayout(header)
            # header_layout.setContentsMargins(24, 16, 24, 16)
            # header_layout.setSpacing(16)
            # 
            # # Título con icono
            # title_container = QWidget(header)
            # title_layout = QHBoxLayout(title_container)
            # title_layout.setContentsMargins(0, 0, 0, 0)
            # title_layout.setSpacing(12)
            # 
            # icon_label = QLabel("🏢", header)
            # icon_label.setStyleSheet("font-size: 24px; background-color: transparent;")
            # title_layout.addWidget(icon_label)
            # 
            # title_label = QLabel("AMBIENTES DISPONIBLES", header)
            # title_label.setStyleSheet(
            #     f"color: {TEXT_GRAY_DARK}; "
            #     f"font-size: 18px; "
            #     f"font-weight: 700; "
            #     f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            # )
            # title_layout.addWidget(title_label)
            # 
            # header_layout.addWidget(title_container)
            # header_layout.addStretch()
            # 
            # # Botón cerrar (X)
            # close_btn = QPushButton("✕", header)
            # close_btn.setFixedSize(32, 32)
            # close_btn.setCursor(Qt.PointingHandCursor)
            # close_btn.setStyleSheet(
            #     f"QPushButton {{"
            #     f"background-color: {BG_LIGHT_HTML}; "
            #     f"color: {TEXT_GRAY_LIGHT}; "
            #     f"border: none; "
            #     f"border-radius: 8px; "
            #     f"font-size: 18px; "
            #     f"font-weight: 500;"
            #     f"}}"
            #     f"QPushButton:hover {{"
            #     f"background-color: #E5E7EB; "
            #     f"color: {TEXT_GRAY_DARK};"
            #     f"}}"
            # )
            # close_btn.clicked.connect(dlg.close)
            # header_layout.addWidget(close_btn)
            # 
            # root_layout.addWidget(header)
            
            # Área de contenido centrada
            content_widget = QWidget(dlg)
            content_widget.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(40, 40, 40, 40)
            content_layout.setAlignment(Qt.AlignCenter)
            
            # Título principal
            title_label = QLabel("👋 ¡Bienvenido Aseador@!", content_widget)
            title_label.setAlignment(Qt.AlignHCenter)
            title_label.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 32px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                f"margin-bottom: 20px;"
            )
            content_layout.addWidget(title_label)
            
            # Instrucción
            subtitle_label = QLabel("Seleccione un ambiente para comenzar la limpieza", content_widget)
            subtitle_label.setAlignment(Qt.AlignHCenter)
            subtitle_label.setWordWrap(True)
            subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            subtitle_label.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; "
                f"font-size: 18px; "
                f"font-weight: 400; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                f"margin-bottom: 30px;"
            )
            content_layout.addWidget(subtitle_label)
            
            # Contenedor de cuadrícula de ambientes
            environments_container = QWidget(content_widget)
            environments_container.setStyleSheet(f"background-color: transparent;")
            grid_layout = QGridLayout(environments_container)  # Cuadrícula
            grid_layout.setSpacing(20)  # Espaciado entre botones
            grid_layout.setContentsMargins(20, 20, 20, 20)
            
            # Obtener ambientes de la base de datos
            try:
                from src.utils.utils import get_available_environments
                
                # Obtener ambientes directamente
                ambientes_list = get_available_environments()
                
                if not ambientes_list:
                    # Estado vacío
                    empty_text = QLabel("No hay ambientes disponibles en este momento.", environments_container)
                    empty_text.setAlignment(Qt.AlignHCenter)
                    empty_text.setWordWrap(True)
                    empty_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    empty_text.setStyleSheet(
                        f"color: {TEXT_GRAY_LIGHT}; "
                        f"font-size: 16px; "
                        f"font-weight: 400; "
                        f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
                    )
                    grid_layout.addWidget(empty_text, 0, 0)
                else:
                    # Cuadrícula de botones (2 columnas)
                    row = 0
                    col = 0
                    for ambiente in ambientes_list:
                        # ambiente es una tupla: (id, name, description, length, latitude, farm_id, status)
                        env_id = ambiente[0]
                        nombre = ambiente[1]
                        
                        # Botón grande para el ambiente
                        env_btn = QPushButton(nombre, environments_container)
                        env_btn.setMinimumHeight(120)  # Botón más grande
                        env_btn.setMinimumWidth(120)   # Cuadrado
                        env_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        env_btn.setCursor(Qt.PointingHandCursor)
                        env_btn.setStyleSheet(
                            f"QPushButton {{"
                            f"background-color: {PRIMARY_COLOR}; "
                            f"color: white; "
                            f"border: none; "
                            f"border-radius: 12px; "
                            f"padding: 15px; "
                            f"font-size: 14px; "
                            f"font-weight: 700; "
                            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                            f"}}"
                            f"QPushButton:hover {{"
                            f"background-color: #0E5AA7; "
                            f"}}"
                            f"QPushButton:pressed {{"
                            f"background-color: #0A4A8A; "
                            f"}}"
                        )
                        env_btn.clicked.connect(lambda checked, eid=env_id, n=nombre: self._select_environment(n, eid))
                        
                        # Agregar a la cuadrícula
                        grid_layout.addWidget(env_btn, row, col)
                        
                        # Mover a la siguiente posición
                        col += 1
                        if col >= 2:  # 2 columnas
                            col = 0
                            row += 1
            except Exception as e:
                print(f"Error obteniendo ambientes: {e}")
                import traceback
                traceback.print_exc()
            
            content_layout.addWidget(environments_container)
            content_layout.addStretch()
            
            root_layout.addWidget(content_widget, 1)
            
            # Mostrar el diálogo
            dlg.show()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error abriendo selector de ambientes:\n{e}")

    def _get_available_environments(self):
        """Obtiene los ambientes disponibles de la base de datos"""
        try:
            from src.utils.utils import get_available_environments
            return get_available_environments()
        except Exception as e:
            print(f"❌ Error obteniendo ambientes: {e}")
            return []

    def _select_environment(self, environment_id, environment_name):
        # Mostrar mensaje de confirmación más simple
        QMessageBox.information(
            self.parent,
            "AMBIENTE SELECCIONADO",
            f"Ambiente seleccionado: {environment_name}\n\nEl sistema está configurando la limpieza para este ambiente."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la limpieza del ambiente seleccionado
        print(f"✅ Ambiente seleccionado: {environment_name} (ID: {environment_id})")
