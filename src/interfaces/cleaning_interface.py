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
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QFont, QPixmap
import os
from src.interfaces.dialog_utils import CleanCloseDialog

class CleaningInterface:
    def __init__(self, parent):
        self.parent = parent

    def show_cleaning_interface(self):
        try:
            # Colores consistentes con las otras interfaces (basados en el HTML de Stitch)
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            HEADER_DARK = "#1F2937"  # Cambiado según HTML
            CARD_BG = "#ffffff"
            GREEN_LIGHT = "#10b981"
            YELLOW_LIGHT = "#fbbf24"

            cleaning_win = CleanCloseDialog(self.parent)
            cleaning_win.setWindowTitle("Interfaz de Aseo - Sistema CEFA")
            cleaning_win.setModal(False)
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            cleaning_win.showFullScreen()
            
            cleaning_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")

            root_layout = QVBoxLayout(cleaning_win)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)

            # Header simplificado (oculto para mantener la interfaz limpia)
            # header = QWidget(cleaning_win)
            # header.setFixedHeight(64)  # h-16 = 64px
            # header.setStyleSheet(f"background-color: {HEADER_DARK}; border: none;")
            # header_layout = QHBoxLayout(header)
            # header_layout.setContentsMargins(16, 0, 16, 0)  # px-4 sm:px-6 lg:px-8
            # header_layout.setSpacing(12)  # gap-3
            # 
            # # Icono y título del header
            # header_left = QWidget(header)
            # header_left_layout = QHBoxLayout(header_left)
            # header_left_layout.setContentsMargins(0, 0, 0, 0)
            # header_left_layout.setSpacing(12)
            # 
            # # Icono de limpieza (escobaazul.png)
            # header_icon = QLabel(header_left)
            # header_icon.setAlignment(Qt.AlignCenter)
            # icon_path = "images/escobaazul.png"
            # if not os.path.isabs(icon_path):
            #     icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            # if os.path.exists(icon_path):
            #     pix = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     header_icon.setPixmap(pix)
            #     header_icon.setFixedSize(pix.width(), pix.height())
            #     header_icon.setStyleSheet("background-color: transparent; border: none; padding: 0px; margin: 0px;")
            # else:
            #     # Fallback si la imagen no se carga
            #     header_icon.setText("🧹")
            #     header_icon.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 24px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            # header_left_layout.addWidget(header_icon)
            # 
            # # Título del header - SIN ENCAPSULACIÓN
            # header_title = QLabel("INTERFAZ DE ASEO - SISTEMA CEFA", header_left)
            # header_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            # header_title.setWordWrap(False)
            # header_title.setTextFormat(Qt.PlainText)
            # header_title.setOpenExternalLinks(False)
            # header_title.setMinimumWidth(0)
            # header_title.setMaximumWidth(16777215)
            # header_title_font = header_title.font()
            # header_title_font.setPointSize(16)  # text-base sm:text-lg
            # header_title_font.setBold(True)
            # header_title.setFont(header_title_font)
            # header_title_fm = QFontMetrics(header_title_font)
            # header_title.setMinimumWidth(header_title_fm.horizontalAdvance("INTERFAZ DE ASEO - SISTEMA CEFA"))
            # header_title.setStyleSheet(
            #     f"color: white; font-size: 16px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            # )
            # header_left_layout.addWidget(header_title)
            # 
            # header_layout.addWidget(header_left)
            # header_layout.addStretch()

            # root_layout.addWidget(header)

            # Contenido principal centrado
            main_container = QWidget(cleaning_win)
            main_container.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            main_layout = QVBoxLayout(main_container)
            main_layout.setContentsMargins(40, 40, 40, 40)
            main_layout.setAlignment(Qt.AlignCenter)
            
            # Contenedor central
            center_widget = QWidget(main_container)
            center_widget.setMaximumWidth(600)
            center_layout = QVBoxLayout(center_widget)
            center_layout.setSpacing(30)
            center_layout.setAlignment(Qt.AlignCenter)
            
            # Título principal - MUY GRANDE Y CLARO
            title = QLabel("🧹 Gestión de Aseo", center_widget)
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 36px; "
                f"font-weight: 700; "
                f"font-family: 'Segoe UI', Arial, sans-serif;"
            )
            center_layout.addWidget(title)
            
            # Icono grande
            icon_label = QLabel(center_widget)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_path = "images/escobablanca.png"
            if not os.path.isabs(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(pix)
                icon_label.setFixedSize(pix.width(), pix.height())
                icon_label.setStyleSheet("background-color: transparent; border: none; padding: 0px; margin: 0px;")
            else:
                # Fallback si la imagen no se carga
                icon_label.setText("🧹")
                icon_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 80px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            center_layout.addWidget(icon_label, 0, Qt.AlignCenter)
            
            # Instrucción MUY CLARA
            instruction = QLabel("Seleccione un ambiente\npara comenzar la limpieza", center_widget)
            instruction.setAlignment(Qt.AlignCenter)
            instruction.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 24px; "
                f"font-weight: 600; "
                f"font-family: 'Segoe UI', Arial, sans-serif; "
                f"line-height: 1.4;"
            )
            center_layout.addWidget(instruction)
            
            # Botón Seleccionar Ambiente GRANDE
            select_btn = QPushButton("🏢 Seleccionar Ambiente", center_widget)
            select_btn.setCursor(Qt.PointingHandCursor)
            select_btn.setMinimumHeight(70)
            select_btn.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: {PRIMARY_COLOR}; "
                f"  color: white; "
                f"  border: none; "
                f"  border-radius: 12px; "
                f"  font-size: 20px; "
                f"  font-weight: 700; "
                f"  font-family: 'Segoe UI', Arial, sans-serif; "
                f"  padding: 20px;"
                f"}}"
                f"QPushButton:hover {{"
                f"  background-color: #0E5AA7;"
                f"}}"
                f"QPushButton:pressed {{"
                f"  background-color: #0A4A8A;"
                f"}}"
            )
            select_btn.clicked.connect(self._open_environment_selector)
            center_layout.addWidget(select_btn)
            
            main_layout.addWidget(center_widget)
            root_layout.addWidget(main_container, 1)

            print("✅ Interfaz de aseo simplificada mostrada en pantalla completa")
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
            dlg.setModal(False)
            dlg.setWindowTitle("AMBIENTES DISPONIBLES")
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            dlg.showFullScreen()
            dlg.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            
            # Layout principal
            root_layout = QVBoxLayout(dlg)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)
            
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
            title_label = QLabel("🏢 Seleccionar Ambiente", content_widget)
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
            
            # Contenedor de lista de ambientes
            environments_container = QWidget(content_widget)
            environments_container.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-radius: 12px; "
                f"padding: 20px;"
            )
            environments_layout = QVBoxLayout(environments_container)
            environments_layout.setContentsMargins(20, 20, 20, 20)
            environments_layout.setSpacing(15)
            
            # Obtener ambientes de la base de datos
            try:
                from src.utils.db_utils import db_connect, get_environments
                env_ids_with_keys = {}
                envs_list = get_environments()
                envs = {e['id']: e for e in envs_list} if isinstance(envs_list, list) else {}
                with db_connect() as cnx:
                    cur = cnx.cursor(dictionary=True)
                    cur.execute("SELECT id, codigo_llave, descripcion, ambiente_id, estado, angulo_grados FROM llaves WHERE activo = 1 AND estado IN ('DISPONIBLE','ASIGNADA')")
                    for row in cur.fetchall():
                        a_id = row.get('ambiente_id')
                        if a_id:
                            env_ids_with_keys.setdefault(a_id, []).append(row)
            except Exception:
                from src.utils.db_utils import get_environments
                keys = get_available_keys()
                envs = {e['id']: e for e in get_environments()} if isinstance(get_environments(), list) else {}
                env_ids_with_keys = {}
                for k in keys:
                    a_id = k.get('ambiente_id')
                    if a_id:
                        env_ids_with_keys.setdefault(a_id, []).append(k)
            
            if not env_ids_with_keys:
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
                environments_layout.addWidget(empty_text)
            else:
                # Lista de ambientes con botones grandes
                for env_id, klist in env_ids_with_keys.items():
                    info = envs.get(env_id, {})
                    name = info.get('nombre', f"Ambiente {env_id}")
                    
                    # Botón para seleccionar ambiente
                    env_btn = QPushButton(name, environments_container)
                    env_btn.setMinimumHeight(60)
                    env_btn.setCursor(Qt.PointingHandCursor)
                    env_btn.setStyleSheet(
                        f"QPushButton {{"
                        f"background-color: {PRIMARY_COLOR}; "
                        f"color: white; "
                        f"border: none; "
                        f"border-radius: 8px; "
                        f"padding: 15px; "
                        f"font-size: 16px; "
                        f"font-weight: 500; "
                        f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                        f"margin: 5px;"
                        f"}}"
                        f"QPushButton:hover {{"
                        f"background-color: #0E5AA7; "
                        f"}}"
                        f"QPushButton:pressed {{"
                        f"background-color: #0A4A8A; "
                        f"}}"
                    )
                    env_btn.clicked.connect(lambda checked, eid=env_id, n=name: self._select_environment(eid, n))
                    environments_layout.addWidget(env_btn)
            
            content_layout.addWidget(environments_container)
            content_layout.addStretch()
            
            root_layout.addWidget(content_widget, 1)
            
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
            "🧹 AMBIENTE SELECCIONADO",
            f"Ambiente seleccionado: {environment_name}\n\nEl sistema está configurando la limpieza para este ambiente."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la limpieza del ambiente seleccionado
        print(f"✅ Ambiente seleccionado: {environment_name} (ID: {environment_id})")
