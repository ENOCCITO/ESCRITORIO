#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
- Archivo principal del sistema de dispensación biométrica
- Integra todas las interfaces y mantiene la funcionalidad original (PySide6)
"""

import json
import time
import threading
import os
from datetime import datetime
from typing import List, Tuple, Optional

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, QObject, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap

# Importar módulos separados
import styles
from config import *
from utils import (
    _import_mysql, _import_pyfingerprint, _import_serial,
    db_connect, load_candidates_from_db, query_latest_environment,
    send_home, open_key_angle, create_sample_candidates,
    get_users_from_database, create_sample_users, is_administrator,
    get_system_info, export_to_csv, open_file, get_dependency_status,
    log_file, init_log_file, log_system_info
)
# Importaciones de interfaces se harán perezosas (lazy) para evitar dependencias mientras migramos
# from admin_interface import AdminInterface
# from instructor_interface import InstructorInterface
# from security_interface import SecurityInterface
# from cleaning_interface import CleaningInterface
# from administrative_interface import AdministrativeInterface
# from schedule_interface import ScheduleInterface
from alert_system import alert_system
from desktop_alerts import desktop_alert_system
from role_validator import role_validator
# from fingerprint_registration_interface import show_fingerprint_registration_interface


class Var:
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value
    def set(self, v):
        self._value = v


class UiDispatcher(QObject):
    call = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Conectar a invocador en el hilo principal
        self.call.connect(self._invoke)

    def _invoke(self, func):
        try:
            func()
        except Exception as e:
            print(f"⚠️ Error en UiDispatcher: {e}")


class FingerprintCanvas(QWidget):
    """Widget de dibujo para icono/animación de huella futurista."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(280, 280)
        self._phase = 0
        self._pulse = 0.0
        self._beam = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def _tick(self):
        self._phase = (self._phase + 1) % 120
        self._pulse = (self._pulse + 0.06) % (6.28318)
        self._beam = (self._beam + 3) % max(1, (self.height() - 120))
        self.update()

    def paintEvent(self, event):
        import math
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        cx = w // 2
        cy = h // 2
        accent = QColor(0, 212, 255)

        # Óvalo principal con brillo
        painter.setPen(QPen(QColor(0, 255, 255, 200), 6))
        painter.setBrush(QColor(20, 26, 40, 220))
        painter.drawEllipse(cx - 90, cy - 120, 180, 240)

        # Líneas de cresta ampliadas y con alpha
        pen_lines = QPen(accent)
        pen_lines.setWidth(3)
        painter.setPen(pen_lines)
        for i in range(-80, 81, 10):
            y = cy + i
            if abs(i) < 100:
                width_line = int(60 * (1 - abs(i) / 100))
                a = 180 - int(140 * abs(i) / 100)
                pen_lines.setColor(QColor(0, 212, 255, max(50, a)))
                painter.setPen(pen_lines)
                painter.drawLine(cx - width_line, y, cx + width_line, y)

        # Barra de escaneo con efecto rayo
        beam_y = cy - 100 + self._beam
        painter.setPen(QPen(QColor(0, 255, 255, 180), 2))
        painter.drawLine(cx - 70, beam_y, cx + 70, beam_y)
        painter.setPen(QPen(QColor(0, 170, 255, 90), 6))
        painter.drawLine(cx - 60, beam_y, cx + 60, beam_y)

        # Arcos laterales dinámicos
        amp = int(6 + 4 * abs(math.sin(self._pulse)))
        painter.setPen(QPen(QColor(0, 200, 255, 180), 3))
        painter.drawArc(cx - 95 - amp, cy - 125 - amp, 190 + 2*amp, 250 + 2*amp, 30 * 16, 120 * 16)
        painter.drawArc(cx - 95 - amp, cy - 125 - amp, 190 + 2*amp, 250 + 2*amp, 210 * 16, 120 * 16)


# ---------------------- UI PRINCIPAL ----------------------
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA")
        try:
            w, h = [int(x) for x in MAIN_WINDOW_SIZE.lower().split('x')]
            self.resize(w, h)
        except Exception:
            self.resize(1200, 800)
        self.setMinimumSize(*MAIN_WINDOW_MIN_SIZE)

        # estado
        self.candidates: List[Tuple[int, str, List[int]]] = []
        self.best: Optional[Tuple[int, str, int]] = None  # (id, name, score)
        self.working = False
        self.worker: Optional[threading.Thread] = None
        self.fingerprint_modal = None  # Referencia al modal de escaneo de huella

        # Inicializar contadores y estadísticas
        self.operations_count = 0
        self.start_time = time.time()

        # Interfaces (lazy): se crearán al abrirse para evitar dependencias de Tk
        self.admin_interface = None
        self.instructor_interface = None
        self.security_interface = None
        self.cleaning_interface = None
        self.administrative_interface = None
        self.schedule_interface = None

        # Construir interfaz
        self._build_ui()

        # Cargar candidatos en arranque
        self._auto_load_candidates()

        # Inicializar archivo de log del sistema
        init_log_file()
        log_system_info()

        # Log de inicio de la aplicación
        print("✅ Interfaz principal futurista cargada correctamente")
        print("🔐 Sistema listo para operaciones de dispensación biométrica")

        # Dispatcher para ejecutar acciones en el hilo de UI desde workers
        self._dispatcher = UiDispatcher(self)

    def _build_ui(self):
        # No usar setup_futuristic_styles porque estamos usando tema claro del HTML
        # styles.setup_futuristic_styles(QApplication.instance())

        # Colores exactos del HTML
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111827"  # gray-900
        TEXT_GRAY_LIGHT = "#6b7280"  # gray-500
        BORDER_COLOR = "#e5e7eb"  # gray-200
        
        # Fondo claro del HTML
        self.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header con logo y título (exacto del HTML)
        header = QWidget(self)
        header.setFixedHeight(60)
        header.setStyleSheet(
            f"background-color: transparent;"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 12, 40, 12)
        header_layout.setSpacing(16)
        
        # Logo/ícono del sistema (escudo.png)
        logo_label = QLabel(header)
        logo_label.setFixedSize(32, 32)
        escudo_pixmap = QPixmap("images/escudo.png")
        if not escudo_pixmap.isNull():
            escudo_pixmap = escudo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(escudo_pixmap)
        else:
            # Fallback si la imagen no se carga
            logo_label.setText("🛡️")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet(
                f"color: {PRIMARY_COLOR}; "
                f"font-size: 24px;"
            )
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)

        # Título del header (exacto del HTML)
        header_title = QLabel("Sistema de Dispensación de Llaves", header)
        header_title.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 18px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        root_layout.addWidget(header)

        # Sección principal con título y subtítulo centrado (exacto del HTML)
        main_section = QWidget(self)
        main_section.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        main_layout = QVBoxLayout(main_section)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(32)
        
        # Título principal centrado (exacto del HTML)
        title_container = QWidget(main_section)
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        title_layout.setAlignment(Qt.AlignCenter)
        
        main_title = QLabel("Sistema de Dispensación Biométrica", title_container)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 36px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
            f"line-height: 1.2;"
        )
        main_title.setWordWrap(False)  # Sin encapsulado, texto fluye naturalmente
        title_layout.addWidget(main_title)
        
        subtitle_main = QLabel("Seleccione su rol para continuar", title_container)
        subtitle_main.setAlignment(Qt.AlignCenter)
        subtitle_main.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 16px; "
            f"font-weight: 400; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        subtitle_main.setWordWrap(False)  # Sin encapsulado, texto fluye naturalmente
        title_layout.addWidget(subtitle_main)
        
        main_layout.addWidget(title_container)
        
        # Grilla de tarjetas de roles (exacto del HTML: grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6)
        cards_container = QWidget(main_section)
        cards_container.setStyleSheet(f"background-color: transparent;")
        cards_layout = QGridLayout(cards_container)
        cards_layout.setSpacing(24)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        # Permitir que las columnas se expandan para que el texto no esté encapsulado
        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)
        cards_layout.setColumnStretch(2, 1)
        
        # Definir los roles con sus íconos y descripciones (exacto del HTML)
        roles = [
            {
                "icon": "images/administrador.jpg",  # Imagen del administrador
                "title": "Administrador",
                "description": "Gestión del sistema",
                "action": lambda: self._handle_biometric_access("admin")
            },
            {
                "icon": "images/instructor .jpg",  # Imagen del instructor (tiene espacio en el nombre)
                "title": "Instructor",
                "description": "Acceso a aulas",
                "action": lambda: self._handle_biometric_access("instructor")
            },
            {
                "icon": "images/seguridad.jpg",  # Imagen de seguridad
                "title": "Seguridad",
                "description": "Control de áreas seguras",
                "action": lambda: self._handle_biometric_access("security")
            },
            {
                "icon": "images/aseo.jpg",  # Imagen de aseo
                "title": "Aseo",
                "description": "Acceso a almacenes",
                "action": lambda: self._handle_biometric_access("cleaning")
            },
            {
                "icon": "images/administrativo.jpg",  # Imagen administrativo
                "title": "Administrativo",
                "description": "Oficinas y archivos",
                "action": lambda: self._handle_biometric_access("administrative")
            },
            {
                "icon": "images/calendario.jpg",  # Imagen de calendario/programación
                "title": "Ver Programación",
                "description": "Revisar horarios",
                "action": self._show_schedule_interface
            }
        ]
        
        # Crear las 6 tarjetas y organizarlas en grilla (3 columnas)
        num_cols = 3
        for i, role in enumerate(roles):
            row = i // num_cols
            col = i % num_cols
            card = styles.create_role_card(
                cards_container,
                role["icon"],
                role["title"],
                role["description"],
                role["action"]
            )
            cards_layout.addWidget(card, row, col)
        
        main_layout.addWidget(cards_container)
        root_layout.addWidget(main_section, 1)

        # Estado y acciones (mantenido del sistema original, pero con fondo claro)
        status_block = QWidget(self)
        status_block.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        status_layout = QVBoxLayout(status_block)
        status_layout.setContentsMargins(40, 20, 40, 20)
        status_layout.setSpacing(12)
        
        self.status_label = QLabel("🟢 Sistema listo y operativo", status_block)
        self.status_label.setAlignment(Qt.AlignHCenter)
        self.status_label.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 14px; "
            f"font-weight: 600;"
        )
        status_layout.addWidget(self.status_label)

        info_label = QLabel("Sistema de Control de Acceso Biométrico - CEFA", status_block)
        info_label.setAlignment(Qt.AlignHCenter)
        info_label.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 12px;"
        )
        status_layout.addWidget(info_label)

        actions = QWidget(status_block)
        actions_layout = QHBoxLayout(actions)
        actions_layout.setSpacing(10)
        actions_layout.setAlignment(Qt.AlignCenter)
        
        reload_btn = QPushButton("🔄 Recargar candidatos", actions)
        reload_btn.setCursor(Qt.PointingHandCursor)
        reload_btn.clicked.connect(self._manual_reload_candidates)
        reload_btn.setStyleSheet(
            f"background-color: transparent; "
            f"color: {PRIMARY_COLOR}; "
            f"border: 1px solid {BORDER_COLOR}; "
            f"border-radius: 8px; "
            f"padding: 8px 16px; "
            f"font-size: 12px;"
        )
        
        db_btn = QPushButton("⚙️ Configurar BD", actions)
        db_btn.setCursor(Qt.PointingHandCursor)
        db_btn.clicked.connect(self._show_database_config)
        db_btn.setStyleSheet(
            f"background-color: {PRIMARY_COLOR}; "
            f"color: white; "
            f"border: none; "
            f"border-radius: 8px; "
            f"padding: 8px 16px; "
            f"font-size: 12px; "
            f"font-weight: 600;"
        )
        
        actions_layout.addWidget(reload_btn)
        actions_layout.addWidget(db_btn)
        status_layout.addWidget(actions)

        root_layout.addWidget(status_block)

        # Variables para el lector biométrico
        self.var_fp_port = Var(FINGERPRINT_PORT_DEFAULT)
        self.var_fp_baud = Var(FINGERPRINT_BAUD_DEFAULT)
        self.var_threshold = Var(DEFAULT_THRESHOLD)
        self.var_topn = Var(DEFAULT_TOPN)
        self.var_dwell = Var(DEFAULT_DWELL)

        # Variable para rastrear la interfaz solicitada
        self.requested_interface = None

    def _set_status(self, text: str):
        try:
            self.status_label.setText(text)
        except Exception:
            pass

    def _handle_biometric_access(self, interface_type):
        self.requested_interface = interface_type
        # Acceso directo temporal sin verificación por huella
        self._open_requested_interface()

    def _open_requested_interface(self):
        if not self.requested_interface:
            return
        print(f"🚪 Abriendo interfaz solicitada: {self.requested_interface}")

        try:
            if self.requested_interface == "admin":
                if not self.admin_interface:
                    from admin_interface import AdminInterface  # PySide6 version
                    self.admin_interface = AdminInterface(self)
                self._close_fingerprint_scan_window()
                QTimer.singleShot(100, self.admin_interface.show_admin_interface)
            elif self.requested_interface == "instructor":
                if not self.instructor_interface:
                    from instructor_interface import InstructorInterface
                    # Pasar el usuario autenticado (pid, name) para saludar y evitar segundo escaneo
                    authed_user = None
                    try:
                        if self.best:
                            pid, name, score = self.best
                            authed_user = {'id': pid, 'name': name}
                        elif self.candidates:
                            # Fallback: primer candidato si best aún no está seteado
                            pid, name, _ = self.candidates[0]
                            authed_user = {'id': pid, 'name': name}
                    except Exception:
                        pass
                    self.instructor_interface = InstructorInterface(self, authed_user)
                self._close_fingerprint_scan_window()
                QTimer.singleShot(100, self.instructor_interface.show_instructor_interface)
            elif self.requested_interface == "security":
                if not self.security_interface:
                    from security_interface import SecurityInterface
                    authed_user = None
                    try:
                        if self.candidates and self.best:
                            pid, name, score = self.best
                            authed_user = {'id': pid, 'name': name}
                    except Exception:
                        pass
                    self.security_interface = SecurityInterface(self, authed_user)
                else:
                    try:
                        if self.best:
                            pid, name, score = self.best
                            self.security_interface.set_authenticated_user({'id': pid, 'name': name})
                    except Exception:
                        pass
                self._close_fingerprint_scan_window()
                QTimer.singleShot(100, self.security_interface.show_security_interface)
            elif self.requested_interface == "cleaning":
                if not self.cleaning_interface:
                    from cleaning_interface import CleaningInterface
                    self.cleaning_interface = CleaningInterface(self)
                self._close_fingerprint_scan_window()
                QTimer.singleShot(100, self.cleaning_interface.show_cleaning_interface)
            elif self.requested_interface == "administrative":
                if not self.administrative_interface:
                    from administrative_interface import AdministrativeInterface
                    self.administrative_interface = AdministrativeInterface(self)
                self._close_fingerprint_scan_window()
                QTimer.singleShot(100, self.administrative_interface.show_administrative_interface)
        finally:
            self.requested_interface = None

    def _close_fingerprint_scan_window(self):
        try:
            print("🚪 Cerrando modal de escaneo de huella...")
            if hasattr(self, 'fingerprint_modal') and self.fingerprint_modal:
                self.fingerprint_modal.close()
                self.fingerprint_modal = None
            log_file("🚪 Modal de escaneo de huella cerrado después de login exitoso")
        except Exception as e:
            print(f"⚠️ Error cerrando modal de escaneo: {e}")
            log_file(f"⚠️ Error cerrando modal de escaneo: {e}")

    def _restore_main_window(self):
        try:
            print("🔄 Restaurando ventana principal...")
            self.show()
            self.raise_()
            log_file("🔄 Ventana principal restaurada")
        except Exception as e:
            print(f"⚠️ Error restaurando ventana principal: {e}")
            log_file(f"⚠️ Error restaurando ventana principal: {e}")

    def _cancel_fingerprint_scan(self):
        try:
            print("❌ Cancelando escaneo de huella...")
            if self.working and self.worker:
                self.working = False
            if self.fingerprint_modal:
                self.fingerprint_modal.close()
                self.fingerprint_modal = None
            self.requested_interface = None
            log_file("❌ Escaneo de huella cancelado por el usuario")
        except Exception as e:
            print(f"⚠️ Error cancelando escaneo: {e}")
            log_file(f"⚠️ Error cancelando escaneo: {e}")

    def _auto_load_candidates(self):
        try:
            print("🔄 Conectando a la base de datos sistema_llaves_v2...")
            try:
                mysql, err = _import_mysql()
                if not mysql:
                    raise Exception(f"MySQL no disponible: {err}")
                connection = mysql.connect(**DB_CONFIG)
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES LIKE 'personal'")
                if not cursor.fetchone():
                    raise Exception("La tabla 'personal' no existe en la base de datos")
                cursor.execute("SELECT COUNT(*) FROM personal WHERE activo = 1")
                total_people = cursor.fetchone()[0]
                print(f"📊 Total de personas en la base de datos: {total_people}")
                cursor.execute("SELECT COUNT(*) FROM personal WHERE huella_digital IS NOT NULL AND activo = 1")
                biometric_people = cursor.fetchone()[0]
                print(f"🔐 Personas con huella digital: {biometric_people}")
                self.candidates = load_candidates_from_db()
                if self.candidates:
                    print(f"✅ {len(self.candidates)} candidatos cargados desde sistema_llaves_v2")
                    self._set_status(f"🟢 {len(self.candidates)} CANDIDATOS CARGADOS DESDE SISTEMA_LLAVES_V2 - SISTEMA LISTO")
                    for i, (pid, name, bio) in enumerate(self.candidates[:3]):
                        print(f"   {i+1}. ID: {pid}, Nombre: {name}, Bio: {len(bio) if bio else 0} bytes")
                else:
                    print("⚠️ No se encontraron candidatos con huella digital en sistema_llaves_v2")
                    self._set_status("🟡 SIN CANDIDATOS BIOMÉTRICOS EN SISTEMA_LLAVES_V2")
                cursor.close()
                connection.close()
            except Exception as db_error:
                print(f"❌ Error conectando a sistema_llaves_v2: {db_error}")
                self._set_status("🔴 ERROR CONECTANDO A SISTEMA_LLAVES_V2")
                print("🔄 Creando candidatos de ejemplo para desarrollo...")
                self._create_sample_candidates()
        except Exception as e:
            print(f"❌ Error crítico cargando candidatos: {e}")
            self._set_status("🔴 ERROR CRÍTICO CARGANDO CANDIDATOS")
            self._create_sample_candidates()

    def _create_sample_candidates(self):
        try:
            print("🔄 Creando candidatos de ejemplo...")
            self.candidates = create_sample_candidates()
            print(f"✅ {len(self.candidates)} candidatos de ejemplo creados")
            self._set_status("🟡 CANDIDATOS DE EJEMPLO CARGADOS - MODO DESARROLLO")
        except Exception as e:
            print(f"❌ Error creando candidatos de ejemplo: {e}")
            self._set_status("🔴 ERROR CRÍTICO - SIN CANDIDATOS")
            self.candidates = []

    def _manual_reload_candidates(self):
        try:
            self._auto_load_candidates()
            QMessageBox.information(self, "✅ ÉXITO", "Candidatos recargados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "❌ ERROR", f"Error recargando candidatos:\n\n{e}")

    def _show_database_config(self):
        QMessageBox.information(self, "⚙️ CONFIGURACIÓN BD",
                                (
                                    f"Configuración actual de la base de datos:\n\n"
                                    f"Host: {DB_CONFIG['host']}\n"
                                    f"Usuario: {DB_CONFIG['user']}\n"
                                    f"Base de datos: {DB_CONFIG['database']}\n\n"
                                    "Para cambiar la configuración, edite el archivo config.py"
                                ))

    # ============ INTERFACES DE USUARIOS ============
    def _show_schedule_interface(self):
        try:
            if not self.schedule_interface:
                from schedule_interface import ScheduleInterface
                self.schedule_interface = ScheduleInterface(self)
            self.schedule_interface.show_schedule_interface()
        except Exception as e:
            QMessageBox.warning(self, "⚠️", f"Error abriendo programación: {e}")

    # ============ FUNCIONALIDADES DEL SISTEMA ORIGINAL ============
    def _show_fingerprint_modal(self):
        self.fingerprint_modal = styles.create_modal_window(self, "Escaneo de Huella", MODAL_SIZE)
        modal = self.fingerprint_modal

        layout = QVBoxLayout(modal)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)
        try:
            modal.setStyleSheet("QDialog { background-color: #0b1220; border: 1px solid #08c6ff; border-radius: 10px; }")
        except Exception:
            pass

        title_label = styles.create_title_label(modal, "Escanea huella")
        layout.addWidget(title_label)

        fp_widget = FingerprintCanvas(modal)
        layout.addWidget(fp_widget, 1, alignment=Qt.AlignHCenter)
        hint = styles.create_subtitle_label(modal, "Coloque su dedo en el lector y manténgalo hasta completar el escaneo")
        hint.setAlignment(Qt.AlignHCenter)
        layout.addWidget(hint)

        buttons = QWidget(modal)
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.setSpacing(10)
        scan_btn = styles.create_accent_button(buttons, "🔍 ESCANEAR HUELLA", self._start_fingerprint_scan)
        cancel_btn = styles.create_danger_button(buttons, "❌ CANCELAR", self._cancel_fingerprint_scan)
        buttons_layout.addWidget(scan_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addWidget(buttons)

        modal.show()

    def _start_fingerprint_scan(self):
        if not hasattr(self, 'candidates') or not self.candidates:
            QMessageBox.critical(self, "❌ ERROR", "No hay candidatos cargados en el sistema.\n\nPor favor, recargue los candidatos desde la base de datos.")
            return
        try:
            fp_mod, err = _import_pyfingerprint()
            if not fp_mod:
                QMessageBox.critical(self, "❌ ERROR", f"Lector biométrico no disponible: {err}\n\nInstale pyfingerprint para usar esta funcionalidad.")
                return
        except Exception as e:
            QMessageBox.critical(self, "❌ ERROR", f"Error verificando lector biométrico: {e}")
            return
        self._start_real_fingerprint_scan()

    def _start_real_fingerprint_scan(self):
        if not self.candidates:
            QMessageBox.critical(self, "❌ ERROR", "No hay candidatos cargados desde la base de datos SICEFA.\n\nVerifique la conexión a la base de datos.")
            return

        self._show_scan_instructions_dialog()

        self.working = True
        self._set_status("🔍 ESCANEANDO HUELLA DIGITAL - Coloque su dedo en el sensor físico...")
        print(f"🔐 Configuración del lector biométrico:")
        print(f"   Puerto: {self.var_fp_port.get()}")
        print(f"   Baud Rate: {self.var_fp_baud.get()}")
        print(f"   Candidatos disponibles: {len(self.candidates)}")

        self.worker = threading.Thread(target=self._real_fingerprint_worker, daemon=True)
        self.worker.start()

    def _show_scan_instructions_dialog(self):
        try:
            dlg = styles.create_modal_window(self, "🔍 ESCANEO REAL INICIADO", "640x420")
            lay = QVBoxLayout(dlg)
            lay.setContentsMargins(20, 16, 20, 16)
            lay.setSpacing(12)

            title = styles.create_title_label(dlg, "Escaneo de huella - Instrucciones")
            lay.addWidget(title)

            # Panel contenido
            panel = styles.create_main_frame(dlg)
            panel_lay = QVBoxLayout(panel)
            panel_lay.setContentsMargins(16, 16, 16, 16)
            panel_lay.setSpacing(10)

            lines = [
                "1️⃣ Coloque su dedo en el lector biométrico físico",
                "2️⃣ Mantenga el dedo en el sensor hasta que se complete la captura",
                "3️⃣ El sistema validará su huella contra la base de datos SICEFA",
                "4️⃣ Si es administrador, tendrá acceso completo",
            ]
            for t in lines:
                lbl = styles.create_info_label(panel, t)
                panel_lay.addWidget(lbl)

            warn = styles.create_subtitle_label(dlg, f"⚠️ IMPORTANTE: Asegúrese de que el lector esté conectado al puerto {self.var_fp_port.get()}")
            warn.setAlignment(Qt.AlignHCenter)
            panel_lay.addWidget(warn)

            lay.addWidget(panel)

            # Botón de continuar
            btn_row = QWidget(dlg)
            btn_lay = QHBoxLayout(btn_row)
            btn_lay.setContentsMargins(0, 0, 0, 0)
            btn_lay.addStretch(1)
            ok_btn = styles.create_accent_button(btn_row, "✅ ENTENDIDO", dlg.accept)
            btn_lay.addWidget(ok_btn)
            lay.addWidget(btn_row)

            dlg.exec()
        except Exception:
            # Fallback a QMessageBox si algo falla
            QMessageBox.information(self, "🔍 ESCANEO REAL INICIADO",
                                    (
                                        "INSTRUCCIONES PARA ESCANEO DE HUELLA:\n\n"
                                        "1️⃣ Coloque su dedo en el lector biométrico físico\n"
                                        "2️⃣ Mantenga el dedo en el sensor hasta que se complete la captura\n"
                                        "3️⃣ El sistema validará su huella contra la base de datos SICEFA\n"
                                        "4️⃣ Si es administrador, tendrá acceso completo\n\n"
                                        f"⚠️ IMPORTANTE: Asegúrese de que el lector esté conectado al puerto {self.var_fp_port.get()}"
                                    ))

    def _real_fingerprint_worker(self):
        try:
            print("🚀 INICIANDO ESCANEO REAL DE HUELLA...")
            fp_mod, err = _import_pyfingerprint()
            if not fp_mod:
                self._end_error(f"Lector biométrico no disponible: {err}")
                return
            PyFingerprint, F1, F2 = fp_mod

            print(f"🔌 Conectando al lector biométrico en puerto {self.var_fp_port.get()}...")
            self._ui(lambda: self._set_status("🔌 CONECTANDO AL LECTOR BIOMÉTRICO..."))

            try:
                sensor = PyFingerprint(self.var_fp_port.get().strip(), int(self.var_fp_baud.get()), 0xFFFFFFFF, 0x00000000)
                print("✅ Lector biométrico conectado, verificando contraseña...")
                if not sensor.verifyPassword():
                    self._end_error("Contraseña del sensor incorrecta")
                    return
                print("✅ Contraseña del sensor verificada correctamente")
                self._ui(lambda: self._set_status("✅ SENSOR CONECTADO - Coloque su dedo en el lector..."))
                self._ui(lambda: log_file("✅ Sensor biométrico conectado y verificado"))
            except Exception as e:
                error_msg = f"Error conectando al lector biométrico: {e}"
                print(f"❌ {error_msg}")
                self._end_error(f"Error conectando al lector biométrico: {e}")
                return

            print("📱 Iniciando captura de huella digital...")
            self._ui(lambda: self._set_status("📱 CAPTURANDO HUELLA - Mantenga el dedo en el sensor..."))
            self._ui(lambda: log_file("📱 Iniciando captura de huella digital..."))

            t0 = time.time()
            timeout_s = DEFAULT_TIMEOUT_S
            ok = False
            print("⏳ Esperando que coloque el dedo en el sensor...")
            while True:
                try:
                    if sensor.readImage():
                        ok = True
                        print("✅ Imagen de huella capturada exitosamente")
                        break
                except Exception as e:
                    print(f"⚠️ Error leyendo imagen: {e}")
                    self._end_error(f"Lectura fallida del sensor: {e}")
                    return
                if time.time() - t0 > timeout_s:
                    print("⏰ Tiempo agotado esperando huella")
                    break
                time.sleep(0.1)

            if not ok:
                self._end_info("Tiempo agotado esperando huella. Intente nuevamente.")
                return

            print("🔄 Convirtiendo imagen capturada...")
            try:
                sensor.convertImage(F1)
                print("✅ Imagen convertida correctamente")
                self._ui(lambda: log_file("✅ Huella capturada y convertida correctamente"))
            except Exception as e:
                self._end_error(f"No se pudo convertir la imagen capturada: {e}")
                return

            print(f"🔍 Comparando huella con {len(self.candidates)} candidatos de SICEFA...")
            self._ui(lambda: self._set_status("🔍 COMPARANDO HUELLA CON BASE DE DATOS SICEFA..."))
            self._ui(lambda: log_file("🔍 Comparando huella capturada con candidatos de SICEFA..."))

            try:
                threshold = int(self.var_threshold.get())
                topn = max(1, int(self.var_topn.get()))
                scored: List[Tuple[int, str, int]] = []
                print(f"🎯 Umbral de coincidencia: {threshold}")
                print(f"🔝 Top-N resultados: {topn}")
                for i, (pid, name, tpl) in enumerate(self.candidates):
                    try:
                        print(f"   Comparando con candidato {i+1}/{len(self.candidates)}: {name} (ID: {pid})")
                        sensor.uploadCharacteristics(F2, tpl)
                        score = sensor.compareCharacteristics()
                        scored.append((pid, name, score))
                        print(f"     Puntuación: {score}")
                    except Exception as ex:
                        print(f"     ⚠️ Error comparando: {ex}")
                        self._ui(lambda: log_file(f"Plantilla corrupta para {name or pid}: {ex}"))
                scored.sort(key=lambda x: x[2], reverse=True)
                best = scored[0] if scored else None
                print(f"🏆 Mejor puntuación: {best[2] if best else 'N/A'}")
            except Exception as e:
                self._end_error(f"Error al comparar huella: {e}")
                return

            if best and best[2] >= threshold:
                pid, name, score = best
                # Guardar mejor resultado para pasar a la interfaz correspondiente
                try:
                    self.best = (pid, name, score)
                except Exception:
                    pass
                print(f"🎉 IDENTIFICACIÓN EXITOSA: {name} (ID: {pid}) con puntuación {score}")
                self._ui(lambda: log_file(f"✅ Identificación exitosa: {name} (ID: {pid}) con puntuación {score}"))
                if self.requested_interface:
                    has_access, user_name, user_role = role_validator.validate_role_access(pid, self.requested_interface)
                    if has_access:
                        print(f"🔐 Usuario {name} tiene acceso al rol {self.requested_interface}")
                        self._ui(lambda: self._set_status(f"🔐 {user_role.upper()} IDENTIFICADO - Acceso concedido"))
                        self._ui(lambda: log_file(f"🔐 Acceso de {user_role} concedido"))
                        self._ui(lambda: desktop_alert_system.show_access_granted_alert(self.requested_interface, user_name))
                        # Programar apertura de interfaz en el hilo de UI
                        self._ui(lambda: QTimer.singleShot(2000, self._open_requested_interface))
                    else:
                        print(f"❌ Usuario {name} no tiene acceso al rol {self.requested_interface}")
                        self._ui(lambda: self._set_status(f"❌ ACCESO DENEGADO - Rol incorrecto"))
                        self._ui(lambda: log_file(f"❌ Acceso denegado: {name} no es {self.requested_interface}"))
                        self._ui(lambda: desktop_alert_system.show_access_denied_alert(self.requested_interface, user_name))
                else:
                    if is_administrator(pid, name):
                        print("🔐 Usuario identificado como ADMINISTRADOR")
                        self._ui(lambda: self._set_status("🔐 ADMINISTRADOR IDENTIFICADO - Acceso concedido"))
                        self._ui(lambda: log_file("🔐 Acceso de administrador concedido"))
                        self._ui(self._close_fingerprint_scan_window)
                        self._ui(lambda: QTimer.singleShot(100, lambda: self._open_requested_interface()))
                    else:
                        print("👤 Usuario identificado con acceso limitado")
                        self._ui(lambda: self._set_status("👤 USUARIO IDENTIFICADO - Acceso limitado"))
                        self._ui(lambda: log_file(f"👤 Usuario {name} identificado - Acceso limitado"))
                        self._ui(self._close_fingerprint_scan_window)
                        self._ui(lambda: QTimer.singleShot(100, lambda: self._show_user_access_interface(name, pid)))
            else:
                print(f"❌ Sin coincidencias válidas. Mejor puntuación: {best[2] if best else 'N/A'} (umbral: {threshold})")
                self._ui(lambda: self._set_status("❌ HUELLA NO RECONOCIDA"))
                self._ui(lambda: log_file("❌ Huella no reconocida en el sistema"))
                self._ui(lambda: desktop_alert_system.show_fingerprint_not_found_alert())
                return
        except Exception as e:
            print(f"❌ Error crítico en el escaneo de huella: {e}")
            self._end_error(f"Error crítico en el escaneo de huella: {e}")
        finally:
            self.working = False
            print("🏁 Proceso de escaneo finalizado")

    def _ui(self, func):
        """Ejecuta una función en el hilo de UI de Qt desde cualquier hilo."""
        try:
            self._dispatcher.call.emit(func)
        except Exception as e:
            print(f"⚠️ Error en _ui: {e}")

    def _show_user_access_interface(self, name: str, pid: int):
        QMessageBox.information(self, "👤 ACCESO DE USUARIO",
                                f"Usuario identificado: {name}\nID: {pid}\n\nAcceso limitado concedido.\nContacte al administrador para permisos adicionales.")

    def cleanup(self):
        try:
            alert_system.cleanup()
            desktop_alert_system.cleanup()
        except Exception as e:
            print(f"⚠️ Error en limpieza: {e}")

    def on_closing(self):
        try:
            self.cleanup()
            self.close()
        except Exception as e:
            print(f"⚠️ Error al cerrar: {e}")
            self.close()

    def _end_error(self, msg: str):
        error_msg = f"❌ ERROR EN ESCANEO DE HUELLA: {msg}"
        QTimer.singleShot(0, lambda: log_file(error_msg))
        QTimer.singleShot(0, lambda: self._set_status("🔴 ERROR EN ESCANEO DE HUELLA"))
        QTimer.singleShot(0, lambda: QMessageBox.critical(self, "🚨 ERROR", f"Error en el escaneo de huella:\n\n{msg}"))
        self.working = False

    def _end_info(self, msg: str):
        info_msg = f"ℹ️ INFORMACIÓN: {msg}"
        QTimer.singleShot(0, lambda: log_file(info_msg))
        QTimer.singleShot(0, lambda: self._set_status("ℹ️ INFORMACIÓN PROCESADA"))
        QTimer.singleShot(0, lambda: QMessageBox.information(self, "ℹ️ INFORMACIÓN", f"Información del sistema:\n\n{msg}"))
        self.working = False


# ============ FUNCIÓN PRINCIPAL ============
def main():
    try:
        qt_app = QApplication.instance() or QApplication([])
        styles.setup_futuristic_styles(qt_app)
        win = App()
        win.show()
        qt_app.aboutToQuit.connect(win.on_closing)
        qt_app.exec()
    except Exception as e:
        print(f"❌ ERROR CRÍTICO en la aplicación principal: {e}")
        log_file(f"❌ ERROR CRÍTICO en la aplicación principal: {e}")
        try:
            tmp_app = QApplication.instance() or QApplication([])
            QMessageBox.critical(None, "🚨 ERROR CRÍTICO", f"Error crítico en la aplicación:\n\n{e}\n\nLa aplicación se cerrará.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
