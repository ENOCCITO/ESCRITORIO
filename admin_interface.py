#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
admin_interface.py
- Interfaz de administrador del sistema de dispensación biométrica
- Gestión de ambientes y registro de huellas
"""

import tkinter as tk
from tkinter import messagebox
import styles
from config import *
from utils import *
from fingerprint_registration_interface import show_fingerprint_registration_interface

class AdminInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_admin_interface(self):
        """Muestra la interfaz de administrador con dos botones como en la imagen"""
        # Crear ventana principal de administrador
        admin_win = styles.create_modal_window(self.parent, "🔐 INTERFAZ DE ADMINISTRADOR - SISTEMA CEFA", ADMIN_WINDOW_SIZE)
        
        # Contenedor principal
        main_container = styles.create_main_frame(admin_win)
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Título de bienvenida
        welcome_label = styles.create_title_label(main_container, "¡BIENVENIDO ADMINISTRADOR!")
        welcome_label.pack(pady=(0, 40))
        
        # Contenedor para los dos botones
        buttons_container = styles.create_main_frame(main_container)
        buttons_container.pack(expand=True)
        
        # Primer botón: Seleccionar Ambiente
        select_env_btn = styles.create_futuristic_button(
            buttons_container, 
            "Seleccionar Ambiente", 
            lambda: self._show_environment_selection(admin_win)
        )
        
        # Aplicar efectos de hover
        styles.apply_button_hover_effects(select_env_btn)
        select_env_btn.pack(pady=(0, 30))
        
        # Segundo botón: Registrar Huella
        register_fp_btn = styles.create_futuristic_button(
            buttons_container, 
            "Registrar Huella", 
            lambda: self._show_fingerprint_registration(admin_win)
        )
        
        # Aplicar efectos de hover
        styles.apply_button_hover_effects(register_fp_btn)
        register_fp_btn.pack()
        
        # Botón de cerrar sesión
        logout_btn = styles.create_danger_button(
            main_container, 
            "🚪 CERRAR SESIÓN", 
            admin_win.destroy
        )
        logout_btn.pack(side="bottom", pady=(20, 0))
        
        # Centrar la ventana
        styles.center_window(admin_win)

    def _show_environment_selection(self, parent_window):
        """Muestra la interfaz de selección de ambientes con cuadrícula 4x3"""
        # Ocultar la ventana padre
        parent_window.withdraw()
        
        # Crear ventana de selección de ambientes
        env_win = styles.create_modal_window(self.parent, "🏢 SELECCIÓN DE AMBIENTES - SISTEMA CEFA", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(env_win, "🏢 SELECCIÓN DE AMBIENTES")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(env_win, "Seleccione el ambiente que desea gestionar")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal para la cuadrícula de botones
        grid_container = styles.create_main_frame(env_win)
        grid_container.pack(expand=True, padx=40, pady=20)
        
        # Configurar el grid 4x3
        for i in range(4):
            grid_container.grid_rowconfigure(i, weight=1)
        for i in range(3):
            grid_container.grid_columnconfigure(i, weight=1)
        
        # Obtener ambientes reales de la base de datos
        from utils import get_available_environments
        ambientes_reales = get_available_environments()
        
        if not ambientes_reales:
            # Si no hay ambientes en la BD, mostrar mensaje
            no_env_label = styles.create_subtitle_label(grid_container, "No hay ambientes disponibles en la base de datos")
            no_env_label.grid(row=0, column=0, columnspan=3, pady=50)
        else:
            # Crear botones de ambientes reales con estilo futurista
            for i, ambiente in enumerate(ambientes_reales):
                row = i // 3
                col = i % 3
                
                # Extraer información del ambiente
                ambiente_id, nombre, descripcion, tipo, ubicacion, piso, edificio = ambiente
                
                # Construir texto del botón
                button_text = nombre
                if ubicacion:
                    button_text += f"\n{ubicacion}"
                
                env_btn = styles.create_futuristic_button(
                    grid_container, 
                    button_text, 
                    lambda aid=ambiente_id, name=nombre: self._select_environment(name, aid),
                    width=15, 
                    height=2
                )
                
                # Aplicar efectos de hover
                styles.apply_button_hover_effects(env_btn)
                env_btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Botones de control
        control_frame = styles.create_main_frame(env_win)
        control_frame.pack(fill="x", padx=40, pady=20)
        
        # Botón para volver
        back_btn = styles.create_warning_button(
            control_frame, 
            "⬅️ VOLVER", 
            lambda: self._back_to_admin_interface(env_win, parent_window)
        )
        back_btn.pack(side="left")
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            env_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(env_win)

    def _show_fingerprint_registration(self, parent_window):
        """Muestra la interfaz de registro de huellas responsive"""
        try:
            # Mostrar la nueva interfaz de registro de huellas
            interface = show_fingerprint_registration_interface(self.parent)
            
            # Ocultar la ventana padre después de que la nueva ventana esté lista
            def hide_parent():
                parent_window.withdraw()
            
            # Programar el ocultamiento de la ventana padre
            self.parent.after(100, hide_parent)
            
        except Exception as e:
            print(f"❌ Error mostrando interfaz de registro de huellas: {e}")
            messagebox.showerror("Error", f"Error mostrando interfaz de registro de huellas:\n{e}")
            # Mostrar ventana padre en caso de error
            parent_window.deiconify()

    def _select_environment(self, env_name, ambiente_id=None):
        """Maneja la selección de un ambiente"""
        if ambiente_id:
            messagebox.showinfo("🏢 AMBIENTE SELECCIONADO", 
                               f"Ha seleccionado: {env_name}\n"
                               f"ID del ambiente: {ambiente_id}\n\n"
                               "El sistema está configurado para gestionar este ambiente.\n"
                               "¿Desea proceder con la configuración?")
        else:
            messagebox.showinfo("🏢 AMBIENTE SELECCIONADO", 
                               f"Ha seleccionado: {env_name}\n\n"
                               "El sistema está configurado para gestionar este ambiente.\n"
                               "¿Desea proceder con la configuración?")
        
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
        user_frame = styles.create_content_frame(container)
        user_frame.pack(fill="x", pady=2, padx=10)
        
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
