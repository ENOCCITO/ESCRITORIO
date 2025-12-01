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
from src.utils import styles
from src.config.config import *
from src.utils.utils import (
    _import_mysql, _import_pyfingerprint, _import_serial,
    db_connect, load_candidates_from_db, query_latest_environment,
    send_home, open_key_angle, create_sample_candidates,
    get_users_from_database, create_sample_users, is_administrator,
    get_system_info, export_to_csv, open_file, get_dependency_status,
    log_file, init_log_file, log_system_info
)
# Importaciones de interfaces se harán perezosas (lazy) para evitar dependencias mientras migramos
# from src.interfaces.admin_interface import AdminInterface
# from src.interfaces.instructor_interface import InstructorInterface
# from src.interfaces.security_interface import SecurityInterface
# from src.interfaces.cleaning_interface import CleaningInterface
# from src.interfaces.administrative_interface import AdministrativeInterface
# from src.interfaces.schedule_interface import ScheduleInterface
from src.core.alert_system import alert_system
from src.core.desktop_alerts import desktop_alert_system
from src.core.role_validator import role_validator
# from src.interfaces.fingerprint_registration_interface import show_fingerprint_registration_interface


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
        self.schedule_button = None

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
        """Construye la interfaz principal simplificada para adultos mayores"""
        # Colores simples y claros
        PRIMARY_COLOR = "#2563eb"  # Azul más visible
        BG_COLOR = "#ffffff"  # Fondo blanco
        TEXT_COLOR = "#1f2937"  # Texto oscuro y claro
        ACCENT_COLOR = "#10b981"  # Verde para estados positivos
        
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header simplificado (OCULTO para interfaces más limpias)
        # header = QWidget(self)
        # header.setFixedHeight(80)
        # header.setStyleSheet(
        #     f"background-color: transparent;"
        # )
        # header_layout = QHBoxLayout(header)
        # header_layout.setContentsMargins(40, 20, 40, 20)
        # header_layout.setSpacing(20)
        # 
        # # Título grande y claro
        # header_title = QLabel("Sistema de Llaves CEFA", header)
        # header_title.setStyleSheet(
        #     f"color: {TEXT_COLOR}; "
        #     f"font-size: 28px; "
        #     f"font-weight: 700; "
        #     f"font-family: 'Segoe UI', Arial, sans-serif;"
        # )
        # header_layout.addWidget(header_title)
        # header_layout.addStretch()
        # 
        # root_layout.addWidget(header)

        # Contenedor principal centrado
        main_container = QWidget(self)
        main_container.setStyleSheet(f"background-color: {BG_COLOR};")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Contenedor central con la huella
        center_widget = QWidget(main_container)
        center_widget.setMaximumWidth(600)
        center_layout = QVBoxLayout(center_widget)
        center_layout.setSpacing(40)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Título principal - MUY GRANDE Y CLARO
        title = QLabel("¡Bienvenido!", center_widget)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            f"color: {TEXT_COLOR}; "
            f"font-size: 48px; "
            f"font-weight: 700; "
            f"font-family: 'Segoe UI', Arial, sans-serif;"
        )
        center_layout.addWidget(title)
        
        # Imagen de huella - Usar la imagen real proporcionada
        fingerprint_label = QLabel(center_widget)
        fingerprint_label.setAlignment(Qt.AlignCenter)
        
        # Cargar la imagen de huella
        fingerprint_pixmap = QPixmap("assets/images/Captura de pantalla 2025-11-30 135242.png")
        if not fingerprint_pixmap.isNull():
            # Escalar la imagen manteniendo la proporción (más pequeña para ver mejor los detalles)
            fingerprint_pixmap = fingerprint_pixmap.scaled(
                250, 250,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            fingerprint_label.setPixmap(fingerprint_pixmap)
        else:
            # Fallback si la imagen no carga
            fingerprint_label.setText("👆")
            fingerprint_label.setStyleSheet(
                f"color: {PRIMARY_COLOR}; "
                f"font-size: 140px;"
            )
        
        center_layout.addWidget(fingerprint_label, 0, Qt.AlignCenter)
        
        # Instrucción MUY CLARA
        instruction = QLabel("Coloque su dedo\nen el lector de huellas", center_widget)
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setStyleSheet(
            f"color: {TEXT_COLOR}; "
            f"font-size: 32px; "
            f"font-weight: 600; "
            f"font-family: 'Segoe UI', Arial, sans-serif; "
            f"line-height: 1.4;"
        )
        center_layout.addWidget(instruction)
        
        # ELIMINADO - Estado del sistema (texto verde que se quería quitar)
        # Crear una etiqueta invisible para que no se rompa el código que la referencia
        self.status_label = QLabel("", center_widget)
        self.status_label.setVisible(False)
        
        main_layout.addWidget(center_widget)
        root_layout.addWidget(main_container, 1)
        
        # Agregar botón de programación en la esquina inferior derecha
        self._create_schedule_button()

        # Variables para el lector biométrico
        self.var_fp_port = Var(FINGERPRINT_PORT_DEFAULT)
        self.var_fp_baud = Var(FINGERPRINT_BAUD_DEFAULT)
        self.var_threshold = Var(DEFAULT_THRESHOLD)
        self.var_topn = Var(DEFAULT_TOPN)
        self.var_dwell = Var(DEFAULT_DWELL)

        # Variable para rastrear la interfaz solicitada
        self.requested_interface = None

        # Inicializar interfaz de programación
        self.schedule_interface = None

    def _create_schedule_button(self):
        """Crea el botón de programación en la esquina"""
        if self.schedule_button is None:
            self.schedule_button = QPushButton("📅", self)
            self.schedule_button.setCursor(Qt.PointingHandCursor)
            self.schedule_button.setFixedSize(70, 70)  # Aumentado de 60x60 a 70x70
            self.schedule_button.setStyleSheet(
                "QPushButton {"
                "  background-color: #6b7280; "
                "  color: white; "
                "  border: none; "
                "  border-radius: 35px; "  # Aumentado de 30px a 35px para mantener la forma circular
                "  font-size: 28px; "  # Aumentado de 24px a 28px
                "  font-weight: 600; "
                "}"
                "QPushButton:hover {"
                "  background-color: #4b5563;"
                "}"
                "QPushButton:pressed {"
                "  background-color: #374151;"
                "}"
            )
            self.schedule_button.clicked.connect(self._show_schedule_interface)
        
        # Posicionar el botón en la esquina inferior derecha
        self._position_schedule_button()

    def _position_schedule_button(self):
        """Posiciona el botón de programación en la esquina inferior derecha"""
        if self.schedule_button:
            self.schedule_button.move(self.width() - 80, self.height() - 80)  # Ajustado de 70 a 80 para el nuevo tamaño

    def resizeEvent(self, event):
        """Maneja el evento de redimensionamiento para reposicionar el botón"""
        super().resizeEvent(event)
        self._position_schedule_button()

    def keyPressEvent(self, event):
        """Maneja eventos de teclado"""
        if event.key() == Qt.Key_Escape:
            print("🚪 Tecla ESC presionada - Cerrando aplicación...")
            self.force_exit()
        else:
            super().keyPressEvent(event)

    def _set_status(self, text: str):
        """Actualiza el mensaje de estado en la pantalla principal"""
        try:
            self.status_label.setText(text)
        except Exception:
            pass

    def _open_requested_interface(self):
        """Abre la interfaz solicitada y oculta la ventana principal"""
        if not self.requested_interface:
            return
        print(f"🚪 Abriendo interfaz solicitada: {self.requested_interface}")

        try:
            if self.requested_interface == "admin":
                if not self.admin_interface:
                    from src.interfaces.admin_interface import AdminInterface  # PySide6 version
                    self.admin_interface = AdminInterface(self)
                self._close_fingerprint_scan_window()
                # NO ocultar la ventana principal, solo mostrar la interfaz secundaria
                QTimer.singleShot(100, self.admin_interface.show_admin_interface)
            elif self.requested_interface == "instructor":
                if not self.instructor_interface:
                    from src.interfaces.instructor_interface import InstructorInterface
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
                # NO ocultar la ventana principal, solo mostrar la interfaz secundaria
                QTimer.singleShot(100, self.instructor_interface.show_instructor_interface)
            elif self.requested_interface == "security":
                if not self.security_interface:
                    from src.interfaces.security_interface import SecurityInterface
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
                # NO ocultar la ventana principal, solo mostrar la interfaz secundaria
                QTimer.singleShot(100, self.security_interface.show_security_interface)
            elif self.requested_interface == "cleaning":
                if not self.cleaning_interface:
                    from src.interfaces.cleaning_interface import CleaningInterface
                    self.cleaning_interface = CleaningInterface(self)
                self._close_fingerprint_scan_window()
                # NO ocultar la ventana principal, solo mostrar la interfaz secundaria
                QTimer.singleShot(100, self.cleaning_interface.show_cleaning_interface)
            elif self.requested_interface == "administrative":
                if not self.administrative_interface:
                    from src.interfaces.administrative_interface import AdministrativeInterface
                    self.administrative_interface = AdministrativeInterface(self)
                self._close_fingerprint_scan_window()
                # NO ocultar la ventana principal, solo mostrar la interfaz secundaria
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

    def show_main_window(self):
        """Método público para mostrar la ventana principal nuevamente"""
        """Las interfaces hijas pueden llamar a este método cuando se cierren"""
        try:
            print("🔄 Restaurando ventana principal...")
            
            # Forzar restauración del estado normal primero
            self.setWindowState(Qt.WindowNoState)
            
            # Mostrar la ventana
            self.show()
            self.raise_()
            self.activateWindow()
            
            # Forzar pantalla completa con un retraso mayor
            QTimer.singleShot(100, self._apply_fullscreen)
            
            print("✅ Ventana principal en pantalla completa")
            log_file("🔄 Ventana principal restaurada en pantalla completa")
        except Exception as e:
            print(f"⚠️ Error restaurando ventana principal: {e}")
            log_file(f"⚠️ Error restaurando ventana principal: {e}")
    
    def _apply_fullscreen(self):
        """Aplicar pantalla completa con un pequeño retraso para asegurar la restauración"""
        try:
            # Forzar restauración del estado normal primero
            self.setWindowState(Qt.WindowNoState)
            # Aplicar pantalla completa
            self.showFullScreen()
        except Exception as e:
            print(f"⚠️ Error aplicando pantalla completa: {e}")

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
        """Muestra la interfaz de programación"""
        try:
            print("📅 Abriendo interfaz de programación...")
            
            # Crear la interfaz de programación si no existe
            if self.schedule_interface is None:
                from src.interfaces.schedule_interface import ScheduleInterface
                self.schedule_interface = ScheduleInterface(self)
            
            # Mostrar la interfaz de programación
            self.schedule_interface.show_schedule_interface()
            
            print("✅ Interfaz de programación mostrada")
        except Exception as e:
            print(f"❌ Error abriendo interfaz de programación: {e}")
            QMessageBox.critical(self, "Error", f"Error abriendo interfaz de programación:\n{e}")

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
        """Limpia recursos y detiene hilos antes de cerrar"""
        try:
            print("🧹 Iniciando limpieza de recursos...")
            
            # Detener el worker thread si está corriendo
            if self.working and self.worker is not None:
                print("⏸️ Deteniendo worker thread...")
                self.working = False
                # Esperar un poco para que el thread termine
                if self.worker.is_alive():
                    self.worker.join(timeout=2.0)
                    if self.worker.is_alive():
                        print("⚠️ Worker thread no terminó a tiempo")
            
            # Cerrar modal de huella si está abierto
            if self.fingerprint_modal is not None:
                try:
                    self.fingerprint_modal.close()
                except Exception:
                    pass
            
            # Limpiar sistemas de alertas
            try:
                alert_system.cleanup()
                desktop_alert_system.cleanup()
            except Exception as e:
                print(f"⚠️ Error limpiando alertas: {e}")
            
            print("✅ Limpieza completada")
        except Exception as e:
            print(f"⚠️ Error en limpieza: {e}")
    
    def force_exit(self):
        """Forzar salida completa de la aplicación"""
        try:
            print("🛑 Forzando salida de la aplicación...")
            # Limpiar recursos
            self.cleanup()
            
            # Forzar cierre de la aplicación Qt
            app = QApplication.instance()
            if app:
                app.quit()
            
            # Forzar salida del sistema
            import sys
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Error forzando salida: {e}")
            import sys
            sys.exit(1)

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana (cuando presionas X)"""
        try:
            print("🚪 Cerrando aplicación...")
            self.force_exit()
            event.accept()  # Aceptar el cierre
        except Exception as e:
            print(f"⚠️ Error al cerrar: {e}")
            event.accept()
            import sys
            sys.exit(1)

    def on_closing(self):
        """Método llamado cuando la aplicación está por cerrarse"""
        try:
            self.force_exit()
        except Exception as e:
            print(f"⚠️ Error al cerrar: {e}")

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
        
        # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
        win.showFullScreen()
        
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
