#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
admin_interface.py
- Interfaz de administrador (PySide6)
"""

from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QScrollArea, QSizePolicy, QGridLayout, QSpacerItem, QPushButton, QFrame
from PySide6.QtGui import QFont, QFontMetrics, QIcon, QPixmap
from PySide6.QtCore import Qt, QObject, QEvent
import styles
from config import *
from utils import *
# from fingerprint_registration_interface import show_fingerprint_registration_interface

class AdminInterface:
    def __init__(self, parent):
        self.parent = parent

    def show_admin_interface(self):
        try:
            # Colores exactos del HTML
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            
            # Crear ventana (no modal para que se pueda usar independientemente)
            from PySide6.QtWidgets import QDialog
            admin_win = QDialog(self.parent)
            admin_win.setWindowTitle("Interfaz De Administrador - Sistema de Dispensación Biométrica")
            admin_win.setModal(False)  # No modal para poder interactuar con la ventana principal
            try:
                w, h = [int(x) for x in ADMIN_WINDOW_SIZE.lower().split('x')]
                admin_win.resize(w, h)
            except Exception:
                admin_win.resize(600, 500)
            admin_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            print("✅ Creando interfaz de administrador...")

            layout = QVBoxLayout(admin_win)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Header (exacto del HTML)
            header = QWidget(admin_win)
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
            
            # Logo (escudo.png)
            logo_label = QLabel(left_header)
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
            left_header_layout.addWidget(logo_label)
            
            # Título del header
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
            
            # Botón Volver
            back_btn = QPushButton("← Volver", header)
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.setStyleSheet(
                f"background-color: #f0f2f4; "
                f"color: {TEXT_GRAY_DARK}; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 8px 12px; "
                f"font-size: 14px; "
                f"font-weight: 700;"
            )
            back_btn.clicked.connect(admin_win.close)
            header_layout.addWidget(back_btn)
            
            layout.addWidget(header)

            # Main content (exacto del HTML)
            main_content = QWidget(admin_win)
            main_content.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            main_layout = QVBoxLayout(main_content)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setAlignment(Qt.AlignCenter)
            
            # Título principal centrado (exacto del HTML)
            title_container = QWidget(main_content)
            title_layout = QVBoxLayout(title_container)
            title_layout.setContentsMargins(16, 40, 16, 32)
            title_layout.setSpacing(12)
            title_layout.setAlignment(Qt.AlignCenter)
            
            main_title = QLabel("Interfaz De Administrador", title_container)
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
            
            subtitle_main = QLabel("Seleccione una opción para continuar.", title_container)
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
            
            # Botones (exacto del HTML)
            buttons_container = QWidget(main_content)
            buttons_layout = QVBoxLayout(buttons_container)
            buttons_layout.setContentsMargins(16, 0, 16, 40)
            buttons_layout.setSpacing(16)
            buttons_layout.setAlignment(Qt.AlignCenter)
            
            # Botón Seleccionar Ambiente
            select_env_btn = QPushButton("Seleccionar Ambiente", buttons_container)
            select_env_btn.setCursor(Qt.PointingHandCursor)
            select_env_btn.setMinimumHeight(64)
            select_env_btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            
            # Cargar imagen para el icono
            selecambiente_pixmap = QPixmap("images/selecambiente.png")
            if not selecambiente_pixmap.isNull():
                selecambiente_pixmap = selecambiente_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                select_env_btn.setIcon(QIcon(selecambiente_pixmap))
                select_env_btn.setIconSize(selecambiente_pixmap.size())
            
            select_env_btn.setStyleSheet(
                f"background-color: {PRIMARY_COLOR}; "
                f"color: white; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 16px 20px; "
                f"font-size: 18px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            select_env_btn.clicked.connect(lambda: self._show_environment_selection(admin_win))
            # Los QPushButton no tienen setWordWrap, solo QLabel
            
            # Calcular ancho necesario para el texto
            btn_font = select_env_btn.font()
            btn_font.setPointSize(18)
            btn_font.setBold(True)
            select_env_btn.setFont(btn_font)
            btn_fm = QFontMetrics(btn_font)
            btn_text_width = btn_fm.horizontalAdvance("Seleccionar Ambiente")
            select_env_btn.setMinimumWidth(max(400, btn_text_width + 60))  # +60 para espacio del icono
            select_env_btn.setMaximumWidth(16777215)
            
            buttons_layout.addWidget(select_env_btn)
            
            # Botón Registrar Huella
            register_fp_btn = QPushButton("Registrar Huella", buttons_container)
            register_fp_btn.setCursor(Qt.PointingHandCursor)
            register_fp_btn.setMinimumHeight(64)
            register_fp_btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            
            # Cargar imagen para el icono
            huella_pixmap = QPixmap("images/huella.png")
            if not huella_pixmap.isNull():
                huella_pixmap = huella_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                register_fp_btn.setIcon(QIcon(huella_pixmap))
                register_fp_btn.setIconSize(huella_pixmap.size())
            
            register_fp_btn.setStyleSheet(
                f"background-color: {PRIMARY_COLOR}; "
                f"color: white; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 16px 20px; "
                f"font-size: 18px; "
                f"font-weight: 700; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            register_fp_btn.clicked.connect(lambda: self._show_fingerprint_registration(admin_win))
            # Los QPushButton no tienen setWordWrap, solo QLabel
            
            # Calcular ancho necesario para el texto
            register_fp_btn.setFont(btn_font)
            fp_text_width = btn_fm.horizontalAdvance("Registrar Huella")
            register_fp_btn.setMinimumWidth(max(400, fp_text_width + 60))  # +60 para espacio del icono
            register_fp_btn.setMaximumWidth(16777215)
            
            buttons_layout.addWidget(register_fp_btn)
        
            main_layout.addWidget(buttons_container)
            layout.addWidget(main_content, 1)

            styles.center_window(admin_win)
            admin_win.show()
            print("✅ Interfaz de administrador mostrada correctamente")
        except Exception as e:
            print(f"❌ Error mostrando interfaz de administrador: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error mostrando interfaz de administrador:\n{e}")

    def _show_environment_selection(self, parent_window):
        """Muestra la interfaz de selección de ambientes con diseño mejorado"""
        try:
            # Colores exactos del HTML
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            CARD_BG = "#ffffff"
            
            # Ocultar la ventana padre
            parent_window.hide()
            
            # Crear ventana de selección de ambientes
            from PySide6.QtWidgets import QDialog, QScrollArea
            env_win = QDialog(self.parent)
            env_win.setWindowTitle("Selección de Ambientes - Sistema de Dispensación Biométrica")
            env_win.setModal(False)
            try:
                w, h = [int(x) for x in ENVIRONMENT_WINDOW_SIZE.lower().split('x')]
                env_win.resize(w, h)
            except Exception:
                env_win.resize(800, 700)
            env_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            
            layout = QVBoxLayout(env_win)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            # Header (exacto del HTML)
            header = QWidget(env_win)
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
            
            # Logo (escudo.png)
            logo_label = QLabel(left_header)
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
            left_header_layout.addWidget(logo_label)
            
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
            
            # Botón Volver
            back_btn = QPushButton("← Volver", header)
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.setStyleSheet(
                f"background-color: #f0f2f4; "
                f"color: {TEXT_GRAY_DARK}; "
                f"border: none; "
                f"border-radius: 8px; "
                f"padding: 8px 12px; "
                f"font-size: 14px; "
                f"font-weight: 700;"
            )
            back_btn.clicked.connect(env_win.close)
            header_layout.addWidget(back_btn)
            
            layout.addWidget(header)
            
            # Main content
            main_content = QWidget(env_win)
            main_content.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            main_layout = QVBoxLayout(main_content)
            main_layout.setContentsMargins(40, 40, 40, 40)
            main_layout.setSpacing(32)
            
            # Título principal centrado
            title_container = QWidget(main_content)
            title_layout = QVBoxLayout(title_container)
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.setSpacing(8)
            title_layout.setAlignment(Qt.AlignCenter)
            
            main_title = QLabel("Selección de Ambientes", title_container)
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
            
            subtitle_main = QLabel("Seleccione el ambiente que desea gestionar", title_container)
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
            
            # Lista de ambientes con scroll
            scroll = QScrollArea(main_content)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet(f"background-color: transparent; border: none;")
            scroll.setFrameShape(QFrame.NoFrame)
            
            grid_holder = QWidget(scroll)
            grid_holder.setStyleSheet(f"background-color: transparent;")
            grid_layout = QVBoxLayout(grid_holder)
            grid_layout.setSpacing(16)
            grid_layout.setContentsMargins(0, 0, 0, 0)
            
            from utils import get_available_environments
            ambientes_reales = get_available_environments()
            if not ambientes_reales:
                no_data_label = QLabel("No hay ambientes disponibles en la base de datos", grid_holder)
                no_data_label.setAlignment(Qt.AlignCenter)
                no_data_label.setStyleSheet(
                    f"color: {TEXT_GRAY_LIGHT}; "
                    f"font-size: 16px; "
                    f"font-weight: 400; "
                    f"padding: 40px;"
                )
                no_data_label.setWordWrap(False)
                grid_layout.addWidget(no_data_label)
            else:
                # Crear tarjetas de ambientes mejoradas
                for ambiente in ambientes_reales:
                    ambiente_id, nombre, descripcion, tipo, ubicacion, piso, edificio = ambiente
                    subtitle = f"Ubicación: {ubicacion}" if ubicacion else ""
                    
                    # Crear tarjeta de ambiente
                    card = QWidget(grid_holder)
                    card.setMinimumHeight(80)
                    card.setStyleSheet(
                        f"background-color: {CARD_BG}; "
                        f"border: 1px solid {BORDER_COLOR}; "
                        f"border-radius: 12px; "
                        f"padding: 20px;"
                    )
                    card.setCursor(Qt.PointingHandCursor)
                    
                    card_layout = QHBoxLayout(card)
                    card_layout.setContentsMargins(0, 0, 0, 0)
                    card_layout.setSpacing(16)
                    
                    # Ícono del ambiente
                    icon_label = QLabel("🏢", card)
                    icon_label.setFixedSize(48, 48)
                    icon_label.setAlignment(Qt.AlignCenter)
                    icon_label.setStyleSheet(
                        f"background-color: rgba(19, 109, 236, 0.1); "
                        f"border-radius: 24px; "
                        f"font-size: 24px;"
                    )
                    card_layout.addWidget(icon_label)
                    
                    # Información del ambiente
                    info_layout = QVBoxLayout()
                    info_layout.setSpacing(4)
                    info_layout.setAlignment(Qt.AlignLeft)
                    
                    title_label = QLabel(nombre, card)
                    title_label.setStyleSheet(
                        f"color: {TEXT_GRAY_DARK}; "
                        f"font-size: 18px; "
                        f"font-weight: 700;"
                    )
                    title_label.setWordWrap(False)
                    info_layout.addWidget(title_label)
                    
                    if subtitle:
                        subtitle_label = QLabel(subtitle, card)
                        subtitle_label.setStyleSheet(
                            f"color: {TEXT_GRAY_LIGHT}; "
                            f"font-size: 14px; "
                            f"font-weight: 400;"
                        )
                        subtitle_label.setWordWrap(False)
                        info_layout.addWidget(subtitle_label)
                    
                    card_layout.addLayout(info_layout, 1)
                    card_layout.addStretch()
                    
                    # Hover effect y click
                    class CardHoverEffect(QObject):
                        def __init__(self, widget, callback):
                            super().__init__(widget)
                            self.widget = widget
                            self.callback = callback
                        def eventFilter(self, obj, ev):
                            if ev.type() == QEvent.Enter:
                                self.widget.setStyleSheet(
                                    f"background-color: {CARD_BG}; "
                                    f"border: 1px solid {PRIMARY_COLOR}; "
                                    f"border-radius: 12px; "
                                    f"padding: 20px;"
                                )
                            elif ev.type() == QEvent.Leave:
                                self.widget.setStyleSheet(
                                    f"background-color: {CARD_BG}; "
                                    f"border: 1px solid {BORDER_COLOR}; "
                                    f"border-radius: 12px; "
                                    f"padding: 20px;"
                                )
                            elif ev.type() == QEvent.MouseButtonRelease:
                                try:
                                    if self.callback:
                                        self.callback()
                                except Exception:
                                    pass
                            return False
                    
                    # Callback para el click
                    def on_card_click():
                        self._select_environment(nombre, ambiente_id)
                    
                    hover_effect = CardHoverEffect(card, on_card_click)
                    card.installEventFilter(hover_effect)
                    card._hover_effect = hover_effect
                    
                    grid_layout.addWidget(card)
            
            scroll.setWidget(grid_holder)
            main_layout.addWidget(scroll, 1)
            
            layout.addWidget(main_content, 1)
            
            styles.center_window(env_win)
            env_win.show()
        except Exception as e:
            print(f"❌ Error mostrando interfaz de selección de ambientes: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.parent, "Error", f"Error mostrando interfaz de selección de ambientes:\n{e}")
            parent_window.show()

    def _show_fingerprint_registration(self, parent_window):
        """Muestra la interfaz de registro de huellas responsive"""
        try:
            from fingerprint_registration_interface import show_fingerprint_registration_interface
            show_fingerprint_registration_interface(self.parent)
            QTimer = __import__('PySide6.QtCore', fromlist=['Qt']).QTimer
            QTimer.singleShot(100, parent_window.hide)
        except Exception as e:
            print(f"❌ Error mostrando interfaz de registro de huellas: {e}")
            QMessageBox.critical(self.parent, "Error", f"Error mostrando interfaz de registro de huellas:\n{e}")
            parent_window.show()

    def _select_environment(self, env_name, ambiente_id=None):
        """Maneja la selección de un ambiente"""
        if ambiente_id:
            QMessageBox.information(self.parent, "🏢 AMBIENTE SELECCIONADO",
                                    f"Ha seleccionado: {env_name}\nID del ambiente: {ambiente_id}\n\nEl sistema está configurado para gestionar este ambiente.\n¿Desea proceder con la configuración?")
        else:
            QMessageBox.information(self.parent, "🏢 AMBIENTE SELECCIONADO",
                                    f"Ha seleccionado: {env_name}\n\nEl sistema está configurado para gestionar este ambiente.\n¿Desea proceder con la configuración?")
        
        # Aquí se podría integrar con la lógica del sistema original
        # para configurar el ambiente seleccionado

    def _load_users_list(self, container):
        """Carga la lista de usuarios desde la base de datos"""
        try:
            # Obtener usuarios de la base de datos
            users = get_users_from_database(self.parent.candidates if hasattr(self.parent, 'candidates') else [])
            
            # Crear elementos de la lista
            for i, user in enumerate(users):
                self._create_user_list_item(container, user, i)
                
        except Exception as e:
            # Si hay error, mostrar usuarios de ejemplo
            self._create_sample_users(container)

    def _create_sample_users(self, container):
        """Crea usuarios de ejemplo si no hay base de datos"""
        sample_users = create_sample_users()
        
        for i, user in enumerate(sample_users):
            self._create_user_list_item(container, user, i)

    def _create_user_list_item(self, container, user, index):
        """Crea un elemento de la lista de usuarios"""
        # Frame para cada usuario
        # Este método no se usa en PySide6 migrado aún; mantenido por compatibilidad lógica.
        user_frame = styles.create_content_frame(container)
        
        # Avatar (círculo con inicial)
        avatar_frame = styles.create_main_frame(user_frame)
        avatar_frame.configure(width=50, height=50)
        avatar_frame.pack(side="left", padx=15, pady=10)
        avatar_frame.pack_propagate(False)
        
        # Crear avatar circular
        avatar_canvas = tk.Canvas(avatar_frame, bg=ACCENT_BLUE, highlightthickness=0, 
                                 width=50, height=50)
        avatar_canvas.pack(expand=True)
        
        # Dibujar círculo y inicial
        avatar_canvas.create_oval(5, 5, 45, 45, fill=ACCENT_BLUE, outline=ACCENT_CYAN, width=2)
        initial = user['name'][0].upper() if user['name'] else "U"
        avatar_canvas.create_text(25, 25, text=initial, font=FONT_BUTTON, 
                                 fill=TEXT_WHITE)
        
        # Información del usuario
        info_frame = styles.create_main_frame(user_frame)
        info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
        
        # Nombre del usuario
        name_label = styles.create_info_label(info_frame, user['name'])
        name_label.configure(font=FONT_BUTTON)
        name_label.pack(anchor="w")
        
        # ID del usuario
        id_label = styles.create_info_label(info_frame, user['document'])
        id_label.pack(anchor="w")
        
        # Botón de registrar huella
        register_btn = styles.create_accent_button(
            user_frame, 
            "Registrar Huella", 
            lambda u=user: self._register_user_fingerprint(u)
        )
        register_btn.pack(side="right", padx=15, pady=10)
        
        # Efecto de selección al hacer hover
        user_frame.bind("<Enter>", lambda e, f=user_frame: f.configure(bg=BG_LIGHT))
        user_frame.bind("<Leave>", lambda e, f=user_frame: f.configure(bg=BG_MEDIUM))

    def _search_users(self, query, user_list):
        """Realiza búsqueda de usuarios"""
        if not query or query == "Buscar por número de documento, nombre...":
            messagebox.showinfo("🔍 BÚSQUEDA", "Por favor, ingrese un término de búsqueda válido.")
            return
        
        # Aquí se implementaría la búsqueda real en la base de datos
        messagebox.showinfo("🔍 BÚSQUEDA", f"Buscando usuarios que coincidan con: '{query}'\n\n"
                           "Esta funcionalidad se integrará con la base de datos del sistema.")

    def _register_user_fingerprint(self, user):
        """Inicia el registro de huella para un usuario específico"""
        # Mostrar modal de registro de huella
        messagebox.showinfo("👆 REGISTRO DE HUELLA", 
                           f"Registrando huella para: {user['name']}\n\n"
                           "Coloque su dedo en el lector biométrico para capturar la huella digital.")
        
        # Aquí se integraría con el lector biométrico real
        # self._start_fingerprint_capture_for_user(user)

    def _back_to_admin_interface(self, current_window, parent_window):
        """Vuelve a la interfaz de administrador"""
        current_window.destroy()
        parent_window.deiconify()  # Mostrar la ventana padre nuevamente
