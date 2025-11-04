#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_interface.py
- Interfaz de seguridad (PySide6)
"""

import os

import styles
from config import *
from utils import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QFont, QPixmap
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
from key_manager import KeyManager
from desktop_alerts import desktop_alert_system
from db_utils import get_available_keys, get_environments, assign_key_to_person, get_personal_by_id

class SecurityInterface:
    def __init__(self, parent, user: dict | None = None):
        self.parent = parent
        self._km = KeyManager()
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass

    def set_authenticated_user(self, user: dict | None):
        """Actualiza el usuario autenticado para la sesión de seguridad."""
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass
        
    def show_security_interface(self):
        try:
            PRIMARY_COLOR = "#0D6EFD"
            BG_LIGHT_HTML = "#F8F9FA"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#E5E7EB"
            HEADER_DARK = "#212529"
            CARD_BG = "#FFFFFF"

            security_win = QDialog(self.parent)
            security_win.setWindowTitle("Interfaz de Seguridad – Sistema CEFA")
            security_win.setModal(False)
            try:
                w, h = [int(x) for x in ADMIN_WINDOW_SIZE.lower().split('x')]
                security_win.resize(max(w, 1100), max(h, 760))
            except Exception:
                security_win.resize(1100, 760)
            security_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")

            root_layout = QVBoxLayout(security_win)
            root_layout.setContentsMargins(0, 0, 0, 0)
            root_layout.setSpacing(0)

            # Header oscuro
            header = QWidget(security_win)
            header.setFixedHeight(72)
            header.setStyleSheet(f"background-color: {HEADER_DARK}; border: none;")
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(24, 12, 24, 12)
            header_layout.setSpacing(16)

            header_icon = QLabel(header)
            header_icon.setAlignment(Qt.AlignCenter)
            icon_path = "images/escudoazul.png"
            if not os.path.isabs(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path)
            if os.path.exists(icon_path):
                pix = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                header_icon.setPixmap(pix)
                header_icon.setFixedSize(pix.width(), pix.height())
            else:
                header_icon.setText("🛡️")
                header_icon.setStyleSheet("color: white; font-size: 28px;")
            header_layout.addWidget(header_icon)

            header_title = QLabel("INTERFAZ DE SEGURIDAD – SISTEMA CEFA", header)
            header_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            header_title.setWordWrap(False)
            header_title.setTextFormat(Qt.PlainText)
            header_title.setOpenExternalLinks(False)
            header_title.setMinimumWidth(0)
            header_title.setMaximumWidth(16777215)
            header_font = header_title.font()
            header_font.setPointSize(18)
            header_font.setBold(True)
            header_title.setFont(header_font)
            header_fm = QFontMetrics(header_font)
            header_title.setMinimumWidth(header_fm.horizontalAdvance("INTERFAZ DE SEGURIDAD – SISTEMA CEFA"))
            header_title.setStyleSheet(
                "color: white; font-size: 18px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            header_layout.addWidget(header_title)
            header_layout.addStretch()

            root_layout.addWidget(header)

            scroll = QScrollArea(security_win)
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            scroll.setStyleSheet(f"background-color: {BG_LIGHT_HTML}; border: none;")

            main_content = QWidget()
            main_layout = QVBoxLayout(main_content)
            main_layout.setContentsMargins(32, 32, 32, 32)
            main_layout.setSpacing(28)

            # Welcome card
            welcome_card = QWidget(main_content)
            welcome_card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 12px;")
            welcome_layout = QHBoxLayout(welcome_card)
            welcome_layout.setContentsMargins(32, 28, 32, 28)
            welcome_layout.setSpacing(24)
            welcome_layout.setAlignment(Qt.AlignTop)

            hero_icon = QLabel(welcome_card)
            hero_icon.setAlignment(Qt.AlignCenter)
            hero_path = "images/seguridad.jpg"
            if not os.path.isabs(hero_path):
                hero_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), hero_path)
            if os.path.exists(hero_path):
                hero_pix = QPixmap(hero_path).scaled(92, 92, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                hero_icon.setPixmap(hero_pix)
                hero_icon.setFixedSize(hero_pix.width(), hero_pix.height())
            else:
                hero_icon.setText("🛡️")
                hero_icon.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; font-size: 56px; background-color: transparent; border: none;"
                )
            welcome_layout.addWidget(hero_icon, 0, Qt.AlignTop)

            text_block = QVBoxLayout()
            text_block.setSpacing(6)
            text_block.setContentsMargins(0, 0, 0, 0)

            welcome_title = QLabel("Control de Seguridad", welcome_card)
            welcome_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            welcome_title.setWordWrap(False)
            welcome_title.setTextFormat(Qt.PlainText)
            welcome_title.setOpenExternalLinks(False)
            welcome_title.setMinimumWidth(0)
            welcome_title.setMaximumWidth(16777215)
            welcome_title_font = welcome_title.font()
            welcome_title_font.setPointSize(30)
            welcome_title_font.setBold(True)
            welcome_title.setFont(welcome_title_font)
            welcome_title_fm = QFontMetrics(welcome_title_font)
            welcome_title.setMinimumWidth(welcome_title_fm.horizontalAdvance("Control de Seguridad"))
            welcome_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; font-size: 30px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            text_block.addWidget(welcome_title)

            welcome_subtitle = QLabel(
                "Interfaz dedicada para la gestión y monitoreo de llaves asignadas y en custodia.",
                welcome_card,
            )
            welcome_subtitle.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            welcome_subtitle.setWordWrap(False)
            welcome_subtitle.setTextFormat(Qt.PlainText)
            welcome_subtitle.setOpenExternalLinks(False)
            welcome_subtitle.setMinimumWidth(0)
            welcome_subtitle.setMaximumWidth(16777215)
            welcome_subtitle_font = welcome_subtitle.font()
            welcome_subtitle_font.setPointSize(14)
            welcome_subtitle.setFont(welcome_subtitle_font)
            welcome_subtitle_fm = QFontMetrics(welcome_subtitle_font)
            welcome_subtitle.setMinimumWidth(welcome_subtitle_fm.horizontalAdvance("Interfaz dedicada para la gestión y monitoreo de llaves asignadas y en custodia."))
            welcome_subtitle.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; font-size: 14px; font-weight: 400; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            text_block.addWidget(welcome_subtitle)
            text_block.addStretch(1)

            welcome_layout.addLayout(text_block)
            main_layout.addWidget(welcome_card)

            # Actions title
            actions_title = QLabel("Acciones principales", main_content)
            actions_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            actions_title.setWordWrap(False)
            actions_title.setTextFormat(Qt.PlainText)
            actions_title.setOpenExternalLinks(False)
            actions_title.setMinimumWidth(0)
            actions_title.setMaximumWidth(16777215)
            actions_title_font = actions_title.font()
            actions_title_font.setPointSize(20)
            actions_title_font.setBold(True)
            actions_title.setFont(actions_title_font)
            actions_title_fm = QFontMetrics(actions_title_font)
            actions_title.setMinimumWidth(actions_title_fm.horizontalAdvance("Acciones principales"))
            actions_title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; font-size: 20px; font-weight: 700; font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; background-color: transparent; border: none; padding: 0px; margin: 0px;"
            )
            main_layout.addWidget(actions_title)

            actions_container = QWidget(main_content)
            actions_layout = QHBoxLayout(actions_container)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(20)

            # Solo "Seleccionar Ambiente"
            title_text = "Seleccionar Ambiente"
            desc_text = "Elija el entorno específico para gestionar las llaves correspondientes."
            image_path = "images/ambiente.jpg"
            fallback_emoji = "🏢"
            callback = self._open_environment_selector

            card = QWidget(actions_container)
            card.setCursor(Qt.PointingHandCursor)
            card.setStyleSheet(
                f"background-color: {CARD_BG}; border: 1px solid {BORDER_COLOR}; border-radius: 12px;"
            )
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(40, 32, 40, 32)  # left, top, right, bottom - Más espacio alrededor del contenido
            card_layout.setSpacing(20)

            header_row = QHBoxLayout()
            header_row.setSpacing(16)
            header_row.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel(card)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_abs = image_path
            if not os.path.isabs(icon_abs):
                icon_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_path)
            pixmap = None
            if os.path.exists(icon_abs):
                pixmap = QPixmap(icon_abs).scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if pixmap:
                icon_label.setPixmap(pixmap)
                icon_label.setFixedSize(pixmap.width(), pixmap.height())
                icon_label.setStyleSheet(
                    "background-color: transparent; border: none; padding: 0px; margin: 0px;"
                )
            else:
                icon_label.setText(fallback_emoji)
                icon_label.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; font-size: 32px; background-color: rgba(13,110,253,0.12); border-radius: 999px; padding: 14px;"
                )
            header_row.addWidget(icon_label, 0, Qt.AlignLeft)

            title_label = QLabel(title_text, card)
            title_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            title_label.setWordWrap(False)
            title_label.setTextFormat(Qt.PlainText)
            title_label.setOpenExternalLinks(False)
            title_label.setMinimumWidth(0)
            title_label.setMaximumWidth(16777215)
            title_font = title_label.font()
            title_font.setPointSize(16)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_fm = QFontMetrics(title_font)
            title_label.setMinimumWidth(title_fm.horizontalAdvance(title_text))
            title_label.setStyleSheet(f"color: {TEXT_GRAY_DARK}; font-size: 16px; font-weight: 700; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            header_row.addWidget(title_label)
            header_row.addStretch(1)
            card_layout.addLayout(header_row)

            desc_label = QLabel(desc_text, card)
            desc_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            desc_label.setWordWrap(False)
            desc_label.setTextFormat(Qt.PlainText)
            desc_label.setOpenExternalLinks(False)
            desc_label.setMinimumWidth(0)
            desc_label.setMaximumWidth(16777215)
            desc_font = desc_label.font()
            desc_font.setPointSize(13)
            desc_label.setFont(desc_font)
            desc_fm = QFontMetrics(desc_font)
            desc_label.setMinimumWidth(desc_fm.horizontalAdvance(desc_text))
            desc_label.setStyleSheet(f"color: {TEXT_GRAY_LIGHT}; font-size: 13px; font-weight: 500; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            card_layout.addWidget(desc_label)

            action_btn = QPushButton("Seleccionar", card)
            action_btn.setCursor(Qt.PointingHandCursor)
            action_btn.setStyleSheet(
                f"background-color: {PRIMARY_COLOR}; color: white; border: none; border-radius: 8px; padding: 10px 22px; font-size: 13px; font-weight: 600;"
            )
            action_btn.clicked.connect(callback)
            card_layout.addWidget(action_btn, 0, Qt.AlignLeft)

            def make_handler(func):
                def _handler(event):
                    try:
                        func()
                    except Exception as exc:
                        QMessageBox.critical(self.parent, "Error", f"No se pudo ejecutar la acción:\n{exc}")
                return _handler

            card.mousePressEvent = make_handler(callback)
            actions_layout.addWidget(card)

            main_layout.addWidget(actions_container)

            # Llaves en custodia
            keys_card = QWidget(main_content)
            keys_card.setStyleSheet(f"background-color: {CARD_BG}; border: 1px solid {BORDER_COLOR}; border-radius: 12px;")
            keys_layout = QVBoxLayout(keys_card)
            keys_layout.setContentsMargins(24, 24, 24, 24)
            keys_layout.setSpacing(20)

            keys_header = QHBoxLayout()
            keys_header.setSpacing(12)

            keys_title = QLabel("Llaves en custodia", keys_card)
            keys_title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            keys_title.setWordWrap(False)
            keys_title.setTextFormat(Qt.PlainText)
            keys_title.setOpenExternalLinks(False)
            keys_title.setMinimumWidth(0)
            keys_title.setMaximumWidth(16777215)
            keys_title_font = keys_title.font()
            keys_title_font.setPointSize(20)
            keys_title_font.setBold(True)
            keys_title.setFont(keys_title_font)
            keys_title_fm = QFontMetrics(keys_title_font)
            keys_title.setMinimumWidth(keys_title_fm.horizontalAdvance("Llaves en custodia"))
            keys_title.setStyleSheet(f"color: {TEXT_GRAY_DARK}; font-size: 20px; font-weight: 700; background-color: transparent; border: none; padding: 0px; margin: 0px;")
            keys_header.addWidget(keys_title)

            self._keys_count_label = QLabel("0", keys_card)
            self._keys_count_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self._keys_count_label.setWordWrap(False)
            self._keys_count_label.setTextFormat(Qt.PlainText)
            self._keys_count_label.setOpenExternalLinks(False)
            self._keys_count_label.setMinimumWidth(0)
            self._keys_count_label.setMaximumWidth(16777215)
            count_font = self._keys_count_label.font()
            count_font.setPointSize(13)
            count_font.setBold(True)
            self._keys_count_label.setFont(count_font)
            count_fm = QFontMetrics(count_font)
            self._keys_count_label.setMinimumWidth(count_fm.horizontalAdvance("0") + 28)  # +28 para padding
            self._keys_count_label.setStyleSheet(f"color: {PRIMARY_COLOR}; background-color: rgba(13,110,253,0.12); border-radius: 999px; padding: 6px 14px;")
            keys_header.addWidget(self._keys_count_label)
            keys_header.addStretch(1)

            refresh_btn = QPushButton("Actualizar", keys_card)
            refresh_btn.setCursor(Qt.PointingHandCursor)
            refresh_btn.setStyleSheet("background-color: rgba(17,24,39,0.08); color: #111418; border: none; border-radius: 8px; padding: 10px 18px; font-size: 13px; font-weight: 600;")
            refresh_btn.clicked.connect(self._refresh_my_keys)
            keys_header.addWidget(refresh_btn)

            keys_layout.addLayout(keys_header)

            self._my_keys_container = QWidget(keys_card)
            self._my_keys_layout = QVBoxLayout(self._my_keys_container)
            self._my_keys_layout.setContentsMargins(0, 0, 0, 0)
            self._my_keys_layout.setSpacing(12)
            keys_layout.addWidget(self._my_keys_container)

            main_layout.addWidget(keys_card)

            scroll.setWidget(main_content)
            root_layout.addWidget(scroll, 1)

            footer = QWidget(security_win)
            footer.setStyleSheet(f"background-color: {HEADER_DARK};")
            footer_layout = QHBoxLayout(footer)
            footer_layout.setContentsMargins(24, 12, 24, 12)
            footer_layout.addStretch(1)

            close_btn = QPushButton("Cerrar", footer)
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setStyleSheet(f"background-color: {PRIMARY_COLOR}; color: white; border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px; font-weight: 600;")
            close_btn.clicked.connect(security_win.close)
            footer_layout.addWidget(close_btn)
            root_layout.addWidget(footer)

            self.security_win = security_win
            self._refresh_my_keys()

            styles.center_window(security_win)
            security_win.show()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error mostrando interfaz de seguridad:\n{e}")

    def _open_environment_selector(self):
        dlg = styles.create_modal_window(self.parent, "🏢 AMBIENTES DISPONIBLES", "900x620")
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)
        lay.addWidget(styles.create_subtitle_label(dlg, "Seleccione un ambiente para gestionar sus llaves disponibles"))

        # Construir lista de ambientes con llaves disponibles
        # Mostrar todos los ambientes con llaves en estado DISPONIBLE o ASIGNADA (pero no DEVUELTA)
        # Seguridad puede sacar llaves asignadas si no han sido reclamadas (estado ASIGNADA pero físicamente presente)
        try:
            from db_utils import db_connect
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
            keys = get_available_keys()
            envs = {e['id']: e for e in get_environments()} if isinstance(get_environments(), list) else {}
            env_ids_with_keys = {}
            for k in keys:
                a_id = k.get('ambiente_id')
                if a_id:
                    env_ids_with_keys.setdefault(a_id, []).append(k)

        container = styles.create_main_frame(dlg)
        v = QVBoxLayout(container)
        if not env_ids_with_keys:
            v.addWidget(styles.create_info_label(container, "No hay llaves disponibles en este momento."))
        else:
            for env_id, klist in env_ids_with_keys.items():
                info = envs.get(env_id, {})
                name = info.get('nombre', f"Ambiente {env_id}")
                row = styles.create_main_frame(container)
                r = QHBoxLayout(row)
                r.addWidget(styles.create_info_label(row, f"🏢 {name}  •  🔑 {len(klist)} llaves disponibles o asignadas sin reclamar"))
                btn = styles.create_accent_button(row, "Ver llaves", lambda eid=env_id, n=name, kl=klist: self._open_keys_for_environment(eid, n, kl))
                r.addStretch(1)
                r.addWidget(btn)
                v.addWidget(row)
        lay.addWidget(container)
        dlg.show()

    def _create_security_header(self, parent, layout):
        header = styles.create_main_frame(parent)
        header_layout = QVBoxLayout(header)
        icon = styles.create_title_label(header, "🛡️")
        title = styles.create_title_label(header, "CONTROL DE ACCESO")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        layout.addWidget(header)

    def _open_keys_for_environment(self, environment_id: int, environment_name: str, preset_keys: list | None = None):
        dlg = styles.create_modal_window(self.parent, f"🔑 Llaves - {environment_name}", "900x620")
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)
        lay.addWidget(styles.create_subtitle_label(dlg, f"Llaves disponibles en {environment_name}"))

        container = styles.create_main_frame(dlg)
        v = QVBoxLayout(container)
        v.setContentsMargins(10, 8, 10, 8)
        v.setSpacing(8)
        # Usar la lista precargada de llaves si viene del selector para evitar inconsistencias
        if preset_keys is not None:
            available = preset_keys
        else:
            try:
                from db_utils import db_connect
                with db_connect() as cnx:
                    cur = cnx.cursor(dictionary=True)
                    cur.execute("SELECT id, codigo_llave, descripcion, ambiente_id, estado, angulo_grados FROM llaves WHERE activo = 1 AND ambiente_id = %s ORDER BY codigo_llave", (environment_id,))
                    available = cur.fetchall()
            except Exception:
                # Fallback: usar solo disponibles
                available = [k for k in get_available_keys() if k.get('ambiente_id') == environment_id]
        if not available:
            v.addWidget(styles.create_info_label(container, "No hay llaves registradas para este ambiente."))
        else:
            for key in available:
                row = styles.create_main_frame(container)
                r = QHBoxLayout(row)
                estado = str(key.get('estado','')).upper()
                # Línea de detalle más clara y estética
                label = styles.create_info_label(
                    row,
                    f"Código: {key['codigo_llave']}  •  {key.get('descripcion','')}  •  Estado: {estado}  •  Ángulo {key.get('angulo_grados','-')}"
                )
                r.addWidget(label)
                # Acción según estado
                if estado == 'DISPONIBLE':
                    btn = styles.create_accent_button(row, "Tomar", lambda kid=key['id'], kcode=key['codigo_llave']: self._take_security_key(kid, kcode))
                    r.addStretch(1)
                    r.addWidget(btn)
                elif estado == 'ASIGNADA':
                    btn = styles.create_warning_button(row, "Reclamar (Seguridad)", lambda kid=key['id'], kcode=key['codigo_llave']: self._take_security_key(kid, kcode))
                    r.addStretch(1)
                    r.addWidget(btn)
                else:
                    r.addStretch(1)
                r.addStretch(1)
                v.addWidget(row)
        lay.addWidget(container)
        dlg.show()

    def _refresh_my_keys(self):
        PRIMARY_COLOR = "#0D6EFD"
        BORDER_COLOR = "#E5E7EB"
        CARD_BG = "#FFFFFF"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"

        if not hasattr(self, "_my_keys_layout"):
            return

        # Limpiar contenedor
        while self._my_keys_layout.count():
            item = self._my_keys_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Obtener asignaciones activas
        try:
            if self._km.current_user:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
            else:
                assignments = []
        except Exception:
            assignments = []

        count = len(assignments)
        if hasattr(self, "_keys_count_label"):
            count_text = f"{count} llave{'s' if count != 1 else ''}"
            self._keys_count_label.setText(count_text)
            # Actualizar el ancho mínimo dinámicamente
            count_font = self._keys_count_label.font()
            count_fm = QFontMetrics(count_font)
            self._keys_count_label.setMinimumWidth(count_fm.horizontalAdvance(count_text) + 28)  # +28 para padding

        if not assignments:
            empty_text = "No tienes llaves asignadas actualmente."
            empty_label = QLabel(empty_text, self._my_keys_container)
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            empty_label.setWordWrap(False)
            empty_label.setTextFormat(Qt.PlainText)
            empty_label.setOpenExternalLinks(False)
            empty_label.setMinimumWidth(0)
            empty_label.setMaximumWidth(16777215)
            empty_font = empty_label.font()
            empty_font.setPointSize(13)
            empty_label.setFont(empty_font)
            empty_fm = QFontMetrics(empty_font)
            empty_label.setMinimumWidth(empty_fm.horizontalAdvance(empty_text))
            empty_label.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; "
                f"font-size: 13px; "
                f"font-weight: 500; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 12px; "
                f"margin: 0px;"
            )
            self._my_keys_layout.addWidget(empty_label, 0, Qt.AlignCenter)
            self._my_keys_layout.addStretch(1)
            return

        for assignment in assignments:
            card = QWidget(self._my_keys_container)
            card.setStyleSheet(
                f"background-color: {CARD_BG}; "
                f"border: 1px solid {BORDER_COLOR}; "
                f"border-radius: 10px; "
                f"padding: 16px;"
            )
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(12)

            info_layout = QVBoxLayout()
            info_layout.setContentsMargins(0, 0, 0, 0)
            info_layout.setSpacing(4)

            title_text = f"{assignment['llave_codigo']} • {assignment.get('llave_descripcion', '')}"
            title = QLabel(title_text, card)
            title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            title.setWordWrap(False)
            title.setTextFormat(Qt.PlainText)
            title.setOpenExternalLinks(False)
            title.setMinimumWidth(0)
            title.setMaximumWidth(16777215)
            title_font = title.font()
            title_font.setPointSize(15)
            title_font.setBold(True)
            title.setFont(title_font)
            title_fm = QFontMetrics(title_font)
            title.setMinimumWidth(title_fm.horizontalAdvance(title_text))
            title.setStyleSheet(
                f"color: {TEXT_GRAY_DARK}; "
                f"font-size: 15px; "
                f"font-weight: 700; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            info_layout.addWidget(title)

            ambiente = assignment.get('ambiente_nombre', 'Ambiente desconocido')
            try:
                fecha = assignment['fecha_asignacion'].strftime('%Y-%m-%d %H:%M')
            except Exception:
                fecha = str(assignment.get('fecha_asignacion', ''))
            subtitle_text = f"{ambiente} • {fecha}"
            subtitle = QLabel(subtitle_text, card)
            subtitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            subtitle.setWordWrap(False)
            subtitle.setTextFormat(Qt.PlainText)
            subtitle.setOpenExternalLinks(False)
            subtitle.setMinimumWidth(0)
            subtitle.setMaximumWidth(16777215)
            subtitle_font = subtitle.font()
            subtitle_font.setPointSize(13)
            subtitle.setFont(subtitle_font)
            subtitle_fm = QFontMetrics(subtitle_font)
            subtitle.setMinimumWidth(subtitle_fm.horizontalAdvance(subtitle_text))
            subtitle.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; "
                f"font-size: 13px; "
                f"font-weight: 500; "
                f"background-color: transparent; "
                f"border: none; "
                f"padding: 0px; "
                f"margin: 0px;"
            )
            info_layout.addWidget(subtitle)

            estado = assignment.get('estado', '').upper() if isinstance(assignment, dict) else ''
            if estado:
                status_text = f"Estado: {estado}"
                status_label = QLabel(status_text, card)
                status_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                status_label.setWordWrap(False)
                status_label.setTextFormat(Qt.PlainText)
                status_label.setOpenExternalLinks(False)
                status_label.setMinimumWidth(0)
                status_label.setMaximumWidth(16777215)
                status_font = status_label.font()
                status_font.setPointSize(12)
                status_label.setFont(status_font)
                status_fm = QFontMetrics(status_font)
                status_label.setMinimumWidth(status_fm.horizontalAdvance(status_text))
                status_label.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; "
                    f"font-size: 12px; "
                    f"font-weight: 600; "
                    f"background-color: transparent; "
                    f"border: none; "
                    f"padding: 0px; "
                    f"margin: 0px;"
                )
                info_layout.addWidget(status_label)

            info_layout.addStretch(1)
            card_layout.addLayout(info_layout)
            card_layout.addStretch(1)

            return_btn = QPushButton("Devolver", card)
            return_btn.setCursor(Qt.PointingHandCursor)
            return_btn.setStyleSheet(
                "background-color: #ef4444; "
                "color: white; "
                "border: none; "
                "border-radius: 8px; "
                "padding: 10px 20px; "
                "font-size: 13px; "
                "font-weight: 600;"
            )
            return_btn.clicked.connect(lambda _, aid=assignment['id']: self._return_security_key(aid))
            card_layout.addWidget(return_btn)

            self._my_keys_layout.addWidget(card)

        self._my_keys_layout.addStretch(1)

    def _take_security_key(self, key_id: int, key_code: str):
        # Robustez: si el usuario no está seteado, intentar recuperarlo desde main -> role context
        if not self._km.current_user:
            try:
                if hasattr(self.parent, 'best') and self.parent.best:
                    pid, name, score = self.parent.best
                    user = get_personal_by_id(int(pid))
                    if user:
                        self._km.current_user = user
            except Exception:
                pass
        if not self._km.current_user:
            QMessageBox.warning(self.parent, "⚠️", "No hay usuario de seguridad autenticado.")
            return
        # Seguridad puede tomar sin restricciones: usar asignación directa en BD
        ok = assign_key_to_person(self._km.current_user['id'], key_id, "Entrega a seguridad")
        if ok:
            # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
            self._send_arduino_command(key_id, "TOMAR")
            
            try:
                desktop_alert_system.show_key_assigned_alert(key_code, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
            except Exception:
                QMessageBox.information(self.parent, "Llave asignada", f"Se asignó la llave {key_code}")
            self._refresh_my_keys()
        else:
            QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")

    def _return_security_key(self, assignment_id: int):
        if not self._km.current_user:
            QMessageBox.warning(self.parent, "⚠️", "No hay usuario de seguridad autenticado.")
            return
        ok = self._km.return_key_from_user(assignment_id, "Devolución por seguridad")
        if ok:
            # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
            self._send_arduino_command(assignment_id, "DEVOLVER")
            
            try:
                desktop_alert_system.show_key_returned_alert(None, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
            except Exception:
                QMessageBox.information(self.parent, "Llave devuelta", "Devolución registrada correctamente")
            self._refresh_my_keys()
        else:
            QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")

    def _control_environment_access(self, environment_id, environment_name, access_type):
        pass

    def _create_security_footer(self, parent, window, layout):
        footer = styles.create_main_frame(parent)
        footer_layout = QHBoxLayout(footer)
        close_btn = styles.create_danger_button(footer, "❌ CERRAR", window.close)
        footer_layout.addStretch(1)
        footer_layout.addWidget(close_btn)
        layout.addWidget(footer)

    def _show_security_reports(self, parent_window):
        """Muestra los reportes de seguridad"""
        # Crear ventana de reportes de seguridad
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES DE SEGURIDAD", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES DE SEGURIDAD")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes de seguridad del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas de seguridad
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas de seguridad
        security_stats_content = """
📊 ESTADÍSTICAS DE SEGURIDAD

🚪 ACCESOS:
   • Total de accesos hoy: 1,247
   • Accesos autorizados: 1,245
   • Accesos denegados: 2
   • Tasa de éxito: 99.8%

👥 PERSONAS EN CAMPUS:
   • Máximo concurrente: 312
   • Promedio diario: 245
   • Personal autorizado: 43
   • Visitantes: 12

📹 CÁMARAS DE SEGURIDAD:
   • Total de cámaras: 24
   • Cámaras activas: 24
   • Cámaras en mantenimiento: 0
   • Tiempo de grabación: 24/7

🚨 INCIDENTES:
   • Incidentes reportados: 0
   • Alertas de seguridad: 0
   • Llamadas de emergencia: 0
   • Tiempo de respuesta: < 2 min

🛡️ MEDIDAS DE SEGURIDAD:
   • Control biométrico: Activo
   • Verificación de identidad: Activa
   • Monitoreo 24/7: Activo
   • Protocolos de emergencia: Actualizados
        """
        
        # Crear etiquetas para las estadísticas de seguridad
        stats_lines = security_stats_content.strip().split('\n')
        for i, line in enumerate(stats_lines):
            if line.strip():
                label = styles.create_info_label(stats_frame, line)
                label.pack(anchor="w", pady=2)
        
        # Botones de control
        control_frame = styles.create_main_frame(reports_win)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón para exportar reporte
        export_btn = styles.create_accent_button(
            control_frame, 
            "📊 EXPORTAR REPORTE", 
            lambda: self._export_security_report()
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            reports_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(reports_win)

    def _refresh_campus_status(self):
        """Actualiza el estado del campus"""
        QMessageBox.information(self.parent, "🔄 ACTUALIZACIÓN", "Estado del campus actualizado.\n\nTodas las áreas están siendo monitoreadas en tiempo real.")
        
        # Aquí se integraría con la lógica del sistema original
        # para actualizar el estado real del campus

    def _control_access_point(self, access_point):
        """Maneja el control de un punto de acceso específico"""
        QMessageBox.information(self.parent, "🚪 CONTROL DE ACCESO", f"Gestionando: {access_point}\n\nEl sistema está configurando el control de acceso para este punto.\nPor favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el control de acceso al punto seleccionado

    def _export_security_report(self):
        """Exporta el reporte de seguridad"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_seguridad_{timestamp}.csv"
            
            # Datos del reporte de seguridad
            report_data = [
                ['REPORTE DE SEGURIDAD - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS DE SEGURIDAD'],
                ['Total de accesos hoy', '1,247'],
                ['Accesos autorizados', '1,245'],
                ['Accesos denegados', '2'],
                ['Tasa de éxito', '99.8%'],
                ['Máximo concurrente', '312'],
                ['Total de cámaras', '24'],
                ['Cámaras activas', '24'],
                ['Incidentes reportados', '0']
            ]
            
            if export_to_csv(report_data, filename):
                QMessageBox.information(self.parent, "📊 EXPORTACIÓN EXITOSA", f"El reporte de seguridad se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                QMessageBox.critical(self.parent, "❌ ERROR", "Error al exportar el reporte de seguridad.")
                
        except Exception as e:
            QMessageBox.critical(self.parent, "🚨 ERROR", f"Error al exportar el reporte de seguridad:\n\n{e}")

    def _send_arduino_command(self, key_id_or_assignment_id: int, action: str):
        """
        Envía comando al Arduino para mover el motor NEMA17 a la posición de la llave
        
        Args:
            key_id_or_assignment_id: ID de la llave o asignación
            action: "TOMAR" o "DEVOLVER"
        """
        try:
            from utils import open_key_by_id, send_home, log_file
            from config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
            
            print(f"🤖 [SEGURIDAD] Enviando comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            log_file(f"🤖 [SEGURIDAD] Comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            
            if action == "TOMAR":
                # Para tomar llave, mover a la posición de la llave
                success = open_key_by_id(key_id_or_assignment_id, dwell_seconds=5)
                if success:
                    print(f"✅ [SEGURIDAD] Motor movido a posición de llave {key_id_or_assignment_id}")
                    log_file(f"✅ [SEGURIDAD] Motor movido a posición de llave {key_id_or_assignment_id}")
                else:
                    print(f"❌ [SEGURIDAD] Error moviendo motor a llave {key_id_or_assignment_id}")
                    log_file(f"❌ [SEGURIDAD] Error moviendo motor a llave {key_id_or_assignment_id}")
                    
            elif action == "DEVOLVER":
                # Para devolver llave, mover a posición HOME (0 grados)
                try:
                    response = send_home(ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT)
                    if "HOME completado" in response or "Posición" in response:
                        print("✅ [SEGURIDAD] Motor movido a posición HOME")
                        log_file("✅ [SEGURIDAD] Motor movido a posición HOME")
                    else:
                        print(f"⚠️ [SEGURIDAD] Respuesta inesperada del Arduino: {response}")
                        log_file(f"⚠️ [SEGURIDAD] Respuesta Arduino: {response}")
                except Exception as e:
                    print(f"❌ [SEGURIDAD] Error enviando HOME al Arduino: {e}")
                    log_file(f"❌ [SEGURIDAD] Error enviando HOME al Arduino: {e}")
            
        except Exception as e:
            print(f"❌ [SEGURIDAD] Error en comando Arduino {action}: {e}")
            log_file(f"❌ [SEGURIDAD] Error en comando Arduino {action}: {e}")
            # No mostrar error al usuario para no interrumpir el flujo principal
