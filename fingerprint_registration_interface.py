#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fingerprint_registration_interface.py
- Interfaz de registro de huellas digitales (PySide6)
- Filtrado por tipo de personal y diseño optimizado para pantallas pequeñas
"""

from typing import List, Dict, Any, Optional
import threading
import time
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer

from db_utils import get_personal_types, db_connect
from desktop_alerts import desktop_alert_system
from biometric_scanner import biometric_scanner
from utils import log_file


class FingerprintRegistrationInterface:
    """Interfaz de registro de huellas digitales responsive (Qt)."""

    def __init__(self, parent=None):
        self.parent = parent
        self.window: Optional[QDialog] = None
        self.personal_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.current_personal_type: str = "TODOS"
        self.search_text: str = ""
        self.scanning: bool = False

        # Configuración para pantalla TFT 7 pulgadas
        self.screen_width = 800
        self.screen_height = 480
        self.font_size_small = 10
        self.font_size_medium = 12
        self.font_size_large = 16
        self.font_size_xlarge = 20

        # Widgets que se llenan en _create_interface
        self.type_combo: Optional[QComboBox] = None
        self.search_entry: Optional[QLineEdit] = None
        self.status_label: Optional[QLabel] = None
        self.count_label: Optional[QLabel] = None
        self.scroll_area_widget: Optional[QWidget] = None
        self.scroll_area_layout: Optional[QVBoxLayout] = None

    def show_fingerprint_registration(self):
        """Muestra la interfaz de registro de huellas"""
        if self.window is not None:
            try:
                self.window.raise_()
                self.window.activateWindow()
                return
            except Exception:
                pass

        # Crear ventana como QDialog modal
        self.window = QDialog(self.parent)
        self.window.setWindowTitle("REGISTRO DE HUELLAS - SISTEMA CEFA")
        self.window.resize(self.screen_width, self.screen_height)
        self.window.setModal(True)

        # Construir UI
        self._create_interface(self.window)

        # Inicializar lector biométrico y cargar datos
        self._initialize_biometric_scanner()
        self._load_personal_data()

        # Mostrar
        self.window.finished.connect(self._on_closed)
        self.window.show()

    def _create_interface(self, win: QDialog):
        root = QVBoxLayout(win)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        # Header
        header = QVBoxLayout()
        title = QLabel("🔐 REGISTRO DE HUELLAS")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("color: #00ffff; font-weight: 700; font-size: 18px;")
        subtitle = QLabel("Gestionar huellas digitales del personal")
        subtitle.setAlignment(Qt.AlignHCenter)
        subtitle.setStyleSheet("color: #cccccc;")
        header.addWidget(title)
        header.addWidget(subtitle)
        header_frame = QFrame()
        header_frame.setLayout(header)
        root.addWidget(header_frame)

        # Controls (tipo + búsqueda + check)
        controls = QHBoxLayout()
        type_label = QLabel("Tipo de Personal:")
        type_label.setStyleSheet("font-weight: 600;")
        self.type_combo = QComboBox()
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        controls.addWidget(type_label)
        controls.addWidget(self.type_combo)

        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("font-weight: 600;")
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Nombre o documento…")
        self.search_entry.textChanged.connect(self._on_search_changed)
        controls.addWidget(search_label)
        controls.addWidget(self.search_entry, 1)

        check_btn = QPushButton("🔌")
        check_btn.clicked.connect(self._check_scanner_connection)
        controls.addWidget(check_btn)

        controls_frame = QFrame()
        controls_frame.setLayout(controls)
        root.addWidget(controls_frame)

        # Content area (scroll)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area_layout.setSpacing(4)
        scroll.setWidget(self.scroll_area_widget)
        root.addWidget(scroll, 1)

        # Footer (status + count)
        footer = QHBoxLayout()
        self.status_label = QLabel("Listo para registrar huellas")
        self.status_label.setStyleSheet("color: #888888;")
        self.count_label = QLabel("0 registros")
        self.count_label.setStyleSheet("color: #00ffff;")
        footer.addWidget(self.status_label)
        footer.addStretch(1)
        footer.addWidget(self.count_label)
        footer_frame = QFrame()
        footer_frame.setLayout(footer)
        root.addWidget(footer_frame)

    def _initialize_biometric_scanner(self):
        try:
            self._update_status("Conectando al lector biométrico...")

            def connect_scanner():
                try:
                    if biometric_scanner.test_com3_connection():
                        QTimer.singleShot(0, lambda: self._update_status("✅ Lector biométrico conectado en COM3"))
                        print("✅ Lector biométrico inicializado correctamente en COM3")
                    elif biometric_scanner.connect():
                        QTimer.singleShot(0, lambda: self._update_status("✅ Lector biométrico conectado"))
                        print("✅ Lector biométrico inicializado correctamente")
                    else:
                        def show_warn():
                            self._update_status("⚠️ Lector biométrico no disponible")
                            QMessageBox.warning(self.window, "Advertencia",
                                                "Lector biométrico no disponible. Algunas funciones pueden estar limitadas.\n\n"
                                                "Posibles soluciones:\n"
                                                "• Verifique que el lector esté conectado por USB en COM3\n"
                                                "• Compruebe que el puerto COM3 esté disponible\n"
                                                "• Instale los drivers del lector\n"
                                                "• Asegúrese de que el lector esté encendido\n"
                                                "• Use el botón 🔌 para intentar reconectar")
                        QTimer.singleShot(0, show_warn)
                        print("⚠️ Lector biométrico no pudo conectarse")
                except Exception as e:
                    err = f"Error conectando lector: {e}"
                    print(f"❌ {err}")
                    QTimer.singleShot(0, lambda: self._update_status("❌ Error conectando lector"))
                    QTimer.singleShot(0, lambda: QMessageBox.critical(self.window, "Error de Conexión", err))

            threading.Thread(target=connect_scanner, daemon=True).start()
        except Exception as e:
            print(f"❌ Error inicializando lector biométrico: {e}")
            self._update_status("⚠️ Error inicializando lector biométrico")

    def _load_personal_data(self):
        try:
            personal_types = get_personal_types()
            type_names = ["TODOS"] + [pt["nombre"] for pt in personal_types]
            self.type_combo.clear()
            self.type_combo.addItems(type_names)

            self.personal_data = self._get_all_personal()
            self.filtered_data = list(self.personal_data)
            self._update_personal_list()
            self._update_count()
            log_file("✅ Datos de personal cargados correctamente")
        except Exception as e:
            error_msg = f"Error cargando datos: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            QMessageBox.critical(self.window, "Error de Conexión", "Error de conexión a la base de datos")

    def _get_all_personal(self) -> List[Dict[str, Any]]:
        query = """
            SELECT p.id, p.tipo_personal_id, p.documento_tipo, p.documento_numero,
                   p.nombres, p.apellidos, p.email, p.telefono, p.direccion,
                   p.fecha_nacimiento, p.genero, p.huella_digital, p.fecha_registro_huella,
                   p.activo, p.fecha_contratacion, p.fecha_terminacion,
                   tp.nombre as tipo_personal_nombre, tp.max_llaves_por_dia, tp.permisos_especiales
            FROM personal p
            JOIN tipos_personal tp ON p.tipo_personal_id = tp.id
            WHERE p.activo = 1 AND p.deleted_at IS NULL
            ORDER BY p.nombres, p.apellidos
        """
        try:
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                cur.execute(query)
                personal = cur.fetchall()
                cur.close()
                return personal
        except Exception as e:
            print(f"❌ Error obteniendo personal: {e}")
            return []

    def _on_type_changed(self, index: int):
        self.current_personal_type = self.type_combo.currentText()
        self._apply_filters()

    def _on_search_changed(self, text: str):
        self.search_text = text.lower()
        self._apply_filters()

    def _apply_filters(self):
        self.filtered_data = []
        for person in self.personal_data:
            if self.current_personal_type != "TODOS":
                if person["tipo_personal_nombre"] != self.current_personal_type:
                    continue
            if self.search_text:
                searchable = f"{person['nombres']} {person['apellidos']} {person['documento_numero']}".lower()
                if self.search_text not in searchable:
                    continue
            self.filtered_data.append(person)
        self._update_personal_list()
        self._update_count()

    def _update_personal_list(self):
        # Limpiar
        while self.scroll_area_layout.count():
            child = self.scroll_area_layout.takeAt(0)
            w = child.widget()
            if w is not None:
                w.deleteLater()
        if not self.filtered_data:
            no_data = QLabel("No se encontraron registros")
            no_data.setStyleSheet("color: #888888;")
            self.scroll_area_layout.addWidget(no_data)
            return
        # Crear tarjetas
        for person in self.filtered_data:
            self._create_person_card(person)
        # Relleno final
        self.scroll_area_layout.addStretch(1)

    def _create_person_card(self, person: Dict[str, Any]):
        card = QFrame(self.scroll_area_widget)
        card.setFrameShape(QFrame.NoFrame)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # Inicial/avatar
        initial = person["nombres"][0].upper() if person["nombres"] else "?"
        avatar = QLabel(initial)
        avatar.setStyleSheet("background:#00ffff;color:#000;font-weight:700;font-size:16px;padding:8px 12px;border-radius:4px;")
        layout.addWidget(avatar)

        # Info
        info_col = QVBoxLayout()
        name_lbl = QLabel(f"{person['nombres']} {person['apellidos']}")
        name_lbl.setStyleSheet("color:#00ffff;font-weight:700;")
        info_col.addWidget(name_lbl)
        id_type_row = QHBoxLayout()
        id_lbl = QLabel(f"ID: {person['id']}")
        type_lbl = QLabel(f"• {person['tipo_personal_nombre']}")
        id_lbl.setStyleSheet("color:#ccc;")
        type_lbl.setStyleSheet("color:#888;")
        id_type_row.addWidget(id_lbl)
        id_type_row.addWidget(type_lbl)
        id_type_row.addStretch(1)
        info_col.addLayout(id_type_row)

        # Estado de huella
        fingerprint_status = "✅ Registrada" if person["huella_digital"] else "❌ Sin registrar"
        status_color = "#4caf50" if person["huella_digital"] else "#ff6b6b"
        status_lbl = QLabel(fingerprint_status)
        status_lbl.setStyleSheet(f"color:{status_color};font-weight:700;")
        info_col.addWidget(status_lbl)
        layout.addLayout(info_col, 1)

        # Acción
        btn = QPushButton("🔄 Actualizar" if person.get("huella_digital") else "👆 Registrar")
        btn.clicked.connect(lambda _, p=person: self._register_fingerprint(p))
        layout.addWidget(btn)

        self.scroll_area_layout.addWidget(card)

    def _register_fingerprint(self, person: Dict[str, Any]):
        if self.scanning:
            QMessageBox.warning(self.window, "Advertencia", "Ya hay un escaneo en progreso. Espere a que termine.")
            return
        has_fingerprint = person.get('huella_digital') is not None
        action = "actualizar" if has_fingerprint else "registrar"
        result = QMessageBox.question(
            self.window,
            f"Confirmar {action.title()}",
            (
                f"¿Desea {action} la huella digital de:\n\n"
                f"{person['nombres']} {person['apellidos']}\n"
                f"ID: {person['id']}\n"
                f"Tipo: {person['tipo_personal_nombre']}\n\n"
                f"Coloque su dedo en el lector biométrico cuando esté listo."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return
        if not biometric_scanner.connected:
            self._update_status("Conectando al lector biométrico...")
            if not biometric_scanner.connect():
                QMessageBox.critical(self.window, "Error de Conexión", "No se pudo conectar al lector biométrico.\n\nVerifique que el lector esté conectado y configurado correctamente.")
                return
        self.scanning = True
        self._update_status(f"Escaneando huella digital para {action}...")
        thread = threading.Thread(target=self._scan_fingerprint_thread, args=(person, action), daemon=True)
        thread.start()

    def _scan_fingerprint_thread(self, person: Dict[str, Any], action: str):
        try:
            person_id = person["id"]
            person_name = f"{person['nombres']} {person['apellidos']}"
            if action == "registrar":
                success, message = biometric_scanner.register_fingerprint_for_person(person_id, person_name)
            else:
                success, message = biometric_scanner.update_fingerprint_for_person(person_id, person_name)
            if success:
                QTimer.singleShot(0, lambda: QMessageBox.information(self.window, "Registro Exitoso", message))
                QTimer.singleShot(0, self._load_personal_data)
                QTimer.singleShot(0, lambda: self._update_status(f"✅ {message}"))
                log_file(f"✅ {message}")
            else:
                QTimer.singleShot(0, lambda: QMessageBox.critical(self.window, "Error de Registro", message))
                QTimer.singleShot(0, lambda: self._update_status(f"❌ {message}"))
                log_file(f"❌ {message}")
        except Exception as e:
            error_msg = f"Error en escaneo: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            QTimer.singleShot(0, lambda: QMessageBox.critical(self.window, "Error del Sistema", "Error en el sistema de escaneo"))
            QTimer.singleShot(0, lambda: self._update_status("❌ Error en el sistema"))
        finally:
            self.scanning = False

    def _update_status(self, message: str):
        if self.status_label is not None:
            self.status_label.setText(message)

    def _update_count(self):
        if self.count_label is not None:
            self.count_label.setText(f"{len(self.filtered_data)} registros")

    def _check_scanner_connection(self):
        try:
            self._update_status("🔌 Verificando conexión del lector...")
            if biometric_scanner.connected:
                self._update_status("✅ Lector biométrico conectado")
                QMessageBox.information(self.window, "Conexión Exitosa", "El lector biométrico está conectado y listo para usar.")
            else:
                self._update_status("⚠️ Lector biométrico no disponible")
                if biometric_scanner.test_com3_connection():
                    self._update_status("✅ Lector biométrico conectado en COM3")
                    QMessageBox.information(self.window, "Conexión Exitosa", "El lector biométrico se ha conectado correctamente en COM3.")
                elif biometric_scanner.connect():
                    self._update_status("✅ Lector biométrico reconectado")
                    QMessageBox.information(self.window, "Reconexión Exitosa", "El lector biométrico se ha reconectado correctamente.")
                else:
                    self._update_status("❌ No se pudo conectar al lector")
                    QMessageBox.critical(
                        self.window,
                        "Error de Conexión",
                        (
                            "No se pudo conectar al lector biométrico.\n\n"
                            "Verifique que:\n"
                            "• El lector esté conectado por USB en COM3\n"
                            "• El puerto COM3 esté disponible\n"
                            "• Los drivers estén instalados\n"
                            "• El lector esté encendido\n"
                            "• No haya otros programas usando COM3"
                        ),
                    )
        except Exception as e:
            print(f"❌ Error verificando conexión: {e}")
            self._update_status("❌ Error verificando conexión")
            QMessageBox.critical(self.window, "Error del Sistema", f"Error verificando conexión: {e}")

    def _on_closed(self, *args):
        if self.scanning:
            QMessageBox.warning(self.window, "Escaneo en Progreso", "Hay un escaneo en progreso. Espere a que termine.")
            return
        try:
            biometric_scanner.disconnect()
        except Exception:
            pass
        if self.parent is not None:
            try:
                self.parent.show()
                self.parent.raise_()
                self.parent.activateWindow()
            except Exception:
                pass
        self.window = None


# Función para mostrar la interfaz desde el sistema principal
def show_fingerprint_registration_interface(parent=None):
    interface = FingerprintRegistrationInterface(parent)
    interface.show_fingerprint_registration()
    return interface
