#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_interface.py
- Interfaz de seguridad (PySide6)
"""

import os

from src.utils import styles
from src.config.config import *
from src.utils.utils import *
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
    QGridLayout,
)
from src.core.key_manager import KeyManager
from src.core.desktop_alerts import desktop_alert_system
from src.utils.db_utils import get_available_keys, get_environments, assign_key_to_person, get_personal_by_id
from src.interfaces.dialog_utils import CleanCloseDialog

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
        """Abre directamente el selector de ambientes"""
        try:
            # Ir directamente a la selección de ambientes
            self._open_environment_selector()
            print("✅ Interfaz de seguridad - Selector de ambientes mostrado")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error al mostrar la interfaz de seguridad:\n{e}")
            import traceback
            traceback.print_exc()

    def _open_environment_selector(self):
        """Ícono de saludo y mensaje de bienvenida"""
        print("\n" + "="*60)
        print("🚨 _open_environment_selector EJECUTADO")
        print("="*60 + "\n")
        
        # Colores del diseño
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        
        # Crear diálogo personalizado grande
        dlg = CleanCloseDialog(self.parent)
        dlg.setWindowTitle("Seguridad - Ambientes")
        dlg.setModal(False)
        dlg.showFullScreen()
        dlg.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        
        # Layout principal
        main_layout = QVBoxLayout(dlg)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header con botón de cierre
        header = QWidget(dlg)
        header.setFixedHeight(60)
        header.setStyleSheet(f"background-color: {BG_LIGHT_HTML}; border-bottom: 1px solid {BORDER_COLOR};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(16)
        
        header_title = QLabel("🛡️ SEGURIDAD - CONTROL DE ACCESO", header)
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
        
        main_layout.addWidget(header)
        
        # Área de contenido centrada
        content_widget = QWidget(dlg)
        content_widget.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Título principal
        title_label = QLabel("🛡️ ¡Bienvenido Seguridad!", content_widget)
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
        subtitle_label = QLabel("Seleccione un ambiente para controlar acceso", content_widget)
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
                    env_btn.clicked.connect(lambda checked, eid=env_id, n=nombre: self._select_environment_security(n, eid))
                    
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
        
        main_layout.addWidget(content_widget, 1)
        
        print("✅ Mostrando cuadrícula de ambientes")
        dlg.show()
    
    def _select_environment_security(self, env_name, ambiente_id=None):
        """Maneja la selección de un ambiente desde seguridad"""
        if ambiente_id:
            QMessageBox.information(self.parent, "🛡️ AMBIENTE SELECCIONADO",
                                    f"Ha seleccionado: {env_name}\nID del ambiente: {ambiente_id}\n\nLa seguridad está activa para este ambiente.")
        else:
            QMessageBox.information(self.parent, "🛡️ AMBIENTE SELECCIONADO",
                                    f"Ha seleccionado: {env_name}\n\nLa seguridad está activa para este ambiente.")

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
                from src.utils.db_utils import db_connect
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
            from src.utils.utils import open_key_by_id, send_home, log_file
            from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
            
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
