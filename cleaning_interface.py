#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleaning_interface.py
- Interfaz de aseo (PySide6)
"""

import styles
from config import *
from utils import *
from db_utils import get_available_keys, get_environments
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

            cleaning_win = QDialog(self.parent)
            cleaning_win.setWindowTitle("Interfaz de Aseo - Sistema CEFA")
            cleaning_win.setModal(False)
            try:
                w, h = [int(x) for x in ADMIN_WINDOW_SIZE.lower().split('x')]
                cleaning_win.resize(max(w, 1000), max(h, 700))
            except Exception:
                cleaning_win.resize(1000, 700)
            cleaning_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")

            root_layout = QVBoxLayout(cleaning_win)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)

            # Header oscuro (sticky top)
            header = QWidget(cleaning_win)
            header.setFixedHeight(64)  # h-16 = 64px
            header.setStyleSheet(f"background-color: {HEADER_DARK}; border: none;")
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(16, 0, 16, 0)  # px-4 sm:px-6 lg:px-8
            header_layout.setSpacing(12)  # gap-3

            # Icono y título del header
            header_left = QWidget(header)
            header_left_layout = QHBoxLayout(header_left)
            header_left_layout.setContentsMargins(0, 0, 0, 0)
            header_left_layout.setSpacing(12)
            
            # Icono de limpieza (escobaazul.png)
            header_icon = QLabel(header_left)
            header_icon.setAlignment(Qt.AlignCenter)
            icon_path = "images/escobaazul.png"
            if not os.path.isabs(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                header_icon.setPixmap(pix)
                header_icon.setFixedSize(pix.width(), pix.height())
                header_icon.setStyleSheet("background-color: transparent; border: none; padding: 0px; margin: 0px;")
            else:
                # Fallback si la imagen no se carga
                header_icon.setText("🧹")
                header_icon.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 24px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            header_left_layout.addWidget(header_icon)

            # Título del header - SIN ENCAPSULACIÓN
            header_title = QLabel("INTERFAZ DE ASEO - SISTEMA CEFA", header_left)
            header_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            header_title.setWordWrap(False)
            header_title.setTextFormat(Qt.PlainText)
            header_title.setOpenExternalLinks(False)
            header_title.setMinimumWidth(0)
            header_title.setMaximumWidth(16777215)
            header_title_font = header_title.font()
            header_title_font.setPointSize(16)  # text-base sm:text-lg
            header_title_font.setBold(True)
            header_title.setFont(header_title_font)
            header_title_fm = QFontMetrics(header_title_font)
            header_title.setMinimumWidth(header_title_fm.horizontalAdvance("INTERFAZ DE ASEO - SISTEMA CEFA"))
            header_title.setStyleSheet(
                f"color: white; font-size: 16px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            header_left_layout.addWidget(header_title)
            
            header_layout.addWidget(header_left)
            header_layout.addStretch()

            root_layout.addWidget(header)

            # Contenido principal con scroll
            scroll_area = QScrollArea(cleaning_win)
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("border: none; background-color: transparent;")
            scroll_area.setFrameShape(QFrame.NoFrame)

            main_content = QWidget()
            main_content.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            main_layout = QVBoxLayout(main_content)
            main_layout.setContentsMargins(16, 16, 16, 16)  # p-4 sm:p-6 lg:p-8
            main_layout.setSpacing(32)  # gap-8

            # Welcome Card (flex horizontal en desktop)
            welcome_card = QWidget(main_content)
            welcome_card.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-radius: 12px; "
                f"padding: 24px;"  # p-6 sm:p-8
            )
            welcome_layout = QHBoxLayout(welcome_card)
            welcome_layout.setContentsMargins(0, 0, 0, 0)
            welcome_layout.setSpacing(24)  # gap-6

            # Icono grande (mop) - izquierda
            welcome_icon_container = QWidget(welcome_card)
            welcome_icon_container.setStyleSheet(f"background-color: transparent;")
            welcome_icon_layout = QVBoxLayout(welcome_icon_container)
            welcome_icon_layout.setContentsMargins(0, 0, 0, 0)
            welcome_icon_layout.setAlignment(Qt.AlignCenter)
            
            welcome_icon_label = QLabel(welcome_icon_container)
            welcome_icon_label.setAlignment(Qt.AlignCenter)
            icon_path = "images/escobablanca.png"
            if not os.path.isabs(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                welcome_icon_label.setPixmap(pix)
                welcome_icon_label.setFixedSize(pix.width(), pix.height())
                welcome_icon_label.setStyleSheet("background-color: transparent; border: none; padding: 0px; margin: 0px;")
            else:
                # Fallback si la imagen no se carga
                welcome_icon_label.setText("🧹")
                welcome_icon_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 72px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            welcome_icon_layout.addWidget(welcome_icon_label)

            welcome_layout.addWidget(welcome_icon_container, 0, Qt.AlignCenter)

            # Texto de bienvenida - derecha
            welcome_text_block = QVBoxLayout()
            welcome_text_block.setContentsMargins(0, 0, 0, 0)
            welcome_text_block.setSpacing(8)  # gap-2

            # Título "Gestión de Aseo" - SIN ENCAPSULACIÓN
            welcome_title = QLabel("Gestión de Aseo", welcome_card)
            welcome_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            welcome_title.setWordWrap(False)
            welcome_title.setTextFormat(Qt.PlainText)
            welcome_title.setOpenExternalLinks(False)
            welcome_title.setMinimumWidth(0)
            welcome_title.setMaximumWidth(16777215)
            welcome_title_font = welcome_title.font()
            welcome_title_font.setPointSize(30)  # text-2xl sm:text-3xl
            welcome_title_font.setBold(True)
            welcome_title.setFont(welcome_title_font)
            welcome_title_fm = QFontMetrics(welcome_title_font)
            welcome_title.setMinimumWidth(welcome_title_fm.horizontalAdvance("Gestión de Aseo"))
            welcome_title.setStyleSheet(
                f"color: {PRIMARY_COLOR}; font-size: 30px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            welcome_text_block.addWidget(welcome_title)

            # Subtítulo - SIN ENCAPSULACIÓN
            welcome_subtitle = QLabel(
                "Este es el centro de control para todas las tareas de limpieza. Desde aquí puede seleccionar ambientes para limpiar y ver el estado actual.",
                welcome_card
            )
            welcome_subtitle.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            welcome_subtitle.setWordWrap(True)
            welcome_subtitle.setTextFormat(Qt.PlainText)
            welcome_subtitle.setOpenExternalLinks(False)
            welcome_subtitle_font = welcome_subtitle.font()
            welcome_subtitle_font.setPointSize(16)  # text-base
            welcome_subtitle.setFont(welcome_subtitle_font)
            welcome_subtitle.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; font-size: 16px; font-weight: 400; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            welcome_text_block.addWidget(welcome_subtitle)

            welcome_layout.addLayout(welcome_text_block, 1)
            welcome_layout.addStretch()

            main_layout.addWidget(welcome_card)

            # Main Action Card - Seleccionar Ambiente
            action_card = QWidget(main_content)
            action_card.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-radius: 12px;"
            )
            action_layout = QVBoxLayout(action_card)
            action_layout.setContentsMargins(40, 32, 40, 32)  # left, top, right, bottom - Más espacio alrededor del contenido
            action_layout.setSpacing(24)  # gap-6

            # Header con icono y título
            action_header = QHBoxLayout()
            action_header.setContentsMargins(0, 0, 0, 0)
            action_header.setSpacing(16)  # gap-4

            # Icono seleccionarambiente (sin cuadro, solo la imagen)
            action_icon_label = QLabel(action_card)
            action_icon_label.setAlignment(Qt.AlignCenter)
            icon_path = "images/seleccionarambiente.png"
            if not os.path.isabs(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                action_icon_label.setPixmap(pix)
                action_icon_label.setFixedSize(pix.width(), pix.height())
                action_icon_label.setStyleSheet("background-color: transparent; border: none; padding: 0px; margin: 0px;")
            else:
                # Fallback si la imagen no se carga
                action_icon_label.setText("🏢")
                action_icon_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 24px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            
            action_header.addWidget(action_icon_label)

            # Título "Seleccionar Ambiente para Limpieza" - SIN ENCAPSULACIÓN
            action_title = QLabel("Seleccionar Ambiente para Limpieza", action_card)
            action_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            action_title.setWordWrap(False)
            action_title.setTextFormat(Qt.PlainText)
            action_title.setOpenExternalLinks(False)
            action_title.setMinimumWidth(0)
            action_title.setMaximumWidth(16777215)
            action_title_font = action_title.font()
            action_title_font.setPointSize(20)  # text-xl sm:text-2xl
            action_title_font.setBold(True)
            action_title.setFont(action_title_font)
            action_title_fm = QFontMetrics(action_title_font)
            action_title.setMinimumWidth(action_title_fm.horizontalAdvance("Seleccionar Ambiente para Limpieza"))
            action_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; font-size: 20px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            action_header.addWidget(action_title)
            action_header.addStretch()

            action_layout.addLayout(action_header)

            # Descripción - SIN ENCAPSULACIÓN
            action_desc = QLabel(
                "Haga clic en el botón a continuación para ver la lista de ambientes disponibles y seleccionar uno para comenzar el proceso de limpieza.",
                action_card
            )
            action_desc.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            action_desc.setWordWrap(True)
            action_desc.setTextFormat(Qt.PlainText)
            action_desc.setOpenExternalLinks(False)
            action_desc_font = action_desc.font()
            action_desc_font.setPointSize(16)  # text-base
            action_desc.setFont(action_desc_font)
            action_desc.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; font-size: 16px; font-weight: 400; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            action_layout.addWidget(action_desc)

            # Botón Seleccionar Ambiente
            select_btn = QPushButton("Seleccionar Ambiente", action_card)
            select_btn.setCursor(Qt.PointingHandCursor)
            select_btn.setMinimumHeight(48)  # h-12
            select_btn.setMinimumWidth(140)  # min-w-[140px]
            select_btn.setStyleSheet(
                f"background-color: {PRIMARY_COLOR}; "
                f"color: white; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 12px 24px; "
                f"font-size: 16px; "
                f"font-weight: 500; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            select_btn.clicked.connect(self._open_environment_selector)
            action_layout.addWidget(select_btn, 0, Qt.AlignLeft)

            main_layout.addWidget(action_card)

            # Sección "Ambientes disponibles para limpieza"
            list_section = QWidget(main_content)
            list_section_layout = QVBoxLayout(list_section)
            list_section_layout.setContentsMargins(0, 0, 0, 0)
            list_section_layout.setSpacing(16)  # gap-4

            # Título de la sección
            list_title = QLabel("Ambientes disponibles para limpieza", list_section)
            list_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            list_title.setWordWrap(False)
            list_title.setTextFormat(Qt.PlainText)
            list_title.setOpenExternalLinks(False)
            list_title.setMinimumWidth(0)
            list_title.setMaximumWidth(16777215)
            list_title_font = list_title.font()
            list_title_font.setPointSize(20)  # text-xl sm:text-2xl
            list_title_font.setBold(True)
            list_title.setFont(list_title_font)
            list_title_fm = QFontMetrics(list_title_font)
            list_title.setMinimumWidth(list_title_fm.horizontalAdvance("Ambientes disponibles para limpieza"))
            list_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; font-size: 20px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 8px; margin: 0px;"
            )
            list_section_layout.addWidget(list_title)

            # Lista de ambientes
            list_container = QWidget(list_section)
            list_container.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-radius: 12px;"
            )
            list_container_layout = QVBoxLayout(list_container)
            list_container_layout.setContentsMargins(0, 0, 0, 0)
            list_container_layout.setSpacing(0)

            # Obtener ambientes de la base de datos
            environments = self._get_available_environments()
            if not environments:
                # Mensaje si no hay ambientes
                no_env_label = QLabel("No hay ambientes disponibles en este momento.", list_container)
                no_env_label.setAlignment(Qt.AlignCenter)
                no_env_label.setStyleSheet(
                    f"color: {TEXT_GRAY_LIGHT}; font-size: 14px; padding: 24px;"
                )
                list_container_layout.addWidget(no_env_label)
            else:
                # Mostrar primeros 3 ambientes como ejemplo (similar al HTML)
                sample_environments = [
                    ("Salón 101", "Piso 1 - Limpieza requerida", "Disponible"),
                    ("Oficina 205", "Piso 2 - Limpieza programada", "Ocupado"),
                    ("Auditorio Principal", "Planta Baja - Limpieza requerida", "Disponible"),
                ]
                
                for i, (env_name, env_desc, env_status) in enumerate(sample_environments):
                    env_item = QWidget(list_container)
                    env_item.setMinimumHeight(72)  # min-h-[72px]
                    env_item.setStyleSheet(
                        f"background-color: transparent; "
                        f"border-bottom: 1px solid {BORDER_COLOR};"
                    )
                    if i == len(sample_environments) - 1:
                        # Último item sin borde inferior
                        env_item.setStyleSheet(f"background-color: transparent;")
                    
                    env_item_layout = QHBoxLayout(env_item)
                    env_item_layout.setContentsMargins(16, 16, 16, 16)  # p-4
                    env_item_layout.setSpacing(16)  # gap-4

                    # Icono
                    item_icon_container = QWidget(env_item)
                    item_icon_container.setFixedSize(48, 48)  # size-12
                    item_icon_container.setStyleSheet(
                        f"background-color: rgba(19, 109, 236, 0.2); "
                        f"border-radius: 8px;"
                    )
                    item_icon_layout = QVBoxLayout(item_icon_container)
                    item_icon_layout.setContentsMargins(0, 0, 0, 0)
                    item_icon_layout.setAlignment(Qt.AlignCenter)
                    
                    item_icon = QLabel(item_icon_container)
                    item_icon.setAlignment(Qt.AlignCenter)
                    item_icon.setText("🏢")  # meeting_room emoji
                    item_icon.setStyleSheet(f"color: {PRIMARY_COLOR}; font-size: 24px; background-color: transparent; border: none; padding: 0px; margin: 0px;")
                    item_icon_layout.addWidget(item_icon)
                    
                    env_item_layout.addWidget(item_icon_container)

                    # Información del ambiente
                    env_info_layout = QVBoxLayout()
                    env_info_layout.setContentsMargins(0, 0, 0, 0)
                    env_info_layout.setSpacing(4)

                    env_name_label = QLabel(env_name, env_item)
                    env_name_label.setStyleSheet(
                        f"color: {TEXT_GRAY_DARK}; font-size: 16px; font-weight: 500; background-color: transparent; border: none; padding: 0px; margin: 0px;"
                    )
                    env_info_layout.addWidget(env_name_label)

                    env_desc_label = QLabel(env_desc, env_item)
                    env_desc_label.setStyleSheet(
                        f"color: {TEXT_GRAY_LIGHT}; font-size: 14px; font-weight: 400; background-color: transparent; border: none; padding: 0px; margin: 0px;"
                    )
                    env_info_layout.addWidget(env_desc_label)

                    env_item_layout.addLayout(env_info_layout, 1)

                    # Estado (chip)
                    status_chip = QLabel(env_item)
                    status_chip.setAlignment(Qt.AlignCenter)
                    status_chip.setText(env_status)
                    if env_status == "Disponible":
                        status_chip.setStyleSheet(
                            f"background-color: rgba(16, 185, 129, 0.1); "  # green-100
                            f"color: #065f46; "  # green-800
                            f"border-radius: 9999px; "
                            f"padding: 4px 12px; "
                            f"font-size: 14px; "
                            f"font-weight: 500;"
                        )
                    else:
                        status_chip.setStyleSheet(
                            f"background-color: rgba(251, 191, 36, 0.1); "  # yellow-100
                            f"color: #92400e; "  # yellow-800
                            f"border-radius: 9999px; "
                            f"padding: 4px 12px; "
                            f"font-size: 14px; "
                            f"font-weight: 500;"
                        )
                    env_item_layout.addWidget(status_chip, 0, Qt.AlignRight)

                    list_container_layout.addWidget(env_item)

            list_section_layout.addWidget(list_container)
            main_layout.addWidget(list_section)

            # Footer
            footer = QWidget(cleaning_win)
            footer.setFixedHeight(64)  # h-16
            footer.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-top: 1px solid {BORDER_COLOR};"
            )
            footer_layout = QHBoxLayout(footer)
            footer_layout.setContentsMargins(16, 0, 16, 0)  # px-4 sm:px-6 lg:px-8
            footer_layout.addStretch()

            # Botón Cerrar
            close_btn = QPushButton("Cerrar", footer)
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setMinimumHeight(40)  # h-10
            close_btn.setMinimumWidth(100)  # min-w-[100px]
            close_btn.setStyleSheet(
                f"background-color: #e5e7eb; "  # bg-gray-200
                f"color: {TEXT_GRAY_DARK}; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 8px 20px; "
                f"font-size: 14px; "
                f"font-weight: 500; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            close_btn.clicked.connect(cleaning_win.close)
            footer_layout.addWidget(close_btn)

            scroll_area.setWidget(main_content)
            root_layout.addWidget(scroll_area, 1)
            
            root_layout.addWidget(footer)

            styles.center_window(cleaning_win)
            cleaning_win.show()

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
            
            # Crear modal
            dlg = QDialog(self.parent)
            dlg.setModal(True)
            dlg.setWindowTitle("AMBIENTES DISPONIBLES")
            dlg.resize(900, 620)
            dlg.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            
            # Layout principal
            root_layout = QVBoxLayout(dlg)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)
            
            # Header del modal
            header = QWidget(dlg)
            header.setFixedHeight(60)
            header.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-bottom: 1px solid {BORDER_COLOR};"
            )
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(24, 16, 24, 16)
            header_layout.setSpacing(16)
            
            # Título con icono
            title_container = QWidget(header)
            title_layout = QHBoxLayout(title_container)
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.setSpacing(12)
            
            icon_label = QLabel("🏢", header)
            icon_label.setStyleSheet("font-size: 24px; background-color: transparent;")
            title_layout.addWidget(icon_label)
            
            title_label = QLabel("AMBIENTES DISPONIBLES", header)
            title_label.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 18px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            title_layout.addWidget(title_label)
            
            header_layout.addWidget(title_container)
            header_layout.addStretch()
            
            # Botón cerrar (X)
            close_btn = QPushButton("✕", header)
            close_btn.setFixedSize(32, 32)
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setStyleSheet(
                f"QPushButton {{"
                f"background-color: {BG_LIGHT_HTML}; "
                f"color: {TEXT_GRAY_LIGHT}; "
                f"border: none; "
                f"border-radius: 8px; "
                f"font-size: 18px; "
                f"font-weight: 500;"
                f"}}"
                f"QPushButton:hover {{"
                f"background-color: #E5E7EB; "
                f"color: {TEXT_GRAY_DARK};"
                f"}}"
            )
            close_btn.clicked.connect(dlg.close)
            header_layout.addWidget(close_btn)
            
            root_layout.addWidget(header)
            
            # Área de contenido scrollable
            scroll_area = QScrollArea(dlg)
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameShape(QFrame.NoFrame)
            scroll_area.setStyleSheet("border: none; background-color: transparent;")
            
            content_widget = QWidget()
            content_widget.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(24, 24, 24, 24)
            content_layout.setSpacing(24)
            
            # Subtítulo/Instrucción
            subtitle_label = QLabel("Seleccione un ambiente para gestionar sus llaves disponibles", content_widget)
            subtitle_label.setAlignment(Qt.AlignHCenter)
            subtitle_label.setWordWrap(True)
            subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            subtitle_label.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; "
                f"font-size: 14px; "
                f"font-weight: 400; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            content_layout.addWidget(subtitle_label)
            
            # Construir lista de ambientes con llaves disponibles
            try:
                from db_utils import db_connect, get_environments
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
                from db_utils import get_environments
                keys = get_available_keys()
                envs = {e['id']: e for e in get_environments()} if isinstance(get_environments(), list) else {}
                env_ids_with_keys = {}
                for k in keys:
                    a_id = k.get('ambiente_id')
                    if a_id:
                        env_ids_with_keys.setdefault(a_id, []).append(k)
            
            # Contenedor de lista de ambientes
            environments_container = QWidget(content_widget)
            environments_layout = QVBoxLayout(environments_container)
            environments_layout.setContentsMargins(0, 0, 0, 0)
            environments_layout.setSpacing(12)
            
            if not env_ids_with_keys:
                # Estado vacío
                empty_card = QWidget(content_widget)
                empty_card.setStyleSheet(
                    f"background-color: {CARD_BG}; "
                    f"border: 1px solid {BORDER_COLOR}; "
                    f"border-radius: 12px;"
                )
                empty_layout = QVBoxLayout(empty_card)
                empty_layout.setContentsMargins(40, 40, 40, 40)
                empty_layout.setSpacing(16)
                
                empty_icon = QLabel("🔑", empty_card)
                empty_icon.setAlignment(Qt.AlignHCenter)
                empty_icon.setStyleSheet("font-size: 48px; background-color: transparent;")
                empty_layout.addWidget(empty_icon)
                
                empty_text = QLabel("No hay llaves disponibles en este momento.", empty_card)
                empty_text.setAlignment(Qt.AlignHCenter)
                empty_text.setWordWrap(True)
                empty_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                empty_text.setStyleSheet(
                    f"color: {TEXT_GRAY_LIGHT}; "
                    f"font-size: 16px; "
                    f"font-weight: 400; "
                    f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
                )
                empty_layout.addWidget(empty_text)
                
                environments_layout.addWidget(empty_card)
            else:
                # Lista de ambientes
                for env_id, klist in env_ids_with_keys.items():
                    info = envs.get(env_id, {})
                    name = info.get('nombre', f"Ambiente {env_id}")
                    
                    # Tarjeta de ambiente
                    env_card = QWidget(environments_container)
                    env_card.setStyleSheet(
                        f"background-color: {CARD_BG}; "
                        f"border: 1px solid {BORDER_COLOR}; "
                        f"border-radius: 12px;"
                    )
                    env_card.setMinimumHeight(72)
                    
                    card_layout = QHBoxLayout(env_card)
                    card_layout.setContentsMargins(20, 20, 20, 20)
                    card_layout.setSpacing(16)
                    
                    # Icono de edificio
                    icon_container = QWidget(env_card)
                    icon_container.setFixedSize(56, 56)
                    icon_container.setStyleSheet(
                        f"background-color: #E3F2FD; "  # Azul muy claro (10% del primario)
                        f"border-radius: 8px;"
                    )
                    icon_layout = QVBoxLayout(icon_container)
                    icon_layout.setContentsMargins(0, 0, 0, 0)
                    
                    env_icon = QLabel("🏢", icon_container)
                    env_icon.setAlignment(Qt.AlignCenter)
                    env_icon.setStyleSheet(
                        f"color: {PRIMARY_COLOR}; "
                        f"font-size: 28px; "
                        f"background-color: transparent;"
                    )
                    icon_layout.addWidget(env_icon)
                    
                    card_layout.addWidget(icon_container)
                    
                    # Información del ambiente - sin contenedor intermedio para que el texto fluya libremente
                    info_layout = QVBoxLayout()
                    info_layout.setContentsMargins(0, 0, 0, 0)
                    info_layout.setSpacing(4)
                    
                    env_name = QLabel(name, env_card)
                    env_name.setWordWrap(True)
                    env_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    env_name.setStyleSheet(
                        f"color: {TEXT_GRAY_DARK}; "
                        f"font-size: 16px; "
                        f"font-weight: 700; "
                        f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
                    )
                    info_layout.addWidget(env_name)
                    
                    env_detail = QLabel(f"{len(klist)} llaves disponibles o asignadas sin reclamar", env_card)
                    env_detail.setWordWrap(True)
                    env_detail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    env_detail.setStyleSheet(
                        f"color: {TEXT_GRAY_LIGHT}; "
                        f"font-size: 13px; "
                        f"font-weight: 400; "
                        f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
                    )
                    info_layout.addWidget(env_detail)
                    
                    # Agregar el layout directamente al card_layout sin widget intermedio
                    card_layout.addLayout(info_layout, 1)
                    
                    # Botón "Seleccionar" (para Aseo)
                    select_btn = QPushButton("Seleccionar", env_card)
                    select_btn.setMinimumHeight(40)
                    select_btn.setMinimumWidth(100)
                    select_btn.setCursor(Qt.PointingHandCursor)
                    select_btn.setStyleSheet(
                        f"QPushButton {{"
                        f"background-color: {PRIMARY_COLOR}; "
                        f"color: white; "
                        f"border: none; "
                        f"border-radius: 8px; "
                        f"padding: 10px 20px; "
                        f"font-size: 14px; "
                        f"font-weight: 500; "
                        f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
                        f"}}"
                        f"QPushButton:hover {{"
                        f"background-color: #0E5AA7; "
                        f"}}"
                    )
                    select_btn.clicked.connect(lambda checked, eid=env_id, n=name: self._select_environment(eid, n))
                    card_layout.addWidget(select_btn)
                    
                    environments_layout.addWidget(env_card)
            
            content_layout.addWidget(environments_container)
            content_layout.addStretch()
            
            scroll_area.setWidget(content_widget)
            root_layout.addWidget(scroll_area, 1)
            
            # Centrar y mostrar
            styles.center_window(dlg)
            dlg.show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error abriendo selector de ambientes:\n{e}")

    def _get_available_environments(self):
        """Obtiene los ambientes disponibles de la base de datos"""
        try:
            from utils import get_available_environments
            return get_available_environments()
        except Exception as e:
            print(f"❌ Error obteniendo ambientes: {e}")
            return []

    def _select_environment(self, environment_id, environment_name):
        QMessageBox.information(
            self.parent,
            "🧹 AMBIENTE SELECCIONADO",
            f"Ambiente seleccionado: {environment_name}\n\nID: {environment_id}\n\nEl sistema está configurando la limpieza para este ambiente.\nPor favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la limpieza del ambiente seleccionado
        print(f"✅ Ambiente seleccionado: {environment_name} (ID: {environment_id})")
