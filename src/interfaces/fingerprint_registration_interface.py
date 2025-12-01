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

from src.utils.db_utils import get_personal_types, db_connect
from src.core.desktop_alerts import desktop_alert_system
from src.core.biometric_interface import biometric_interface
from src.utils.utils import log_file
from src.interfaces.dialog_utils import CleanCloseDialog


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

        # Colores exactos del HTML
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        CARD_BG = "#ffffff"
        
        # Crear ventana como QDialog no modal en pantalla completa real
        self.window = CleanCloseDialog(self.parent)
        self.window.setWindowTitle("Registro de Huellas - Sistema de Dispensación Biométrica")
        self.window.setModal(False)
        
        # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
        self.window.showFullScreen()
        
        self.window.setModal(False)
        self.window.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")

        # Construir UI
        self._create_interface(self.window)

        # Inicializar lector biométrico y cargar datos
        self._initialize_biometric_scanner()
        self._load_personal_data()

        # Mostrar (ya está maximizada)
        self.window.finished.connect(self._on_closed)
        print("✅ Interfaz de registro de huellas mostrada en pantalla completa")

    def _create_interface(self, win: QDialog):
        # Colores exactos del HTML
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        CARD_BG = "#ffffff"
        
        root = QVBoxLayout(win)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header (exacto del HTML)
        header = QWidget(win)
        header.setFixedHeight(60)
        header.setStyleSheet(
            f"background-color: transparent; "
            f"border-bottom: 1px solid {BORDER_COLOR};"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(16)
        
        # Logo y título izquierda
        left_header = QWidget(header)
        left_header_layout = QHBoxLayout(left_header)
        left_header_layout.setContentsMargins(0, 0, 0, 0)
        left_header_layout.setSpacing(16)
        
        logo_container = QWidget(left_header)
        logo_container.setFixedSize(24, 24)
        logo_label = QLabel("🛡️", logo_container)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; "
            f"font-size: 24px;"
        )
        left_header_layout.addWidget(logo_container)
        
        header_title = QLabel("Sistema de Dispensación Biométrica", left_header)
        header_title.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 18px; "
            f"font-weight: 700; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        header_title.setWordWrap(False)
        left_header_layout.addWidget(header_title)
        
        header_layout.addWidget(left_header)
        header_layout.addStretch()
        
        # Botón Volver (oculto para interfaces más limpias)
        # back_btn = QPushButton("← Volver", header)
        # back_btn.setCursor(Qt.PointingHandCursor)
        # back_btn.setStyleSheet(
        #     f"background-color: #f0f2f4; "
        #     f"color: {TEXT_GRAY_DARK}; "
        #     f"border: none; "
        #     f"border-radius: 8px; "
        #     f"padding: 8px 12px; "
        #     f"font-size: 14px; "
        #     f"font-weight: 700;"
        # )
        # back_btn.clicked.connect(win.close)
        # header_layout.addWidget(back_btn)
        
        root.addWidget(header)
        
        # Main content
        main_content = QWidget(win)
        main_content.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)
        
        # Título principal centrado
        title_container = QWidget(main_content)
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        title_layout.setAlignment(Qt.AlignCenter)
        
        main_title = QLabel("Registro de Huellas", title_container)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 36px; "
            f"font-weight: 900; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif; "
            f"line-height: 1.2;"
        )
        main_title.setWordWrap(False)
        title_layout.addWidget(main_title)
        
        subtitle_main = QLabel("Gestionar huellas digitales del personal", title_container)
        subtitle_main.setAlignment(Qt.AlignCenter)
        subtitle_main.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 16px; "
            f"font-weight: 400; "
            f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
        )
        subtitle_main.setWordWrap(False)
        title_layout.addWidget(subtitle_main)
        
        main_layout.addWidget(title_container)

        # Controls (tipo + búsqueda + check)
        controls_container = QWidget(main_content)
        controls_container.setStyleSheet(f"background-color: {CARD_BG}; border: 1px solid {BORDER_COLOR}; border-radius: 12px; padding: 20px;")
        controls = QHBoxLayout(controls_container)
        controls.setContentsMargins(0, 0, 0, 0)
        controls.setSpacing(16)
        
        type_label = QLabel("Tipo de Personal:", controls_container)
        type_label.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        type_label.setWordWrap(False)
        self.type_combo = QComboBox(controls_container)
        self.type_combo.setStyleSheet(
            f"background-color: {BG_LIGHT_HTML}; "
            f"border: 1px solid {BORDER_COLOR}; "
            f"border-radius: 8px; "
            f"padding: 8px 12px; "
            f"font-size: 14px; "
            f"color: {TEXT_GRAY_DARK}; "
            f"QComboBox::drop-down {{ border: none; }} "
            f"QComboBox QAbstractItemView {{ background-color: {CARD_BG}; color: {TEXT_GRAY_DARK}; border: 1px solid {BORDER_COLOR}; border-radius: 8px; }}"
        )
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        controls.addWidget(type_label)
        controls.addWidget(self.type_combo)

        search_label = QLabel("Buscar:", controls_container)
        search_label.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        search_label.setWordWrap(False)
        self.search_entry = QLineEdit(controls_container)
        self.search_entry.setPlaceholderText("Nombre o documento…")
        self.search_entry.setStyleSheet(
            f"background-color: {BG_LIGHT_HTML}; "
            f"border: 1px solid {BORDER_COLOR}; "
            f"border-radius: 8px; "
            f"padding: 8px 12px; "
            f"font-size: 14px; "
            f"color: {TEXT_GRAY_DARK}; "
            f"selection-background-color: {PRIMARY_COLOR}; "
            f"selection-color: white;"
        )
        self.search_entry.textChanged.connect(self._on_search_changed)
        controls.addWidget(search_label)
        controls.addWidget(self.search_entry, 1)

        check_btn = QPushButton("🔌 Verificar Conexión", controls_container)
        check_btn.setCursor(Qt.PointingHandCursor)
        check_btn.setStyleSheet(
            f"background-color: {PRIMARY_COLOR}; "
            f"color: white; "
            f"border: none; "
            f"border-radius: 8px; "
            f"padding: 8px 16px; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        check_btn.clicked.connect(self._check_scanner_connection)
        controls.addWidget(check_btn)
        
        main_layout.addWidget(controls_container)

        # Content area (scroll)
        scroll = QScrollArea(main_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: transparent; border: none;")
        scroll.setFrameShape(QFrame.NoFrame)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setStyleSheet(f"background-color: transparent;")
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setSpacing(12)
        scroll.setWidget(self.scroll_area_widget)
        main_layout.addWidget(scroll, 1)

        # Footer (status + count)
        footer = QWidget(main_content)
        footer.setStyleSheet(f"background-color: {CARD_BG}; border: 1px solid {BORDER_COLOR}; border-radius: 12px; padding: 16px;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(16)
        
        self.status_label = QLabel("Listo para registrar huellas", footer)
        self.status_label.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 14px; "
            f"font-weight: 400;"
        )
        self.status_label.setWordWrap(False)
        
        self.count_label = QLabel("0 registros", footer)
        self.count_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        self.count_label.setWordWrap(False)
        
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.count_label)
        
        main_layout.addWidget(footer)
        root.addWidget(main_content, 1)

    def _initialize_biometric_scanner(self):
        try:
            self._update_status("Conectando al lector biométrico...")

            def connect_scanner():
                try:
                    if biometric_interface.test_com3_connection():
                        QTimer.singleShot(0, lambda: self._update_status("✅ Lector biométrico conectado en COM3"))
                        print("✅ Lector biométrico inicializado correctamente en COM3")
                    elif biometric_interface.connect():
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
        # Colores exactos del HTML
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        CARD_BG = "#ffffff"
        
        # Limpiar
        while self.scroll_area_layout.count():
            child = self.scroll_area_layout.takeAt(0)
            w = child.widget()
            if w is not None:
                w.deleteLater()
        if not self.filtered_data:
            no_data = QLabel("No se encontraron registros")
            no_data.setAlignment(Qt.AlignCenter)
            no_data.setStyleSheet(
                f"color: {TEXT_GRAY_LIGHT}; "
                f"font-size: 16px; "
                f"font-weight: 400; "
                f"padding: 40px;"
            )
            no_data.setWordWrap(False)
            self.scroll_area_layout.addWidget(no_data)
            return
        # Crear tarjetas
        for person in self.filtered_data:
            self._create_person_card(person)
        # Relleno final
        self.scroll_area_layout.addStretch(1)

    def _create_person_card(self, person: Dict[str, Any]):
        # Colores exactos del HTML
        PRIMARY_COLOR = "#136dec"
        BG_LIGHT_HTML = "#f6f7f8"
        TEXT_GRAY_DARK = "#111418"
        TEXT_GRAY_LIGHT = "#617289"
        BORDER_COLOR = "#f0f2f4"
        CARD_BG = "#ffffff"
        
        card = QWidget(self.scroll_area_widget)
        card.setMinimumHeight(100)
        card.setStyleSheet(
            f"background-color: {CARD_BG}; "
            f"border: 1px solid {BORDER_COLOR}; "
            f"border-radius: 12px; "
            f"padding: 20px;"
        )
        card.setCursor(Qt.PointingHandCursor)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Avatar/Inicial circular
        initial = person["nombres"][0].upper() if person["nombres"] else "?"
        avatar = QLabel(initial, card)
        avatar.setFixedSize(56, 56)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(
            f"background-color: rgba(19, 109, 236, 0.1); "
            f"color: {PRIMARY_COLOR}; "
            f"font-weight: 700; "
            f"font-size: 24px; "
            f"border-radius: 28px;"
        )
        layout.addWidget(avatar)

        # Información del personal
        info_col = QVBoxLayout()
        info_col.setSpacing(4)
        info_col.setAlignment(Qt.AlignLeft)
        
        # Nombre completo
        name_lbl = QLabel(f"{person['nombres']} {person['apellidos']}", card)
        name_lbl.setStyleSheet(
            f"color: {TEXT_GRAY_DARK}; "
            f"font-size: 18px; "
            f"font-weight: 700;"
        )
        name_lbl.setWordWrap(False)
        info_col.addWidget(name_lbl)
        
        # ID y tipo en una fila
        id_type_row = QHBoxLayout()
        id_type_row.setSpacing(8)
        id_type_row.setContentsMargins(0, 0, 0, 0)
        
        id_lbl = QLabel(f"ID: {person['id']}", card)
        id_lbl.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 14px; "
            f"font-weight: 400;"
        )
        id_lbl.setWordWrap(False)
        id_type_row.addWidget(id_lbl)
        
        type_lbl = QLabel(f"• {person['tipo_personal_nombre']}", card)
        type_lbl.setStyleSheet(
            f"color: {TEXT_GRAY_LIGHT}; "
            f"font-size: 14px; "
            f"font-weight: 400;"
        )
        type_lbl.setWordWrap(False)
        id_type_row.addWidget(type_lbl)
        id_type_row.addStretch(1)
        info_col.addLayout(id_type_row)

        # Estado de huella
        fingerprint_status = "✅ Registrada" if person["huella_digital"] else "❌ Sin registrar"
        status_color = "#10b981" if person["huella_digital"] else "#ef4444"
        status_lbl = QLabel(fingerprint_status, card)
        status_lbl.setStyleSheet(
            f"color: {status_color}; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        status_lbl.setWordWrap(False)
        info_col.addWidget(status_lbl)
        
        layout.addLayout(info_col, 1)

        # Botón de acción
        btn = QPushButton("🔄 Actualizar" if person.get("huella_digital") else "👆 Registrar", card)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            f"background-color: {PRIMARY_COLOR}; "
            f"color: white; "
            f"border: none; "
            f"border-radius: 8px; "
            f"padding: 10px 20px; "
            f"font-size: 14px; "
            f"font-weight: 700;"
        )
        btn.clicked.connect(lambda _, p=person: self._register_fingerprint(p))
        
        # Calcular ancho necesario
        btn_font = btn.font()
        btn_font.setPointSize(14)
        btn_font.setBold(True)
        btn.setFont(btn_font)
        btn_fm = QFontMetrics(btn_font)
        btn_text = "🔄 Actualizar" if person.get("huella_digital") else "👆 Registrar"
        btn_text_width = btn_fm.horizontalAdvance(btn_text)
        btn.setMinimumWidth(max(150, btn_text_width + 20))
        btn.setMaximumWidth(16777215)
        
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
        if not biometric_interface.connected:
            self._update_status("Conectando al lector biométrico...")
            if not biometric_interface.connect():
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
                success, message = biometric_interface.register_fingerprint_for_person(person_id, person_name)
            else:
                success, message = biometric_interface.update_fingerprint_for_person(person_id, person_name)
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
            if biometric_interface.connected:
                self._update_status("✅ Lector biométrico conectado")
                QMessageBox.information(self.window, "Conexión Exitosa", "El lector biométrico está conectado y listo para usar.")
            else:
                self._update_status("⚠️ Lector biométrico no disponible")
                if biometric_interface.test_com3_connection():
                    self._update_status("✅ Lector biométrico conectado en COM3")
                    QMessageBox.information(self.window, "Conexión Exitosa", "El lector biométrico se ha conectado correctamente en COM3.")
                elif biometric_interface.connect():
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
            biometric_interface.disconnect()
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
