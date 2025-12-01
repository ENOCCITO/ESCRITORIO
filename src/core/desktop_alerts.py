#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
desktop_alerts.py
- Sistema de alertas nativas de escritorio (PySide6)
"""

from typing import Optional

from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt, QTimer


class DesktopAlertSystem:
    """Sistema de alertas nativas de escritorio con diseño futurista (Qt)."""

    def __init__(self):
        self.active_alerts = []

    def show_access_denied_alert(self, role: str, user_name: Optional[str] = None):
        self._create_alert_dialog(
            title="🚫 ACCESO DENEGADO",
            icon="🚫",
            primary_text="Esta huella no corresponde a un",
            role_text=role.upper(),
            secondary_text="La huella digital escaneada no tiene permisos para acceder al módulo solicitado.",
            instruction_text="Por favor, contacte al administrador del sistema para obtener los permisos necesarios.",
            user_name=user_name,
            theme="red",
            auto_close_ms=None
        )

    def show_fingerprint_not_found_alert(self):
        self._create_alert_dialog(
            title="🔍 HUELLA NO RECONOCIDA",
            icon="🔍",
            primary_text="Huella digital no encontrada en el sistema",
            role_text="",
            secondary_text="La huella digital escaneada no se encuentra registrada en la base de datos del sistema.",
            instruction_text="Por favor, asegúrese de que su huella esté registrada en el sistema o contacte al administrador.",
            user_name=None,
            theme="orange",
            auto_close_ms=None
        )

    def show_access_granted_alert(self, role: str, user_name: str):
        self._create_alert_dialog(
            title="✅ ACCESO CONCEDIDO",
            icon="✅",
            primary_text="Bienvenido,",
            role_text=user_name,
            secondary_text=f"Verificación de identidad exitosa. Acceso concedido al módulo de {role.upper()}.",
            instruction_text="Iniciando interfaz del sistema...",
            user_name=None,
            theme="green",
            auto_close_ms=3000
        )

    def show_key_assigned_alert(self, key_code: str, user_name: str):
        self._create_alert_dialog(
            title="🔑 LLAVE ENTREGADA",
            icon="🔑",
            primary_text=f"Se asignó la llave {key_code}",
            role_text=user_name,
            secondary_text="La entrega fue registrada correctamente en el sistema.",
            instruction_text="Recuerde devolverla al finalizar su clase.",
            user_name=None,
            theme="green",
            auto_close_ms=2500,
        )

    def show_key_returned_alert(self, key_code: str | None, user_name: str):
        code_txt = f"{key_code}" if key_code else ""
        self._create_alert_dialog(
            title="↩️ LLAVE DEVUELTA",
            icon="↩️",
            primary_text=(f"Llave {code_txt} devuelta" if code_txt else "Llave devuelta"),
            role_text=user_name,
            secondary_text="La devolución fue registrada correctamente.",
            instruction_text="Gracias por mantener el control de llaves.",
            user_name=None,
            theme="blue",
            auto_close_ms=2500,
        )

    def _create_alert_dialog(
        self,
        *,
        title: str,
        icon: str,
        primary_text: str,
        role_text: str,
        secondary_text: str,
        instruction_text: str,
        user_name: Optional[str],
        theme: str,
        auto_close_ms: Optional[int],
    ) -> QDialog:
        colors = self._get_theme(theme)

        dlg = QDialog()
        dlg.setWindowTitle(title)
        dlg.setModal(True)
        dlg.resize(560, 430)

        root_layout = QVBoxLayout(dlg)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(8)

        border = QWidget(dlg)
        border.setStyleSheet(f"background-color: {colors['accent']}; border-radius: 10px;")
        border_layout = QVBoxLayout(border)
        border_layout.setContentsMargins(2, 2, 2, 2)
        border_layout.setSpacing(0)
        root_layout.addWidget(border)

        content = QWidget(border)
        content.setStyleSheet("background-color: #0e1424; border-radius: 8px;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(10)
        border_layout.addWidget(content)

        title_lbl = QLabel(title, content)
        title_lbl.setAlignment(Qt.AlignHCenter)
        title_lbl.setStyleSheet(f"color: {colors['accent']}; font-size: 20px; font-weight: 700;")
        content_layout.addWidget(title_lbl)

        # Fila de icono grande + título animable
        icon_lbl = QLabel(icon, content)
        icon_lbl.setAlignment(Qt.AlignHCenter)
        icon_lbl.setStyleSheet(f"color: {colors['accent']}; font-size: 64px;")
        content_layout.addWidget(icon_lbl)

        primary_lbl = QLabel(primary_text, content)
        primary_lbl.setAlignment(Qt.AlignHCenter)
        primary_lbl.setStyleSheet("color: #ffffff; font-size: 16px;")
        content_layout.addWidget(primary_lbl)

        if role_text:
            role_lbl = QLabel(role_text, content)
            role_lbl.setAlignment(Qt.AlignHCenter)
            role_lbl.setStyleSheet(f"color: {colors['accent']}; font-size: 18px; font-weight: 700;")
            content_layout.addWidget(role_lbl)

        secondary_lbl = QLabel(secondary_text, content)
        secondary_lbl.setAlignment(Qt.AlignHCenter)
        secondary_lbl.setWordWrap(True)
        secondary_lbl.setStyleSheet("color: #cccccc; font-size: 12px;")
        content_layout.addWidget(secondary_lbl)

        instruction_lbl = QLabel(instruction_text, content)
        instruction_lbl.setAlignment(Qt.AlignHCenter)
        instruction_lbl.setWordWrap(True)
        instruction_lbl.setStyleSheet(f"color: {colors['instruction']}; font-size: 12px; font-weight: 600;")
        content_layout.addWidget(instruction_lbl)

        if user_name:
            user_lbl = QLabel(f"Usuario identificado: {user_name}", content)
            user_lbl.setAlignment(Qt.AlignHCenter)
            user_lbl.setStyleSheet("color: #888888; font-size: 11px;")
            content_layout.addWidget(user_lbl)

        buttons = QWidget(content)
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.setAlignment(Qt.AlignHCenter)
        buttons_layout.setContentsMargins(0, 14, 0, 0)
        content_layout.addWidget(buttons)

        btn_text = "CONTINUAR" if auto_close_ms else "ENTENDIDO"
        main_btn = QPushButton(btn_text, buttons)
        main_btn.setCursor(Qt.PointingHandCursor)
        main_btn.setStyleSheet(
            f"QPushButton {{ background-color: {colors['button']}; color: #ffffff; border: 0; padding: 10px 28px;"
            f"font-weight: 700; border-radius: 8px; }}"
            f"QPushButton:hover {{ background-color: {colors['button']}; }}"
        )
        main_btn.clicked.connect(dlg.accept)
        buttons_layout.addWidget(main_btn)

        if auto_close_ms:
            QTimer.singleShot(auto_close_ms, dlg.accept)

        # Micro-animación de pulso del borde
        try:
            pulse = {"dir": 1, "alpha": 180}
            def tick_pulse():
                a = pulse["alpha"] + 6 * pulse["dir"]
                if a > 240:
                    a = 240; pulse["dir"] = -1
                if a < 140:
                    a = 140; pulse["dir"] = 1
                pulse["alpha"] = a
                border.setStyleSheet(f"background-color: rgba({int(colors['accent'][1:3],16) if colors['accent'].startswith('#') else 255},0,0,0); border-radius: 10px;")
                # fallback: solo cambiar sombra no fiable con QSS puro; omitimos más cambios para no arriesgar
            t = QTimer(dlg)
            t.timeout.connect(tick_pulse)
            t.start(120)
            dlg._pulse_timer = t
        except Exception:
            pass

        self.active_alerts.append(dlg)
        dlg.finished.connect(lambda _: self._remove_dialog(dlg))
        dlg.exec()
        return dlg

    def _remove_dialog(self, dlg: QDialog):
        try:
            if dlg in self.active_alerts:
                self.active_alerts.remove(dlg)
        except Exception:
            pass

    def _get_theme(self, name: str) -> dict:
        themes = {
            "red": {
                "accent": "#ff6b6b",
                "button": "#ff6b6b",
                "instruction": "#ffd93d",
            },
            "orange": {
                "accent": "#ffa726",
                "button": "#ffa726",
                "instruction": "#ffd93d",
            },
            "green": {
                "accent": "#4caf50",
                "button": "#4caf50",
                "instruction": "#81c784",
            },
            "blue": {
                "accent": "#00bcd4",
                "button": "#00bcd4",
                "instruction": "#80deea",
            },
        }
        return themes.get(name, themes["red"])

    def close_all_alerts(self):
        for dlg in self.active_alerts[:]:
            try:
                dlg.reject()
            except Exception:
                pass
        self.active_alerts.clear()

    def cleanup(self):
        self.close_all_alerts()


# Instancia global del sistema de alertas de escritorio
desktop_alert_system = DesktopAlertSystem()
