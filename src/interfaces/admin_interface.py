#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
admin_interface.py
- Interfaz de administrador (PySide6)
"""

from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QScrollArea, QSizePolicy, QGridLayout, QSpacerItem, QPushButton, QFrame
from PySide6.QtGui import QFont, QFontMetrics, QIcon, QPixmap
from PySide6.QtCore import Qt, QObject, QEvent
from src.utils import styles
from src.config.config import *
from src.utils.utils import *
from src.interfaces.dialog_utils import CleanCloseDialog
# from src.interfaces.fingerprint_registration_interface import show_fingerprint_registration_interface


class AdminInterface:
    def __init__(self, parent):
        self.parent = parent
    
    def _close_and_restore(self, window):
        """Cierra la ventana actual y restaura la ventana principal"""
        try:
            window.close()
            # Restaurar la ventana principal
            if hasattr(self.parent, 'show_main_window'):
                self.parent.show_main_window()
        except Exception as e:
            print(f"⚠️ Error cerrando y restaurando: {e}")

    def show_admin_interface(self):
        try:
            # Colores exactos del HTML
            PRIMARY_COLOR = "#136dec"
            BG_LIGHT_HTML = "#f6f7f8"
            TEXT_GRAY_DARK = "#111418"
            TEXT_GRAY_LIGHT = "#617289"
            BORDER_COLOR = "#f0f2f4"
            
            # Crear ventana en pantalla completa real (sin barra de tareas)
            admin_win = CleanCloseDialog(self.parent)
            admin_win.setWindowTitle("Interfaz De Administrador - Sistema de Dispensación Biométrica")
            admin_win.setModal(False)  # No modal para poder interactuar con la ventana principal
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            admin_win.showFullScreen()
            
            admin_win.setStyleSheet(f"background-color: {BG_LIGHT_HTML};")
            print("✅ Creando interfaz de administrador en pantalla completa real...")

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
            
            header_layout.addWidget(left_header)
            header_layout.addStretch()
            
            # Botón cerrar (X) para volver a la pantalla principal
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
            close_btn.clicked.connect(admin_win.close)
            header_layout.addWidget(close_btn)
            
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
            
            main_title = QLabel("Bienvenido Administrador", title_container)
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
            select_env_btn.setMinimumHeight(80)  # Aumentado de 64 a 80
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
            select_env_btn.setMinimumWidth(max(300, btn_text_width + 60))  # Reducido de 400 a 300
            select_env_btn.setMaximumWidth(500)  # Limitar el ancho máximo
            
            buttons_layout.addWidget(select_env_btn)
            
            # Botón Registrar Huella
            register_fp_btn = QPushButton("Registrar Huella", buttons_container)
            register_fp_btn.setCursor(Qt.PointingHandCursor)
            register_fp_btn.setMinimumHeight(80)  # Aumentado de 64 a 80
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
            register_fp_btn.setMinimumWidth(max(300, fp_text_width + 60))  # Reducido de 400 a 300
            register_fp_btn.setMaximumWidth(500)  # Limitar el ancho máximo
            
            buttons_layout.addWidget(register_fp_btn)
        
            main_layout.addWidget(buttons_container)
            layout.addWidget(main_content, 1)

            # Ya no es necesario centrar ni llamar a show() porque showMaximized() ya lo hace
            # La ventana ya está maximizada desde el inicio
            print("✅ Interfaz de administrador mostrada correctamente en pantalla completa")
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
            
            # Crear ventana de selección de ambientes en pantalla completa
            from PySide6.QtWidgets import QScrollArea
            env_win = CleanCloseDialog(self.parent)
            env_win.setWindowTitle("Selección de Ambientes - Sistema de Dispensación Biométrica")
            env_win.setModal(False)
            
            # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
            env_win.showFullScreen()
            
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
                f"color: #000000; "
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
                f"color: #333333; "
                f"font-size: 16px; "
                f"font-weight: 400; "
                f"font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif;"
            )
            subtitle_main.setWordWrap(False)
            title_layout.addWidget(subtitle_main)
            
            main_layout.addWidget(title_container)
            
            # Lista de ambientes con cuadrícula
            scroll = QScrollArea(main_content)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet(f"background-color: transparent; border: none;")
            scroll.setFrameShape(QFrame.NoFrame)
            
            grid_holder = QWidget(scroll)
            grid_holder.setStyleSheet(f"background-color: transparent;")
            grid_layout = QGridLayout(grid_holder)  # Cambiar a QGridLayout
            grid_layout.setSpacing(20)  # Espaciado entre botones
            grid_layout.setContentsMargins(20, 20, 20, 20)
            
            from src.utils.utils import get_available_environments
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
                grid_layout.addWidget(no_data_label, 0, 0)
            else:
                # Crear botones en cuadrícula (2 columnas)
                row = 0
                col = 0
                for ambiente in ambientes_reales:
                    ambiente_id, nombre, descripcion, tipo, ubicacion, piso, edificio = ambiente
                    
                    # Crear botón para el ambiente
                    btn = QPushButton(nombre, grid_holder)
                    btn.setCursor(Qt.PointingHandCursor)
                    btn.setMinimumHeight(120)  # Botón grande
                    btn.setMinimumWidth(120)   # Cuadrado
                    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    
                    # Estilo del botón
                    btn.setStyleSheet(
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
                    
                    # Conectar el click del botón
                    btn.clicked.connect(lambda checked, eid=ambiente_id, n=nombre: self._select_environment(n, eid))
                    
                    # Agregar a la cuadrícula
                    grid_layout.addWidget(btn, row, col)
                    
                    # Mover a la siguiente posición
                    col += 1
                    if col >= 2:  # 2 columnas
                        col = 0
                        row += 1
            
            scroll.setWidget(grid_holder)
            main_layout.addWidget(scroll, 1)
            
            layout.addWidget(main_content, 1)
            
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
            from src.interfaces.fingerprint_registration_interface import show_fingerprint_registration_interface
            show_fingerprint_registration_interface(self.parent)
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
