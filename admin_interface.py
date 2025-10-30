#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
admin_interface.py
- Interfaz de administrador (PySide6)
"""

from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QScrollArea, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import styles
from config import *
from utils import *
# from fingerprint_registration_interface import show_fingerprint_registration_interface

class AdminInterface:
    def __init__(self, parent):
        self.parent = parent

    def show_admin_interface(self):
        admin_win = styles.create_modal_window(self.parent, "🔐 INTERFAZ DE ADMINISTRADOR - SISTEMA CEFA", ADMIN_WINDOW_SIZE)

        layout = QVBoxLayout(admin_win)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        welcome_label = styles.create_title_label(admin_win, "¡BIENVENIDO ADMINISTRADOR!")
        layout.addWidget(welcome_label)

        buttons_row = styles.create_main_frame(admin_win)
        buttons_layout = QVBoxLayout(buttons_row)
        select_env_btn = styles.create_futuristic_button(buttons_row, "🏢  Seleccionar Ambiente", lambda: self._show_environment_selection(admin_win))
        register_fp_btn = styles.create_futuristic_button(buttons_row, "👆  Registrar Huella", lambda: self._show_fingerprint_registration(admin_win))
        buttons_layout.addWidget(select_env_btn)
        buttons_layout.addWidget(register_fp_btn)
        layout.addWidget(buttons_row)

        logout_btn = styles.create_danger_button(admin_win, "🚪 CERRAR SESIÓN", admin_win.close)
        layout.addWidget(logout_btn)

        styles.center_window(admin_win)
        admin_win.show()

    def _show_environment_selection(self, parent_window):
        """Muestra la interfaz de selección de ambientes con cuadrícula 4x3"""
        # Ocultar la ventana padre
        parent_window.hide()
        
        # Crear ventana de selección de ambientes
        env_win = styles.create_modal_window(self.parent, "🏢 SELECCIÓN DE AMBIENTES - SISTEMA CEFA", ENVIRONMENT_WINDOW_SIZE)
        outer = QVBoxLayout(env_win)
        outer.setContentsMargins(40, 20, 40, 20)
        outer.setSpacing(12)
        outer.addWidget(styles.create_title_label(env_win, "🏢 SELECCIÓN DE AMBIENTES"))
        outer.addWidget(styles.create_subtitle_label(env_win, "Seleccione el ambiente que desea gestionar"))

        scroll = QScrollArea(env_win)
        scroll.setWidgetResizable(True)
        grid_holder = styles.create_main_frame(scroll)
        grid_layout = QVBoxLayout(grid_holder)
        grid_layout.setSpacing(12)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        from utils import get_available_environments
        ambientes_reales = get_available_environments()
        if not ambientes_reales:
            grid_layout.addWidget(styles.create_subtitle_label(grid_holder, "No hay ambientes disponibles en la base de datos"))
        else:
            # Render simple en lista vertical de botones (equivalente funcional)
            # Escala responsive para alturas y tipografía
            try:
                sw = env_win.screen().availableGeometry().width()
                scale = max(0.6, min(1.6, sw / 1920.0))
            except Exception:
                scale = 1.0

            for ambiente in ambientes_reales:
                ambiente_id, nombre, descripcion, tipo, ubicacion, piso, edificio = ambiente
                subtitle = f"Ubicación: {ubicacion}" if ubicacion else ""
                row = styles.create_clickable_row(
                    grid_holder,
                    nombre,
                    subtitle,
                    lambda aid=ambiente_id, name=nombre: self._select_environment(name, aid),
                    min_height=int(84 * scale)
                )
                grid_layout.addWidget(row)
                
                # Separador sutil entre botones
                spacer = QWidget(grid_holder)
                spacer.setFixedHeight(2)
                grid_layout.addWidget(spacer)
        # Evitar obligar ancho mínimo que genere scroll horizontal
        scroll.setWidget(grid_holder)
        outer.addWidget(scroll)

        controls = styles.create_main_frame(env_win)
        controls_layout = QHBoxLayout(controls)
        back_btn = styles.create_warning_button(controls, "⬅️ VOLVER", lambda: self._back_to_admin_interface(env_win, parent_window))
        close_btn = styles.create_danger_button(controls, "❌ CERRAR", env_win.close)
        controls_layout.addWidget(back_btn)
        controls_layout.addWidget(close_btn)
        outer.addWidget(controls)

        styles.center_window(env_win)
        env_win.show()

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
