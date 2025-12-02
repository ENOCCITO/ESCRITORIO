#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instructor_interface.py
- Interfaz de instructor (PySide6)
"""

from src.utils import styles
from src.config.config import *
from src.utils.utils import *
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox, QPushButton, QApplication, QDialog, QScrollArea, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QFont, QPixmap
import os
from src.core.key_manager import KeyManager
from src.core.fingerprint_validator import FingerprintValidator
from src.utils.db_utils import get_instructor_week_schedule, get_personal_by_id, db_connect
from typing import List, Dict, Any
from src.interfaces.dialog_utils import CleanCloseDialog

class InstructorInterface:
    def __init__(self, parent, user: dict | None = None):
        self.parent = parent
        self._km = KeyManager()
        # Si viene el usuario autenticado, establecerlo para no pedir huella otra vez
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass
        self._schedule_data = None
        self._status_by_day = {}
        
    def show_instructor_interface(self):
        try:
            # Colores exactos del HTML de Stitch AI
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            HEADER_DARK = "#2D3748"  # Exacto del HTML
            CARD_BG = "#ffffff"
            
            from PySide6.QtWidgets import QScrollArea, QFrame
            instructor_win = CleanCloseDialog(self.parent)
            instructor_win.setWindowTitle("Interfaz de Instructor - Sistema CEFA")
            instructor_win.setModal(False)
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            instructor_win.showFullScreen()
            
            instructor_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            
            root_layout = QVBoxLayout(instructor_win)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)
            
            # Header oscuro fijo (exacto del HTML: bg-[#2D3748])
            header = QWidget(instructor_win)
            header.setFixedHeight(68)  # py-3 = 12px top/bottom = 48px + contenido
            header.setStyleSheet(
                f"background-color: {HEADER_DARK}; "
                f"border: none;"
            )
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(24, 12, 24, 12)  # px-6 = 24px, py-3 = 12px
            header_layout.setSpacing(16)
            
            # Logo/ícono (SVG convertido a texto simple)
            logo_label = QLabel("⚡", header)  # Usar emoji como representación del logo
            logo_label.setFixedSize(24, 24)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet(
                f"color: white; "
                f"font-size: 24px;"
            )
            header_layout.addWidget(logo_label)
            
            # Título del header - SIN ENCAPSULACIÓN
            header_title = QLabel("INTERFAZ DE INSTRUCTOR - SISTEMA CEFA", header)
            header_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            header_title.setWordWrap(False)
            header_title.setTextFormat(Qt.PlainText)
            header_title.setOpenExternalLinks(False)
            header_title.setMinimumWidth(0)
            header_title.setMaximumWidth(16777215)
            header_title.setMinimumHeight(0)
            header_font = header_title.font()
            header_font.setPointSize(18)
            header_font.setBold(True)
            header_title.setFont(header_font)
            header_fm = QFontMetrics(header_font)
            header_text_width = header_fm.horizontalAdvance("INTERFAZ DE INSTRUCTOR - SISTEMA CEFA")
            header_title.setMinimumWidth(header_text_width)
            header_title.setStyleSheet(
                f"color: white; "
                f"font-size: 18px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            header_layout.addWidget(header_title)
            header_layout.addStretch()
            
            # Botón cerrar (X) para volver a la pantalla principal
            close_btn = QPushButton("✕", header)
            close_btn.setFixedSize(40, 40)
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setStyleSheet(
                "QPushButton {"
                "background-color: #404854; "
                "color: white; "
                "border: none; "
                "border-radius: 6px; "
                "font-size: 20px; "
                "font-weight: 600;"
                "}"
                "QPushButton:hover {"
                "background-color: #505864; "
                "}"
            )
            close_btn.clicked.connect(instructor_win.close)
            header_layout.addWidget(close_btn)
            
            root_layout.addWidget(header)
            
            # Contenido principal con scroll (exacto del HTML)
            scroll = QScrollArea(instructor_win)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet(f"background-color: {BG_LIGHT_HTML}; border: none;")
            scroll.setFrameShape(QFrame.NoFrame)
            
            main_content = QWidget()
            main_content.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            main_layout = QVBoxLayout(main_content)
            main_layout.setContentsMargins(40, 20, 40, 20)  # px-4 sm:px-8 md:px-16 lg:px-40 py-5
            main_layout.setSpacing(32)  # mb-8 = 32px (gap entre secciones)
            
            # Sección de bienvenida (exacto del HTML)
            welcome_container = QWidget(main_content)
            welcome_container.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border-radius: 12px; "
                f"padding: 24px;"
            )
            welcome_layout = QHBoxLayout(welcome_container)
            welcome_layout.setContentsMargins(0, 0, 0, 0)
            welcome_layout.setSpacing(16)
            
            # Icono de imagen (sin círculo de fondo)
            icon_label = QLabel(welcome_container)
            icon_label.setAlignment(Qt.AlignCenter)
            
            # Cargar imagen de saludo
            image_path = "images/saludo.jpg"
            if not os.path.isabs(image_path):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                full_image_path = os.path.join(script_dir, image_path)
            else:
                full_image_path = image_path
            
            if os.path.exists(full_image_path):
                pixmap = QPixmap(full_image_path)
                # Escalar la imagen a un tamaño adecuado (80x80 para que se vea bien)
                scaled_pixmap = pixmap.scaled(
                    80, 80,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setStyleSheet(
                    "background-color: transparent; "
                    "border: none; "
                    "padding: 0px; "
                    "margin: 0px;"
                )
                icon_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            else:
                # Fallback si la imagen no existe
                icon_label.setText("👋")
                icon_label.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; "
                    f"font-size: 36px; "
                    f"background-color: transparent; "
                    f"border: none; "
                    f"padding: 0px; "
                    f"margin: 0px;"
                )
            
            welcome_layout.addWidget(icon_label)
            
            # Título de bienvenida - SIN ENCAPSULACIÓN
            welcome_title = QLabel("¡BIENVENIDO INSTRUCTOR!", welcome_container)
            welcome_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            welcome_title.setWordWrap(False)
            welcome_title.setTextFormat(Qt.PlainText)
            welcome_title.setOpenExternalLinks(False)
            welcome_title.setMinimumWidth(0)
            welcome_title.setMaximumWidth(16777215)
            welcome_title.setMinimumHeight(0)
            welcome_font = welcome_title.font()
            welcome_font.setPointSize(30)
            welcome_font.setBold(True)
            welcome_title.setFont(welcome_font)
            welcome_fm = QFontMetrics(welcome_font)
            welcome_text_width = welcome_fm.horizontalAdvance("¡BIENVENIDO INSTRUCTOR!")
            welcome_title.setMinimumWidth(welcome_text_width)
            welcome_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 30px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            welcome_layout.addWidget(welcome_title)
            welcome_layout.addStretch(1)
            
            main_layout.addWidget(welcome_container)
            
            # Sección AMBIENTE ASIGNADO
            self._show_assigned_environment_stitch_new(main_content, main_layout)
            
            scroll.setWidget(main_content)
            root_layout.addWidget(scroll, 1)
            
            # Ya está en pantalla completa real, no es necesario centrar ni mostrar
            print("✅ Interfaz de instructor mostrada correctamente en pantalla completa real")
        except Exception as e:
            print(f"❌ Error mostrando interfaz de instructor: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error mostrando interfaz de instructor:\n{e}")

    def _create_futuristic_header(self, parent, layout):
        header = styles.create_main_frame(parent)
        header_layout = QVBoxLayout(header)
        icon = styles.create_title_label(header, "👨‍🏫")
        # Obtener nombre desde KeyManager si está autenticado
        welcome_name = "INSTRUCTOR"
        try:
            if self._km.current_user:
                welcome_name = f"{self._km.current_user.get('nombres','').strip()} {self._km.current_user.get('apellidos','').strip()}".strip() or "INSTRUCTOR"
        except Exception:
            pass
        title = styles.create_title_label(header, f"¡BIENVENIDO {welcome_name}!")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        layout.addWidget(header)

    def _show_assigned_environment_stitch_new(self, parent, layout):
        """Muestra la sección AMBIENTE ASIGNADO con diseño exacto del HTML de Stitch AI"""
        PRIMARY_COLOR = "#136dec"
        CARD_BG = "#ffffff"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        
        # Contenedor de tarjeta blanca (exacto del HTML) - Más padding horizontal
        env_container = QWidget(parent)
        env_container.setStyleSheet(
            f"background-color: {CARD_BG}; "
            f"border-radius: 12px;"
        )
        env_layout = QVBoxLayout(env_container)
        env_layout.setContentsMargins(60, 24, 60, 24)  # left, top, right, bottom - Más espacio horizontal (60px)
        env_layout.setSpacing(16)
        
        # Título con borde inferior - SIN ENCAPSULACIÓN
        title_label = QLabel("AMBIENTE ASIGNADO", env_container)
        title_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        title_label.setWordWrap(False)
        title_label.setTextFormat(Qt.PlainText)
        title_label.setOpenExternalLinks(False)
        title_label.setMinimumWidth(0)
        title_label.setMaximumWidth(16777215)
        title_label.setMinimumHeight(0)
        title_font = title_label.font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_fm = QFontMetrics(title_font)
        title_text_width = title_fm.horizontalAdvance("AMBIENTE ASIGNADO")
        title_label.setMinimumWidth(title_text_width)
        title_label.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 20px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
            f"border-bottom: 1px solid {BORDER_COLOR}; "
            f"padding-bottom: 16px; "
            f"margin-bottom: 16px; "
            f"background-color: transparent; "
            f"border-left: none; "
            f"border-right: none; "
            f"border-top: none; "
            f"padding-left: 0px; "
            f"padding-right: 0px; "
            f"padding-top: 0px; "
            f"margin-left: 0px; "
            f"margin-right: 0px; "
            f"margin-top: 0px;"
        )
        env_layout.addWidget(title_label)
        
        # Lista de elementos del ambiente (exacto del HTML) - Usar imágenes si existen
        details = [
            ("images/aula.jpg", "🚪", "Aula", "505", "#10b981"),  # green-500 (door_open)
            ("images/equipos.jpg", "💻", "Equipos", "25 Computadores", "#3b82f6"),  # blue-500 (desktop_windows)
            ("images/capacidad.jpg", "👥", "Capacidad", "30 Estudiantes", "#8b5cf6"),  # purple-500 (groups)
            ("images/conectividad.jpg", "📶", "Conectividad", "Disponible", "#14b8a6"),  # teal-500 (wifi)
            ("images/recursos.jpg", "📹", "Recursos", "Video Beam", "#f97316"),  # orange-500 (video_camera_front)
        ]
        
        for icon_path, icon_emoji, label, value, icon_color in details:
            row = QWidget(env_container)
            row.setMinimumHeight(56)  # min-h-14 = 56px
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)  # Los márgenes se manejan en el contenedor padre
            row_layout.setSpacing(16)
            
            # Icono - Usar imagen si existe, sino emoji con contenedor circular
            is_image = False
            icon_label = QLabel(row)
            icon_label.setAlignment(Qt.AlignCenter)
            
            # Verificar si es una ruta de imagen y si existe
            if isinstance(icon_path, str) and icon_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
                # Obtener la ruta absoluta
                if not os.path.isabs(icon_path):
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    full_image_path = os.path.join(script_dir, icon_path)
                else:
                    full_image_path = icon_path
                
                if os.path.exists(full_image_path):
                    is_image = True
                    # Cargar y escalar la imagen (más grande para que se vea mejor)
                    pixmap = QPixmap(full_image_path)
                    # Escalar a 48x48 (más grande que antes)
                    scaled_pixmap = pixmap.scaled(
                        48, 48,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    icon_label.setPixmap(scaled_pixmap)
                    icon_label.setStyleSheet(
                        "background-color: transparent; "
                        "border: none; "
                        "padding: 0px; "
                        "margin: 0px;"
                    )
                    icon_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            
            # Si no es imagen o no existe, usar emoji con contenedor circular
            if not is_image:
                icon_container = QWidget(row)
                icon_container.setFixedSize(40, 40)
                icon_container.setStyleSheet(
                    f"background-color: {BORDER_COLOR}; "
                    f"border-radius: 8px;"
                )
                icon_layout = QVBoxLayout(icon_container)
                icon_layout.setContentsMargins(0, 0, 0, 0)
                icon_layout.setAlignment(Qt.AlignCenter)
                
                emoji_label = QLabel(icon_emoji, icon_container)
                emoji_label.setAlignment(Qt.AlignCenter)
                emoji_label.setStyleSheet(
                    f"color: {icon_color}; "
                    f"font-size: 20px; "
                    f"background-color: transparent; "
                    f"border: none; "
                    f"padding: 0px; "
                    f"margin: 0px;"
                )
                icon_layout.addWidget(emoji_label)
                row_layout.addWidget(icon_container)
            else:
                # Si es imagen, agregarla directamente sin contenedor
                row_layout.addWidget(icon_label)
            
            # Label del ambiente - SIN ENCAPSULACIÓN, alineado a la izquierda
            label_widget = QLabel(label, row)
            label_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            label_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label_widget.setWordWrap(False)
            label_widget.setTextFormat(Qt.PlainText)
            label_widget.setOpenExternalLinks(False)
            label_widget.setMinimumWidth(0)
            label_widget.setMaximumWidth(16777215)
            label_widget.setMinimumHeight(0)
            font = label_widget.font()
            font.setPointSize(16)
            label_widget.setFont(font)
            fm = QFontMetrics(font)
            text_width = fm.horizontalAdvance(label)
            label_widget.setMinimumWidth(text_width)
            label_widget.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 16px; "
                f"font-weight: 400; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            row_layout.addWidget(label_widget)
            row_layout.addStretch(1)  # Espacio flexible para empujar el valor a la derecha
            
            # Valor en azul primario - SIN ENCAPSULACIÓN, alineado a la derecha
            value_widget = QLabel(value, row)
            value_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            value_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            value_widget.setWordWrap(False)
            value_widget.setTextFormat(Qt.PlainText)
            value_widget.setOpenExternalLinks(False)
            value_widget.setMinimumWidth(0)
            value_widget.setMaximumWidth(16777215)
            value_widget.setMinimumHeight(0)
            value_font = value_widget.font()
            value_font.setPointSize(16)
            value_font.setBold(True)
            value_widget.setFont(value_font)
            value_fm = QFontMetrics(value_font)
            value_text_width = value_fm.horizontalAdvance(value)
            value_widget.setMinimumWidth(value_text_width)
            value_widget.setStyleSheet(
                f"color: {PRIMARY_COLOR}; "
                f"font-size: 16px; "
                f"font-weight: 700; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            row_layout.addWidget(value_widget, 0, Qt.AlignRight)  # Alinear a la derecha
            
            env_layout.addWidget(row)
        
        layout.addWidget(env_container)

    def _show_assigned_environment_stitch(self, parent, layout):
        """Muestra la sección AMBIENTE ASIGNADO con diseño Stitch AI"""
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        ICON_PINK = "#ec4899"  # pink-500
        ICON_PURPLE = "#a78bfa"  # purple-400
        ICON_DARK_PURPLE = "#8b5cf6"  # purple-500
        ICON_BLUE = "#60a5fa"  # blue-400
        ICON_GREEN = "#10b981"  # green-500
        
        # Título de la sección
        title_label = QLabel("AMBIENTE ASIGNADO", parent)
        title_label.setStyleSheet(
            f"color: {ICON_BLUE}; "
            f"font-size: 18px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        title_label.setWordWrap(False)
        layout.addWidget(title_label)
        
        # Detalles del ambiente con iconos de colores
        details = [
            ("📍", "AULA PRINCIPAL:", "Aula 101 - Laboratorio de Programación", ICON_PINK),
            ("🔧", "EQUIPOS:", "25 computadoras, Proyector 4K, Pizarra digital", ICON_PURPLE),
            ("👥", "CAPACIDAD:", "30 estudiantes", ICON_DARK_PURPLE),
            ("🌐", "CONECTIVIDAD:", "WiFi de alta velocidad, Red cableada", ICON_BLUE),
            ("📚", "RECURSOS:", "Software de desarrollo, Bibliotecas digitales", ICON_GREEN),
        ]
        
        for icon_emoji, label, value, icon_color in details:
            row = QWidget(parent)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 8, 0, 8)
            row_layout.setSpacing(12)
            
            # Icono con color
            icon_label = QLabel(icon_emoji, row)
            icon_label.setStyleSheet(
                f"color: {icon_color}; "
                f"font-size: 20px;"
            )
            row_layout.addWidget(icon_label)
            
            # Label en azul claro
            label_widget = QLabel(label, row)
            label_widget.setStyleSheet(
                f"color: {ICON_BLUE}; "
                f"font-size: 14px; "
                f"font-weight: 700;"
            )
            label_widget.setWordWrap(False)
            row_layout.addWidget(label_widget)
            
            # Valor en azul claro
            value_widget = QLabel(value, row)
            value_widget.setStyleSheet(
                f"color: {ICON_BLUE}; "
                f"font-size: 14px; "
                f"font-weight: 400;"
            )
            value_widget.setWordWrap(False)
            row_layout.addWidget(value_widget)
            row_layout.addStretch(1)
            
            layout.addWidget(row)

    def _show_instructor_calendar_stitch_new(self, parent, layout):
        """Muestra la sección HORARIO DE CLASES con diseño exacto del HTML de Stitch AI"""
        HEADER_DARK = "#2D3748"
        TEXT_WHITE = "#ffffff"
        TEXT_LIGHT_GRAY = "#d1d5db"
        BORDER_GRAY = "#4b5563"  # gray-600
        
        # Contenedor con fondo oscuro (exacto del HTML)
        schedule_container = QWidget(parent)
        schedule_container.setStyleSheet(
            f"background-color: {HEADER_DARK}; "
            f"border-radius: 12px; "
            f"padding: 32px;"  # Aumentado de 24px a 32px para más espacio
        )
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setContentsMargins(0, 0, 0, 0)
        schedule_layout.setSpacing(24)
        
        # Header con título y borde inferior - SIN ENCAPSULACIÓN
        title_label = QLabel("HORARIO DE CLASES", schedule_container)
        title_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        title_label.setWordWrap(False)
        title_label.setTextFormat(Qt.PlainText)
        title_label.setOpenExternalLinks(False)
        title_label.setMinimumWidth(0)
        title_label.setMaximumWidth(16777215)
        title_label.setMinimumHeight(0)
        title_font = title_label.font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_fm = QFontMetrics(title_font)
        title_text_width = title_fm.horizontalAdvance("HORARIO DE CLASES")
        title_label.setMinimumWidth(title_text_width)
        title_label.setStyleSheet(
            f"color: {TEXT_WHITE}; "
            f"font-size: 20px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
            f"border-bottom: 1px solid {BORDER_GRAY}; "
            f"padding-bottom: 16px; "
            f"margin-bottom: 24px; "
            f"background-color: transparent; "
            f"border-left: none; "
            f"border-right: none; "
            f"border-top: none; "
            f"padding-left: 0px; "
            f"padding-right: 0px; "
            f"padding-top: 0px; "
            f"margin-left: 0px; "
            f"margin-right: 0px; "
            f"margin-top: 0px;"
        )
        schedule_layout.addWidget(title_label)
        
        # Cargar programación real por instructor
        personal_id = None
        try:
            if self._km.current_user:
                personal_id = self._km.current_user.get('id')
        except Exception:
            pass
        
        schedule = []
        day_order = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
        if personal_id:
            week = get_instructor_week_schedule(personal_id)
            for d in day_order:
                items = week.get(d, [])
                if items:
                    pretty = d.capitalize() if d != "MIERCOLES" else "Miércoles"
                    mapped = []
                    for it in items:
                        t = f"{it['inicio']} - {it['fin']}" if it.get('inicio') and it.get('fin') else (it.get('inicio') or '')
                        mapped.append((t, it.get('tipo') or 'Clase', it.get('ambiente') or '', it.get('ambiente_id')))
                    schedule.append((pretty, mapped))
        
        # Si no hay datos, mostrar mensaje informativo (exacto del HTML)
        if not schedule:
            no_data_container = QWidget(schedule_container)
            no_data_layout = QVBoxLayout(no_data_container)
            no_data_layout.setContentsMargins(40, 32, 40, 32)  # Más espacio horizontal (40px) y vertical (32px)
            no_data_layout.setSpacing(16)
            no_data_layout.setAlignment(Qt.AlignCenter)
            
            # Icono de imagen (sin círculo de fondo)
            icon_label = QLabel(no_data_container)
            icon_label.setAlignment(Qt.AlignCenter)
            
            # Cargar imagen de horario
            image_path = "images/horario.jpg"
            if not os.path.isabs(image_path):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                full_image_path = os.path.join(script_dir, image_path)
            else:
                full_image_path = image_path
            
            if os.path.exists(full_image_path):
                pixmap = QPixmap(full_image_path)
                # Escalar la imagen a un tamaño adecuado (64x64 para que se vea bien)
                scaled_pixmap = pixmap.scaled(
                    64, 64,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setStyleSheet(
                    "background-color: transparent; "
                    "border: none; "
                    "padding: 0px; "
                    "margin: 0px;"
                )
                icon_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            else:
                # Fallback si la imagen no existe
                icon_label.setText("📅")
                icon_label.setStyleSheet(
                    f"color: {TEXT_LIGHT_GRAY}; "
                    f"font-size: 36px; "
                    f"background-color: transparent; "
                    f"border: none; "
                    f"padding: 0px; "
                    f"margin: 0px;"
                )
            
            no_data_layout.addWidget(icon_label, 0, Qt.AlignCenter)
            
            # Mensaje principal - SIN ENCAPSULACIÓN
            no_data_msg = QLabel("No hay programación disponible", no_data_container)
            no_data_msg.setAlignment(Qt.AlignCenter)
            no_data_msg.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            no_data_msg.setWordWrap(False)
            no_data_msg.setTextFormat(Qt.PlainText)
            no_data_msg.setOpenExternalLinks(False)
            no_data_msg.setMinimumWidth(0)
            no_data_msg.setMaximumWidth(16777215)
            no_data_msg.setMinimumHeight(0)
            no_data_font = no_data_msg.font()
            no_data_font.setPointSize(18)
            no_data_font.setWeight(QFont.Weight.Medium)  # Medium weight (500)
            no_data_msg.setFont(no_data_font)
            no_data_fm = QFontMetrics(no_data_font)
            no_data_text_width = no_data_fm.horizontalAdvance("No hay programación disponible")
            no_data_msg.setMinimumWidth(no_data_text_width)
            no_data_msg.setStyleSheet(
                f"color: {TEXT_LIGHT_GRAY}; "
                f"font-size: 18px; "
                f"font-weight: 500; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            no_data_layout.addWidget(no_data_msg)
            
            schedule_layout.addWidget(no_data_container)
            layout.addWidget(schedule_container)
            return
        
        # Si hay programación, guardar datos
        self._schedule_data = schedule
        
        # Aquí puedes agregar lógica para mostrar las clases programadas
        layout.addWidget(schedule_container)

    def _show_instructor_calendar_stitch(self, parent, layout):
        """Muestra la sección HORARIO DE CLASES con diseño Stitch AI"""
        SCHEDULE_DARK = "#1f2937"  # dark-800 similar al header
        TEXT_WHITE = "#ffffff"
        TEXT_LIGHT_GRAY = "#d1d5db"  # gray-300
        
        # Contenedor con fondo oscuro
        schedule_container = QWidget(parent)
        schedule_container.setStyleSheet(
            f"background-color: {SCHEDULE_DARK}; "
            f"border-radius: 12px; "
            f"padding: 24px;"
        )
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setContentsMargins(0, 0, 0, 0)
        schedule_layout.setSpacing(16)
        
        # Header con icono y título
        header_row = QWidget(schedule_container)
        header_layout = QHBoxLayout(header_row)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        # Icono de calendario
        calendar_icon = QLabel("📅", header_row)
        calendar_icon.setStyleSheet(
            f"color: {TEXT_WHITE}; "
            f"font-size: 20px;"
        )
        header_layout.addWidget(calendar_icon)
        
        # Título en blanco
        title_label = QLabel("HORARIO DE CLASES", header_row)
        title_label.setStyleSheet(
            f"color: {TEXT_WHITE}; "
            f"font-size: 18px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        title_label.setWordWrap(False)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        
        schedule_layout.addWidget(header_row)
        
        # Cargar programación real por instructor
        personal_id = None
        try:
            if self._km.current_user:
                personal_id = self._km.current_user.get('id')
        except Exception:
            pass
        
        schedule = []
        day_order = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
        if personal_id:
            week = get_instructor_week_schedule(personal_id)
            for d in day_order:
                items = week.get(d, [])
                if items:
                    pretty = d.capitalize() if d != "MIERCOLES" else "Miércoles"
                    mapped = []
                    for it in items:
                        t = f"{it['inicio']} - {it['fin']}" if it.get('inicio') and it.get('fin') else (it.get('inicio') or '')
                        mapped.append((t, it.get('tipo') or 'Clase', it.get('ambiente') or '', it.get('ambiente_id')))
                    schedule.append((pretty, mapped))
        
        # Si no hay datos, mostrar mensaje informativo
        if not schedule:
            no_data_container = QWidget(schedule_container)
            no_data_layout = QVBoxLayout(no_data_container)
            no_data_layout.setContentsMargins(0, 0, 0, 0)
            no_data_layout.setSpacing(8)
            
            # Icono de usuario
            user_icon = QLabel("👤", no_data_container)
            user_icon.setStyleSheet(
                f"color: {TEXT_LIGHT_GRAY}; "
                f"font-size: 24px;"
            )
            no_data_layout.addWidget(user_icon)
            
            # Mensaje principal
            no_data_msg = QLabel("No hay programación disponible", no_data_container)
            no_data_msg.setStyleSheet(
                f"color: {TEXT_LIGHT_GRAY}; "
                f"font-size: 14px; "
                f"font-weight: 400;"
            )
            no_data_msg.setWordWrap(False)
            no_data_layout.addWidget(no_data_msg)
            
            # Mensaje secundario
            contact_msg = QLabel("Contacte al administrador para configurar su horario", no_data_container)
            contact_msg.setStyleSheet(
                f"color: {TEXT_LIGHT_GRAY}; "
                f"font-size: 14px; "
                f"font-weight: 400;"
            )
            contact_msg.setWordWrap(False)
            no_data_layout.addWidget(contact_msg)
            
            schedule_layout.addWidget(no_data_container)
            layout.addWidget(schedule_container)
            return
        
        # Si hay programación, mostrar los días con clases
        self._schedule_data = schedule
        
        # Aquí puedes agregar lógica para mostrar las clases programadas
        # Por ahora, simplemente agregamos el contenedor
        layout.addWidget(schedule_container)

    def _show_instructor_calendar(self, parent, layout):
        # Encabezado mejorado
        card = styles.create_card(parent)
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(20, 16, 20, 16)
        card_l.setSpacing(12)
        
        # Título con icono
        title_frame = QHBoxLayout()
        title_frame.addWidget(QLabel("📅"))
        title_frame.addWidget(styles.create_subtitle_label(card, "HORARIO DE CLASES"))
        title_frame.addStretch(1)
        card_l.addLayout(title_frame)

        # Cargar programación real por instructor
        personal_id = None
        try:
            if self._km.current_user:
                personal_id = self._km.current_user.get('id')
        except Exception:
            pass
        
        schedule = []
        day_order = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
        if personal_id:
            week = get_instructor_week_schedule(personal_id)
            for d in day_order:
                items = week.get(d, [])
                if items:
                    pretty = d.capitalize() if d != "MIERCOLES" else "Miércoles"
                    mapped = []
                    for it in items:
                        t = f"{it['inicio']} - {it['fin']}" if it.get('inicio') and it.get('fin') else (it.get('inicio') or '')
                        mapped.append((t, it.get('tipo') or 'Clase', it.get('ambiente') or '', it.get('ambiente_id')))
                    schedule.append((pretty, mapped))
        
        # Si no hay datos reales, mostrar mensaje informativo
        if not schedule:
            no_data_frame = styles.create_main_frame(card)
            no_data_l = QVBoxLayout(no_data_frame)
            no_data_l.setContentsMargins(20, 20, 20, 20)
            no_data_l.addWidget(QLabel("📭"))
            no_data_l.addWidget(styles.create_info_label(no_data_frame, "No hay programación disponible"))
            no_data_l.addWidget(styles.create_info_label(no_data_frame, "Contacte al administrador para configurar su horario"))
            card_l.addWidget(no_data_frame)
            layout.addWidget(card)
            return
            
        self._schedule_data = schedule

        # Selector de días mejorado - solo mostrar días con programación
        days_bar = QWidget(card)
        hb = QHBoxLayout(days_bar)
        hb.setContentsMargins(0, 0, 0, 0)
        hb.setSpacing(12)
        card_l.addWidget(days_bar)

        # Crear botones de días solo para días con programación
        self._day_buttons = {}
        for i, (day, _) in enumerate(schedule):
            btn = QPushButton(f"📅 {day}", days_bar)
            btn.setProperty("class", "warning")
            btn.setObjectName("warning")
            btn.setCursor(Qt.PointingHandCursor)
            # Usar una función auxiliar para evitar problemas con lambda
            def make_click_handler(day_name):
                def handler():
                    self._populate_day(day_name)
                return handler
            btn.clicked.connect(make_click_handler(day))
            hb.addWidget(btn)
            self._day_buttons[day] = btn
        hb.addStretch(1)

        # Contenedor principal para las clases
        self._day_container = QWidget(card)
        self._day_layout = QVBoxLayout(self._day_container)
        self._day_layout.setContentsMargins(0, 8, 0, 0)
        self._day_layout.setSpacing(8)
        card_l.addWidget(self._day_container)

        # Mostrar el primer día por defecto
        if schedule:
            self._populate_day(schedule[0][0])
        layout.addWidget(card)

    def _populate_day(self, day: str):
        # Limpiar contenido anterior
        while self._day_layout.count():
            item = self._day_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
        
        # Marcar botón activo visualmente
        for name, btn in self._day_buttons.items():
            try:
                if name == day:
                    btn.setStyleSheet(btn.styleSheet() + "font-weight: 800; background-color: #00d4ff; color: #0a0e1a;")
                else:
                    btn.setStyleSheet(btn.styleSheet().replace("font-weight: 800; background-color: #00d4ff; color: #0a0e1a;", ""))
            except Exception:
                pass
        
        # Cargar items del día
        items = []
        found = False
        
        for d, lst in (self._schedule_data or []):
            if d == day:
                items = lst
                found = True
                break
                
        if not found:
            # Si no hay registros para ese día, mostrar un mensaje elegante
            empty = styles.create_card(self._day_container)
            e_l = QVBoxLayout(empty)
            e_l.setContentsMargins(20, 20, 20, 20)
            e_l.addWidget(QLabel("📭"))
            e_l.addWidget(styles.create_info_label(empty, f"No hay clases programadas para {day}"))
            self._day_layout.addWidget(empty)
            return
            
        # Verificar estado actual de llaves
        current_taken = False
        try:
            if self._km and self._km.current_user:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
                current_taken = len(assignments) > 0
        except Exception:
            pass
        self._status_by_day[day] = current_taken

        # Verificar si es el día actual
        import datetime
        now = datetime.datetime.now()
        weekday_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        today_name = weekday_map.get(now.weekday())
        today_is_selected = (day == today_name)

        # Mostrar información del día actual
        if today_is_selected:
            info_frame = styles.create_main_frame(self._day_container)
            info_l = QHBoxLayout(info_frame)
            info_l.setContentsMargins(12, 8, 12, 8)
            info_l.addWidget(QLabel("📅"))
            info_l.addWidget(styles.create_info_label(info_frame, f"Hoy es {day} - Puede gestionar llaves"))
            info_l.addStretch(1)
            self._day_layout.addWidget(info_frame)

        # Mostrar cada clase del día
        for t, title, room, ambiente_id in items:
            # Crear tarjeta para cada clase
            class_card = styles.create_card(self._day_container)
            class_l = QVBoxLayout(class_card)
            class_l.setContentsMargins(16, 12, 16, 12)
            class_l.setSpacing(8)
            
            # Información de la clase
            time_label = styles.create_subtitle_label(class_card, f"🕐 {t}")
            class_l.addWidget(time_label)
            
            class_info = QHBoxLayout()
            class_info.addWidget(QLabel("📚"))
            class_info.addWidget(styles.create_info_label(class_card, f"{title}"))
            class_info.addStretch(1)
            class_l.addLayout(class_info)
            
            room_info = QHBoxLayout()
            room_info.addWidget(QLabel("🏫"))
            room_info.addWidget(styles.create_info_label(class_card, f"{room}"))
            room_info.addStretch(1)
            class_l.addLayout(room_info)
            
            # Acciones de llave
            actions = QHBoxLayout()
            actions.setContentsMargins(0, 8, 0, 0)
            actions.setSpacing(12)
            
            # Estado actual
            if current_taken:
                status_chip = styles.create_status_chip(class_card, "🔑 Llave Tomada", "success")
            else:
                status_chip = styles.create_status_chip(class_card, "⏳ Pendiente", "warning")
            actions.addWidget(status_chip)
            
            # Botones de acción - usar funciones auxiliares para evitar problemas con lambda
            def make_take_handler(day_name, time_range, class_title, room_name, env_id):
                def handler():
                    self._take_key_flow(day_name, time_range, class_title, room_name, env_id)
                return handler
            
            def make_return_handler(day_name, time_range, class_title, room_name, env_id):
                def handler():
                    self._return_key_flow(day_name, time_range, class_title, room_name, env_id)
                return handler
            
            take_btn = QPushButton("🔑 Tomar Llave", class_card)
            take_btn.setProperty("class", "accent")
            take_btn.setObjectName("accent")
            take_btn.setCursor(Qt.PointingHandCursor)
            take_btn.clicked.connect(make_take_handler(day, t, title, room, ambiente_id))
            
            return_btn = QPushButton("↩️ Devolver", class_card)
            return_btn.setProperty("class", "danger")
            return_btn.setObjectName("danger")
            return_btn.setCursor(Qt.PointingHandCursor)
            return_btn.clicked.connect(make_return_handler(day, t, title, room, ambiente_id))
            
            # Validar si puede operar (solo en el día actual)
            can_operate = today_is_selected
            # Por ahora, permitir operar en el día actual sin validación estricta de horario
            # Esto permite mayor flexibilidad al instructor

            # Configurar botones según el estado
            take_btn.setEnabled(not current_taken and can_operate)
            return_btn.setEnabled(current_taken and can_operate)
            
            # Agregar tooltips informativos
            if not today_is_selected:
                take_btn.setToolTip("Solo puede gestionar llaves en el día actual")
                return_btn.setToolTip("Solo puede gestionar llaves en el día actual")
            else:
                take_btn.setToolTip("Hacer clic para tomar la llave del ambiente")
                return_btn.setToolTip("Hacer clic para devolver la llave del ambiente")
            
            actions.addWidget(take_btn)
            actions.addWidget(return_btn)
            actions.addStretch(1)
            
            class_l.addLayout(actions)
            self._day_layout.addWidget(class_card)

    def _create_futuristic_footer(self, parent, window, layout):
        # Footer con botón de cerrar sesión eliminado por solicitud; se usa la X de la ventana
        return

    def _get_keys_for_environment(self, environment_id: int, room_name: str) -> List[Dict[str, Any]]:
        """Busca llaves para un ambiente de manera más flexible"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                
                # Primero buscar llaves disponibles
                query_available = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, activo, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE activo = 1 AND estado = 'DISPONIBLE' AND ambiente_id = %s
                    ORDER BY codigo_llave
                """
                cur.execute(query_available, (environment_id,))
                available_keys = cur.fetchall()
                
                if available_keys:
                    cur.close()
                    return available_keys
                
                # Si no hay disponibles, buscar cualquier llave del ambiente que no esté perdida
                query_any = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, activo, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE activo = 1 AND ambiente_id = %s AND estado != 'PERDIDA'
                    ORDER BY codigo_llave
                """
                cur.execute(query_any, (environment_id,))
                any_keys = cur.fetchall()
                
                cur.close()
                return any_keys
                
        except Exception as e:
            print(f"❌ Error buscando llaves para ambiente {environment_id}: {e}")
            return []

    def _assign_key_directly(self, user_id: int, key_id: int, observations: str = "") -> bool:
        """Asigna una llave directamente sin validaciones estrictas de estado"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor()
                
                # Verificar que la llave existe y está activa
                cur.execute("SELECT id, estado FROM llaves WHERE id = %s AND activo = 1", (key_id,))
                key_info = cur.fetchone()
                if not key_info:
                    print(f"❌ La llave {key_id} no existe o no está activa")
                    return False
                
                # Crear la asignación sin verificar el estado de la llave
                insert_query = """
                    INSERT INTO asignaciones_llaves 
                    (personal_id, llave_id, fecha_asignacion, estado, motivo, created_at)
                    VALUES (%s, %s, NOW(), 'ACTIVA', %s, NOW())
                """
                cur.execute(insert_query, (user_id, key_id, observations))
                
                # Actualizar estado de la llave a ASIGNADA
                cur.execute("UPDATE llaves SET estado = 'ASIGNADA' WHERE id = %s", (key_id,))
                
                cnx.commit()
                cur.close()
                
                print(f"✅ Llave {key_id} asignada exitosamente a usuario {user_id}")
                
                # Registrar en logs
                from src.utils.db_utils import log_access
                log_access(user_id, 'ENTREGA_LLAVE', f"Llave {key_id} asignada - {observations}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error en asignación directa: {e}")
            return False

    def _show_progress(self, text: str) -> QDialog:
        dlg = styles.create_modal_window(self.parent, "Procesando...", "420x160")
        try:
            dlg.setObjectName("progressDialog")
        except Exception:
            pass
        lay = QVBoxLayout(dlg)
        lay.addWidget(styles.create_subtitle_label(dlg, text))
        dlg.show()
        QApplication.processEvents()
        return dlg

    def _take_key_flow(self, day: str, time_range: str, title: str, room: str, ambiente_id: int = None):
        # Si ya hay usuario autenticado, no pedir huella
        if self._km and self._km.current_user:
            try:
                # Usar el ambiente_id de la programación si está disponible
                env_id = ambiente_id
                if not env_id:
                    from src.utils.utils import query_latest_environment
                    env_info = query_latest_environment(self._km.current_user['id'])
                    env_id = env_info[0] if env_info else None
                
                # Buscar llaves de manera más flexible
                keys = self._get_keys_for_environment(env_id, room)
                if not keys:
                    QMessageBox.information(self.parent, "Sin llaves", f"No hay llaves disponibles para el ambiente {room}")
                    return
                
                key_id = keys[0]['id']
                # Usar la función directa de db_utils en lugar de KeyManager para evitar validaciones estrictas
                ok = self._assign_key_directly(self._km.current_user['id'], key_id, f"{day} {time_range} - {title} ({room})")
                if ok:
                    # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                    self._send_arduino_command(key_id, "TOMAR")
                    
                    try:
                        from src.core.desktop_alerts import desktop_alert_system
                        desktop_alert_system.show_key_assigned_alert(keys[0]['codigo_llave'], f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    except Exception:
                        QMessageBox.information(self.parent, "✅ Llave entregada", f"Se asignó la llave {keys[0]['codigo_llave']} a {self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    # Actualizar estado visual: tomada
                    self._status_by_day[day] = True
                    self._populate_day(day)
                else:
                    QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")
                return
            except Exception as e:
                QMessageBox.warning(self.parent, "⚠️", f"No fue posible completar la operación: {e}")
                return

        progress = self._show_progress("👆 Iniciando escaneo para tomar llave...")
        try:
            validator = FingerprintValidator()
            if not validator.connect():
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo conectar al lector biométrico")
                return
            scanned = validator.scan_fingerprint()
            if not scanned:
                QMessageBox.warning(self.parent, "⚠️ Escaneo", "No se obtuvo huella válida")
                return
            user = validator.validate_fingerprint_against_database(scanned)
            validator.disconnect()
            if not user:
                QMessageBox.critical(self.parent, "Acceso denegado", "Huella no coincide con ningún usuario")
                return
            # Autenticar en KeyManager y obtener ambiente
            self._km.authenticate_user(user['id'])
            env_id = ambiente_id
            if not env_id:
                from src.utils.utils import query_latest_environment
                env_info = query_latest_environment(user['id'])
                env_id = env_info[0] if env_info else None
            
            # Buscar llaves de manera más flexible
            keys = self._get_keys_for_environment(env_id, room)
            if not keys:
                QMessageBox.information(self.parent, "Sin llaves", f"No hay llaves disponibles para el ambiente {room}")
                return
            key_id = keys[0]['id']
            # Usar la función directa de db_utils en lugar de KeyManager para evitar validaciones estrictas
            ok = self._assign_key_directly(user['id'], key_id, f"{day} {time_range} - {title} ({room})")
            if ok:
                # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                self._send_arduino_command(key_id, "TOMAR")
                
                QMessageBox.information(self.parent, "✅ Llave entregada", f"Se asignó la llave {keys[0]['codigo_llave']} a {user['nombres']} {user['apellidos']}")
            else:
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")
        finally:
            progress.close()

    def _return_key_directly(self, assignment_id: int, observations: str = "") -> bool:
        """Marca una asignación como devuelta y libera la llave directamente."""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor()
                cur.execute("SELECT llave_id, personal_id FROM asignaciones_llaves WHERE id = %s AND estado = 'ACTIVA'", (assignment_id,))
                row = cur.fetchone()
                if not row:
                    print(f"❌ Asignación {assignment_id} no encontrada o no activa")
                    return False
                key_id = row[0]
                personal_id = row[1] if len(row) > 1 else None
                cur.execute("""
                    UPDATE asignaciones_llaves 
                    SET estado = 'DEVUELTA', fecha_devolucion = NOW(), 
                        notas = CONCAT(IFNULL(notas, ''), ' | Devolución: ', %s),
                        updated_at = NOW()
                    WHERE id = %s
                """, (observations, assignment_id))
                cur.execute("UPDATE llaves SET estado = 'DISPONIBLE' WHERE id = %s", (key_id,))
                cnx.commit()
                cur.close()
                try:
                    from src.utils.db_utils import log_access
                    if personal_id:
                        log_access(personal_id, 'DEVOLUCION_LLAVE', f"Llave {key_id} devuelta - {observations}")
                except Exception:
                    pass
                print(f"✅ Llave {key_id} devuelta (asignación {assignment_id})")
                return True
        except Exception as e:
            print(f"❌ Error en devolución directa: {e}")
            return False
    def _return_key_flow(self, day: str, time_range: str, title: str, room: str, ambiente_id: int = None):
        # Si ya hay usuario autenticado, no pedir huella
        if self._km and self._km.current_user:
            try:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
                if not assignments:
                    QMessageBox.information(self.parent, "Sin asignaciones", "No hay llaves activas para devolver")
                    return
                
                # Buscar la asignación correcta por ambiente si está disponible
                assignment_id = assignments[-1]['id']  # Por defecto la última
                if ambiente_id:
                    for assignment in assignments:
                        # Verificar si la llave pertenece al ambiente correcto
                        try:
                            from src.utils.utils import get_key_environment
                            key_env = get_key_environment(assignment.get('llave_id'))
                            if key_env and key_env.get('id') == ambiente_id:
                                assignment_id = assignment['id']
                                break
                        except Exception:
                            pass
                
                # obtener código de llave para mostrar en alertas
                key_code = None
                try:
                    assignment_obj = next(a for a in assignments if a['id'] == assignment_id)
                    key_code = assignment_obj.get('llave_codigo')
                except Exception:
                    pass
                ok = self._return_key_directly(assignment_id, f"Devolución: {day} {time_range} - {title} ({room})")
                if ok:
                    # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                    self._send_arduino_command(assignment_id, "DEVOLVER")
                    
                    try:
                        from src.core.desktop_alerts import desktop_alert_system
                        desktop_alert_system.show_key_returned_alert(key_code, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    except Exception:
                        if key_code:
                            QMessageBox.information(self.parent, "✅ Llave devuelta", f"Se devolvió la llave {key_code} correctamente")
                        else:
                            QMessageBox.information(self.parent, "✅ Llave devuelta", "Devolución registrada correctamente")
                    # Actualizar estado visual: pendiente
                    self._status_by_day[day] = False
                    self._populate_day(day)
                else:
                    QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")
                return
            except Exception as e:
                QMessageBox.warning(self.parent, "⚠️", f"No fue posible completar la operación: {e}")
                return

        progress = self._show_progress("👆 Escanee su huella para devolver la llave...")
        try:
            validator = FingerprintValidator()
            if not validator.connect():
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo conectar al lector biométrico")
                return
            scanned = validator.scan_fingerprint()
            if not scanned:
                QMessageBox.warning(self.parent, "⚠️ Escaneo", "No se obtuvo huella válida")
                return
            user = validator.validate_fingerprint_against_database(scanned)
            validator.disconnect()
            if not user:
                QMessageBox.critical(self.parent, "Acceso denegado", "Huella no coincide con ningún usuario")
                return
            self._km.authenticate_user(user['id'])
            # Buscar la asignación correcta del usuario
            assignments = self._km.show_user_keys(user['id'])
            if not assignments:
                QMessageBox.information(self.parent, "Sin asignaciones", "No hay llaves activas para devolver")
                return
            
            # Buscar la asignación correcta por ambiente si está disponible
            assignment_id = assignments[-1]['id']  # Por defecto la última
            if ambiente_id:
                for assignment in assignments:
                    # Verificar si la llave pertenece al ambiente correcto
                    try:
                        from src.utils.utils import get_key_environment
                        key_env = get_key_environment(assignment.get('llave_id'))
                        if key_env and key_env.get('id') == ambiente_id:
                            assignment_id = assignment['id']
                            break
                    except Exception:
                        pass
            
            # obtener código de llave para mostrar en mensajes
            key_code = None
            try:
                assignment_obj = next(a for a in assignments if a['id'] == assignment_id)
                key_code = assignment_obj.get('llave_codigo')
            except Exception:
                pass
            ok = self._return_key_directly(assignment_id, f"Devolución: {day} {time_range} - {title} ({room})")
            if ok:
                # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                self._send_arduino_command(assignment_id, "DEVOLVER")
                
                if key_code:
                    QMessageBox.information(self.parent, "✅ Llave devuelta", f"Se devolvió la llave {key_code} correctamente")
                else:
                    QMessageBox.information(self.parent, "✅ Llave devuelta", "Devolución registrada correctamente")
            else:
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")
        finally:
            progress.close()

    def _send_arduino_command(self, key_id_or_assignment_id: int, action: str):
        """
        Envía comando al Arduino para mover el motor NEMA17 a la posición de la llave
        
        Args:
            key_id_or_assignment_id: ID de la llave o asignación
            action: "TOMAR" o "DEVOLVER"
        """
        try:
            from src.utils.utils import open_key_by_id_steps as open_key_by_id, open_environment_key, log_file
            from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
            
            print(f"🤖 Enviando comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            log_file(f"🤖 Comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            
            if action == "TOMAR":
                # Para tomar llave, mover a la posición de la llave
                success = open_key_by_id(key_id_or_assignment_id, dwell_seconds=5)
                if success:
                    print(f"✅ Motor movido a posición de llave {key_id_or_assignment_id}")
                    log_file(f"✅ Motor movido a posición de llave {key_id_or_assignment_id}")
                else:
                    print(f"❌ Error moviendo motor a llave {key_id_or_assignment_id}")
                    log_file(f"❌ Error moviendo motor a llave {key_id_or_assignment_id}")
                    
            elif action == "DEVOLVER":
                # Para devolver llave, mover a posición HOME (0 grados)
                from src.utils.utils import send_home
                try:
                    response = send_home(ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT)
                    if "HOME completado" in response or "Posición" in response:
                        print("✅ Motor movido a posición HOME")
                        log_file("✅ Motor movido a posición HOME")
                    else:
                        print(f"⚠️ Respuesta inesperada del Arduino: {response}")
                        log_file(f"⚠️ Respuesta Arduino: {response}")
                except Exception as e:
                    print(f"❌ Error enviando HOME al Arduino: {e}")
                    log_file(f"❌ Error enviando HOME al Arduino: {e}")
            
        except Exception as e:
            print(f"❌ Error en comando Arduino {action}: {e}")
            log_file(f"❌ Error en comando Arduino {action}: {e}")
            # No mostrar error al usuario para no interrumpir el flujo principal
            # El sistema seguirá funcionando sin el Arduino

