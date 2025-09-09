#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fingerprint_registration_interface.py
- Interfaz de registro de huellas digitales responsive para pantalla TFT 7 pulgadas
- Filtrado por tipo de personal y diseño optimizado para pantallas pequeñas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional
import threading
import time
from datetime import datetime

from db_utils import get_personal_types, get_personal_by_id, db_connect
from desktop_alerts import desktop_alert_system
from biometric_scanner import biometric_scanner
from utils import log_file

class FingerprintRegistrationInterface:
    """Interfaz de registro de huellas digitales responsive"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.personal_data = []
        self.filtered_data = []
        self.current_personal_type = "TODOS"
        self.search_text = ""
        self.scanning = False
        
        # Configuración para pantalla TFT 7 pulgadas
        self.screen_width = 800
        self.screen_height = 480
        self.font_size_small = 10
        self.font_size_medium = 12
        self.font_size_large = 16
        self.font_size_xlarge = 20
        
    def show_fingerprint_registration(self):
        """Muestra la interfaz de registro de huellas"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return
            
        # Si hay un padre, crear como Toplevel, sino como Tk principal
        if self.parent:
            self.window = tk.Toplevel(self.parent)
            # Configurar para que se mantenga en primer plano
            self.window.transient(self.parent)
            self.window.grab_set()
        else:
            self.window = tk.Tk()
            
        self.window.title("REGISTRO DE HUELLAS - SISTEMA CEFA")
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.window.resizable(True, True)
        self.window.configure(bg="#0a0a0a")
        
        # Centrar ventana
        self._center_window()
        
        # Configurar para pantalla pequeña
        self.window.minsize(640, 360)
        
        # Asegurar que la ventana esté visible
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
        
        # Crear interfaz
        self._create_interface()
        
        # Inicializar lector biométrico
        self._initialize_biometric_scanner()
        
        # Cargar datos
        self._load_personal_data()
        
        # Configurar cierre
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Ejecutar si es ventana principal
        if not self.parent:
            self.window.mainloop()
    
    def _center_window(self):
        """Centra la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_interface(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear layout responsive
        self._create_header(main_frame)
        self._create_controls(main_frame)
        self._create_content_area(main_frame)
        self._create_footer(main_frame)
    
    def _create_header(self, parent):
        """Crea el encabezado de la interfaz"""
        header_frame = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=1)
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Título principal
        title_frame = tk.Frame(header_frame, bg="#1a1a2e")
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 REGISTRO DE HUELLAS",
            font=("Segoe UI", self.font_size_xlarge, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(side="left")
        
        # Subtítulo
        subtitle_label = tk.Label(
            title_frame,
            text="Gestionar huellas digitales del personal",
            font=("Segoe UI", self.font_size_medium),
            fg="#cccccc",
            bg="#1a1a2e"
        )
        subtitle_label.pack(side="left", padx=(10, 0))
    
    def _create_controls(self, parent):
        """Crea los controles de filtrado y búsqueda"""
        controls_frame = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=1)
        controls_frame.pack(fill="x", pady=(0, 5))
        
        # Frame superior para filtros
        top_frame = tk.Frame(controls_frame, bg="#1a1a2e")
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Filtro por tipo de personal
        type_frame = tk.Frame(top_frame, bg="#1a1a2e")
        type_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            type_frame,
            text="Tipo de Personal:",
            font=("Segoe UI", self.font_size_medium, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side="left", padx=(0, 10))
        
        self.type_var = tk.StringVar(value="TODOS")
        self.type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            font=("Segoe UI", self.font_size_medium),
            state="readonly",
            width=15
        )
        self.type_combo.pack(side="left", padx=(0, 20))
        self.type_combo.bind("<<ComboboxSelected>>", self._on_type_changed)
        
        # Búsqueda
        search_frame = tk.Frame(top_frame, bg="#1a1a2e")
        search_frame.pack(side="right", fill="x", expand=True)
        
        tk.Label(
            search_frame,
            text="Buscar:",
            font=("Segoe UI", self.font_size_medium, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", self.font_size_medium),
            bg="#2a2a3e",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            bd=1
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)
        
        search_btn = tk.Button(
            search_frame,
            text="🔍",
            font=("Segoe UI", self.font_size_medium),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._perform_search
        )
        search_btn.pack(side="right")
        
        # Botón de verificar conexión del lector
        check_btn = tk.Button(
            search_frame,
            text="🔌",
            font=("Segoe UI", self.font_size_medium),
            fg="#ffffff",
            bg="#ff9800",
            activeforeground="#ffffff",
            activebackground="#f57c00",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._check_scanner_connection
        )
        check_btn.pack(side="right", padx=(0, 10))
    
    def _create_content_area(self, parent):
        """Crea el área de contenido con lista de personal"""
        content_frame = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=1)
        content_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Crear canvas y scrollbar para lista responsive
        canvas_frame = tk.Frame(content_frame, bg="#1a1a2e")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#1a1a2e",
            highlightthickness=0,
            relief="flat"
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame para el contenido scrolleable
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1a1a2e")
        
        # Configurar scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _create_footer(self, parent):
        """Crea el pie de la interfaz"""
        footer_frame = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=1)
        footer_frame.pack(fill="x")
        
        # Información de estado
        self.status_label = tk.Label(
            footer_frame,
            text="Listo para registrar huellas",
            font=("Segoe UI", self.font_size_small),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Contador de registros
        self.count_label = tk.Label(
            footer_frame,
            text="0 registros",
            font=("Segoe UI", self.font_size_small),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        self.count_label.pack(side="right", padx=10, pady=5)
    
    def _initialize_biometric_scanner(self):
        """Inicializa el lector biométrico"""
        try:
            print("🔌 Inicializando lector biométrico...")
            self._update_status("Conectando al lector biométrico...")
            
            # Intentar conectar en hilo separado para no bloquear la UI
            def connect_scanner():
                try:
                    print("🔌 Iniciando proceso de conexión...")
                    # Probar COM3 primero (como en main.py)
                    if biometric_scanner.test_com3_connection():
                        self.window.after(0, lambda: self._update_status("✅ Lector biométrico conectado en COM3"))
                        print("✅ Lector biométrico inicializado correctamente en COM3")
                    elif biometric_scanner.connect():
                        self.window.after(0, lambda: self._update_status("✅ Lector biométrico conectado"))
                        print("✅ Lector biométrico inicializado correctamente")
                    else:
                        self.window.after(0, lambda: self._update_status("⚠️ Lector biométrico no disponible"))
                        self.window.after(0, lambda: self._show_warning_alert(
                            "Advertencia", 
                            "Lector biométrico no disponible. Algunas funciones pueden estar limitadas.\n\n" +
                            "Posibles soluciones:\n" +
                            "• Verifique que el lector esté conectado por USB en COM3\n" +
                            "• Compruebe que el puerto COM3 esté disponible\n" +
                            "• Instale los drivers del lector\n" +
                            "• Asegúrese de que el lector esté encendido\n" +
                            "• Use el botón 🔌 para intentar reconectar"
                        ))
                        print("⚠️ Lector biométrico no pudo conectarse")
                except Exception as e:
                    error_msg = f"Error conectando lector: {e}"
                    print(f"❌ {error_msg}")
                    self.window.after(0, lambda: self._update_status("❌ Error conectando lector"))
                    self.window.after(0, lambda: self._show_error_alert("Error de Conexión", error_msg))
            
            thread = threading.Thread(target=connect_scanner, daemon=True)
            thread.start()
                
        except Exception as e:
            print(f"❌ Error inicializando lector biométrico: {e}")
            self._update_status("⚠️ Error inicializando lector biométrico")
    
    def _load_personal_data(self):
        """Carga los datos del personal desde la base de datos"""
        try:
            # Obtener tipos de personal
            personal_types = get_personal_types()
            type_names = ["TODOS"] + [pt["nombre"] for pt in personal_types]
            self.type_combo["values"] = type_names
            
            # Obtener personal
            self.personal_data = self._get_all_personal()
            self.filtered_data = self.personal_data.copy()
            
            # Actualizar interfaz
            self._update_personal_list()
            self._update_count()
            
            log_file("✅ Datos de personal cargados correctamente")
            
        except Exception as e:
            error_msg = f"Error cargando datos: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            self._show_error_alert("Error de Conexión", "Error de conexión a la base de datos")
    
    def _get_all_personal(self) -> List[Dict[str, Any]]:
        """Obtiene todos los personal desde la base de datos"""
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
    
    def _on_type_changed(self, event=None):
        """Maneja el cambio de tipo de personal"""
        self.current_personal_type = self.type_var.get()
        self._apply_filters()
    
    def _on_search_changed(self, event=None):
        """Maneja el cambio en el campo de búsqueda"""
        self.search_text = self.search_var.get().lower()
        self._apply_filters()
    
    def _perform_search(self):
        """Realiza la búsqueda"""
        self._apply_filters()
    
    def _apply_filters(self):
        """Aplica los filtros de tipo y búsqueda"""
        self.filtered_data = []
        
        for person in self.personal_data:
            # Filtro por tipo
            if self.current_personal_type != "TODOS":
                if person["tipo_personal_nombre"] != self.current_personal_type:
                    continue
            
            # Filtro por búsqueda
            if self.search_text:
                searchable_text = f"{person['nombres']} {person['apellidos']} {person['documento_numero']}".lower()
                if self.search_text not in searchable_text:
                    continue
            
            self.filtered_data.append(person)
        
        self._update_personal_list()
        self._update_count()
    
    def _update_personal_list(self):
        """Actualiza la lista de personal en la interfaz"""
        # Limpiar frame existente
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.filtered_data:
            # Mostrar mensaje de no hay datos
            no_data_label = tk.Label(
                self.scrollable_frame,
                text="No se encontraron registros",
                font=("Segoe UI", self.font_size_medium),
                fg="#888888",
                bg="#1a1a2e"
            )
            no_data_label.pack(pady=50)
            return
        
        # Crear tarjetas para cada persona
        for i, person in enumerate(self.filtered_data):
            self._create_person_card(person, i)
    
    def _create_person_card(self, person: Dict[str, Any], index: int):
        """Crea una tarjeta para una persona"""
        # Frame de la tarjeta
        card_frame = tk.Frame(
            self.scrollable_frame,
            bg="#2a2a3e",
            relief="flat",
            bd=1
        )
        card_frame.pack(fill="x", pady=2, padx=5)
        
        # Configurar hover
        def on_enter(e):
            card_frame.configure(bg="#3a3a4e")
        
        def on_leave(e):
            card_frame.configure(bg="#2a2a3e")
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
        # Frame interno
        inner_frame = tk.Frame(card_frame, bg="#2a2a3e")
        inner_frame.pack(fill="x", padx=10, pady=8)
        
        # Avatar/Inicial
        avatar_frame = tk.Frame(inner_frame, bg="#00ffff", width=40, height=40)
        avatar_frame.pack(side="left", padx=(0, 10))
        avatar_frame.pack_propagate(False)
        
        initial = person["nombres"][0].upper() if person["nombres"] else "?"
        avatar_label = tk.Label(
            avatar_frame,
            text=initial,
            font=("Segoe UI", self.font_size_large, "bold"),
            fg="#000000",
            bg="#00ffff"
        )
        avatar_label.pack(expand=True)
        
        # Información de la persona
        info_frame = tk.Frame(inner_frame, bg="#2a2a3e")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nombre
        name_label = tk.Label(
            info_frame,
            text=f"{person['nombres']} {person['apellidos']}",
            font=("Segoe UI", self.font_size_medium, "bold"),
            fg="#00ffff",
            bg="#2a2a3e",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # ID y tipo
        id_type_frame = tk.Frame(info_frame, bg="#2a2a3e")
        id_type_frame.pack(anchor="w", pady=(2, 0))
        
        id_label = tk.Label(
            id_type_frame,
            text=f"ID: {person['id']}",
            font=("Segoe UI", self.font_size_small),
            fg="#cccccc",
            bg="#2a2a3e"
        )
        id_label.pack(side="left")
        
        type_label = tk.Label(
            id_type_frame,
            text=f"• {person['tipo_personal_nombre']}",
            font=("Segoe UI", self.font_size_small),
            fg="#888888",
            bg="#2a2a3e"
        )
        type_label.pack(side="left", padx=(10, 0))
        
        # Estado de huella
        fingerprint_status = "✅ Registrada" if person["huella_digital"] else "❌ Sin registrar"
        status_color = "#4caf50" if person["huella_digital"] else "#ff6b6b"
        
        status_label = tk.Label(
            id_type_frame,
            text=fingerprint_status,
            font=("Segoe UI", self.font_size_small, "bold"),
            fg=status_color,
            bg="#2a2a3e"
        )
        status_label.pack(side="left", padx=(10, 0))
        
        # Botón de acción
        action_frame = tk.Frame(inner_frame, bg="#2a2a3e")
        action_frame.pack(side="right")
        
        if person["huella_digital"]:
            # Botón para re-registrar
            action_btn = tk.Button(
                action_frame,
                text="🔄 Actualizar",
                font=("Segoe UI", self.font_size_small, "bold"),
                fg="#ffffff",
                bg="#ffa726",
                activeforeground="#ffffff",
                activebackground="#ff9800",
                relief="flat",
                bd=0,
                padx=15,
                pady=5,
                cursor="hand2",
                command=lambda p=person: self._register_fingerprint(p)
            )
        else:
            # Botón para registrar
            action_btn = tk.Button(
                action_frame,
                text="👆 Registrar",
                font=("Segoe UI", self.font_size_small, "bold"),
                fg="#ffffff",
                bg="#4caf50",
                activeforeground="#ffffff",
                activebackground="#45a049",
                relief="flat",
                bd=0,
                padx=15,
                pady=5,
                cursor="hand2",
                command=lambda p=person: self._register_fingerprint(p)
            )
        
        action_btn.pack()
    
    def _register_fingerprint(self, person: Dict[str, Any]):
        """Inicia el proceso de registro de huella para una persona"""
        if self.scanning:
            self._show_warning_alert("Advertencia", "Ya hay un escaneo en progreso. Espere a que termine.")
            return
        
        # Determinar si es registro o actualización
        has_fingerprint = person.get('huella_digital') is not None
        action = "actualizar" if has_fingerprint else "registrar"
        
        # Mostrar confirmación
        result = messagebox.askyesno(
            f"Confirmar {action.title()}",
            f"¿Desea {action} la huella digital de:\n\n"
            f"{person['nombres']} {person['apellidos']}\n"
            f"ID: {person['id']}\n"
            f"Tipo: {person['tipo_personal_nombre']}\n\n"
            f"Coloque su dedo en el lector biométrico cuando esté listo."
        )
        
        if not result:
            return
        
        # Verificar conexión del lector
        if not biometric_scanner.connected:
            self._update_status("Conectando al lector biométrico...")
            if not biometric_scanner.connect():
                self._show_error_alert("Error de Conexión", "No se pudo conectar al lector biométrico.\n\nVerifique que el lector esté conectado y configurado correctamente.")
                return
        
        # Iniciar escaneo en hilo separado
        self.scanning = True
        self._update_status(f"Escaneando huella digital para {action}...")
        
        thread = threading.Thread(
            target=self._scan_fingerprint_thread,
            args=(person, action),
            daemon=True
        )
        thread.start()
    
    def _scan_fingerprint_thread(self, person: Dict[str, Any], action: str):
        """Hilo para escanear huella digital"""
        try:
            person_id = person["id"]
            person_name = f"{person['nombres']} {person['apellidos']}"
            
            # Usar el lector biométrico real
            if action == "registrar":
                success, message = biometric_scanner.register_fingerprint_for_person(person_id, person_name)
            else:  # actualizar
                success, message = biometric_scanner.update_fingerprint_for_person(person_id, person_name)
            
            if success:
                # Mostrar éxito
                self.window.after(0, lambda: self._show_success_alert("Registro Exitoso", message))
                
                # Actualizar lista
                self.window.after(0, self._load_personal_data)
                self.window.after(0, lambda: self._update_status(f"✅ {message}"))
                
                # Log del éxito
                log_file(f"✅ {message}")
            else:
                # Mostrar error
                self.window.after(0, lambda: self._show_error_alert("Error de Registro", message))
                self.window.after(0, lambda: self._update_status(f"❌ {message}"))
                
                # Log del error
                log_file(f"❌ {message}")
                
        except Exception as e:
            error_msg = f"Error en escaneo: {e}"
            print(f"❌ {error_msg}")
            log_file(f"❌ {error_msg}")
            
            self.window.after(0, lambda: self._show_error_alert("Error del Sistema", "Error en el sistema de escaneo"))
            self.window.after(0, lambda: self._update_status("❌ Error en el sistema"))
            
        finally:
            self.scanning = False
    
    
    def _update_status(self, message: str):
        """Actualiza el mensaje de estado"""
        self.status_label.configure(text=message)
    
    def _update_count(self):
        """Actualiza el contador de registros"""
        count = len(self.filtered_data)
        self.count_label.configure(text=f"{count} registros")
    
    def _show_error_alert(self, title: str, message: str):
        """Muestra una alerta de error específica para registro"""
        try:
            # Crear ventana de error personalizada
            error_window = tk.Toplevel(self.window)
            error_window.title(title)
            error_window.geometry("400x300")
            error_window.resizable(False, False)
            error_window.configure(bg="#0a0a0a")
            
            # Centrar ventana
            error_window.update_idletasks()
            x = (error_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (error_window.winfo_screenheight() // 2) - (300 // 2)
            error_window.geometry(f"400x300+{x}+{y}")
            
            # Hacer modal
            error_window.transient(self.window)
            error_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(error_window, bg="#1a1a2e", relief="flat", bd=2)
            main_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Frame de contenido
            content_frame = tk.Frame(main_frame, bg="#1a1a2e")
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Icono de error
            icon_label = tk.Label(
                content_frame,
                text="❌",
                font=("Segoe UI", 48),
                fg="#ff6b6b",
                bg="#1a1a2e"
            )
            icon_label.pack(pady=(20, 15))
            
            # Título
            title_label = tk.Label(
                content_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                fg="#ff6b6b",
                bg="#1a1a2e"
            )
            title_label.pack(pady=(0, 15))
            
            # Mensaje
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 12),
                fg="#ffffff",
                bg="#1a1a2e",
                wraplength=350,
                justify="center"
            )
            message_label.pack(pady=(0, 20))
            
            # Botón de cerrar
            close_btn = tk.Button(
                content_frame,
                text="ENTENDIDO",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff",
                bg="#ff6b6b",
                activeforeground="#ffffff",
                activebackground="#ff5252",
                relief="flat",
                bd=0,
                padx=30,
                pady=10,
                cursor="hand2",
                command=error_window.destroy
            )
            close_btn.pack()
            
        except Exception as e:
            print(f"❌ Error mostrando alerta: {e}")
            # Fallback a messagebox
            messagebox.showerror(title, message)
    
    def _show_warning_alert(self, title: str, message: str):
        """Muestra una alerta de advertencia específica para registro"""
        try:
            # Crear ventana de advertencia personalizada
            warning_window = tk.Toplevel(self.window)
            warning_window.title(title)
            warning_window.geometry("400x300")
            warning_window.resizable(False, False)
            warning_window.configure(bg="#0a0a0a")
            
            # Centrar ventana
            warning_window.update_idletasks()
            x = (warning_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (warning_window.winfo_screenheight() // 2) - (300 // 2)
            warning_window.geometry(f"400x300+{x}+{y}")
            
            # Hacer modal
            warning_window.transient(self.window)
            warning_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(warning_window, bg="#1a1a2e", relief="flat", bd=2)
            main_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Frame de contenido
            content_frame = tk.Frame(main_frame, bg="#1a1a2e")
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Icono de advertencia
            icon_label = tk.Label(
                content_frame,
                text="⚠️",
                font=("Segoe UI", 48),
                fg="#ffa726",
                bg="#1a1a2e"
            )
            icon_label.pack(pady=(20, 15))
            
            # Título
            title_label = tk.Label(
                content_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                fg="#ffa726",
                bg="#1a1a2e"
            )
            title_label.pack(pady=(0, 15))
            
            # Mensaje
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 12),
                fg="#ffffff",
                bg="#1a1a2e",
                wraplength=350,
                justify="center"
            )
            message_label.pack(pady=(0, 20))
            
            # Botón de cerrar
            close_btn = tk.Button(
                content_frame,
                text="ENTENDIDO",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff",
                bg="#ffa726",
                activeforeground="#ffffff",
                activebackground="#ff9800",
                relief="flat",
                bd=0,
                padx=30,
                pady=10,
                cursor="hand2",
                command=warning_window.destroy
            )
            close_btn.pack()
            
        except Exception as e:
            print(f"❌ Error mostrando alerta: {e}")
            # Fallback a messagebox
            messagebox.showwarning(title, message)
    
    def _show_success_alert(self, title: str, message: str):
        """Muestra una alerta de éxito específica para registro"""
        try:
            # Crear ventana de éxito personalizada
            success_window = tk.Toplevel(self.window)
            success_window.title(title)
            success_window.geometry("400x300")
            success_window.resizable(False, False)
            success_window.configure(bg="#0a0a0a")
            
            # Centrar ventana
            success_window.update_idletasks()
            x = (success_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (success_window.winfo_screenheight() // 2) - (300 // 2)
            success_window.geometry(f"400x300+{x}+{y}")
            
            # Hacer modal
            success_window.transient(self.window)
            success_window.grab_set()
            
            # Frame principal
            main_frame = tk.Frame(success_window, bg="#1a1a2e", relief="flat", bd=2)
            main_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Frame de contenido
            content_frame = tk.Frame(main_frame, bg="#1a1a2e")
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Icono de éxito
            icon_label = tk.Label(
                content_frame,
                text="✅",
                font=("Segoe UI", 48),
                fg="#4caf50",
                bg="#1a1a2e"
            )
            icon_label.pack(pady=(20, 15))
            
            # Título
            title_label = tk.Label(
                content_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                fg="#4caf50",
                bg="#1a1a2e"
            )
            title_label.pack(pady=(0, 15))
            
            # Mensaje
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 12),
                fg="#ffffff",
                bg="#1a1a2e",
                wraplength=350,
                justify="center"
            )
            message_label.pack(pady=(0, 20))
            
            # Botón de cerrar
            close_btn = tk.Button(
                content_frame,
                text="ENTENDIDO",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff",
                bg="#4caf50",
                activeforeground="#ffffff",
                activebackground="#45a049",
                relief="flat",
                bd=0,
                padx=30,
                pady=10,
                cursor="hand2",
                command=success_window.destroy
            )
            close_btn.pack()
            
        except Exception as e:
            print(f"❌ Error mostrando alerta: {e}")
            # Fallback a messagebox
            messagebox.showinfo(title, message)
    
    def _on_mousewheel(self, event):
        """Maneja el scroll del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _check_scanner_connection(self):
        """Verifica la conexión del lector biométrico en tiempo real"""
        try:
            self._update_status("🔌 Verificando conexión del lector...")
            
            if biometric_scanner.connected:
                self._update_status("✅ Lector biométrico conectado")
                self._show_success_alert("Conexión Exitosa", "El lector biométrico está conectado y listo para usar.")
            else:
                self._update_status("⚠️ Lector biométrico no disponible")
                # Intentar conectar específicamente en COM3 primero
                if biometric_scanner.test_com3_connection():
                    self._update_status("✅ Lector biométrico conectado en COM3")
                    self._show_success_alert("Conexión Exitosa", "El lector biométrico se ha conectado correctamente en COM3.")
                elif biometric_scanner.connect():
                    self._update_status("✅ Lector biométrico reconectado")
                    self._show_success_alert("Reconexión Exitosa", "El lector biométrico se ha reconectado correctamente.")
                else:
                    self._update_status("❌ No se pudo conectar al lector")
                    self._show_error_alert(
                        "Error de Conexión", 
                        "No se pudo conectar al lector biométrico.\n\n" +
                        "Verifique que:\n" +
                        "• El lector esté conectado por USB en COM3\n" +
                        "• El puerto COM3 esté disponible\n" +
                        "• Los drivers estén instalados\n" +
                        "• El lector esté encendido\n" +
                        "• No haya otros programas usando COM3"
                    )
        except Exception as e:
            print(f"❌ Error verificando conexión: {e}")
            self._update_status("❌ Error verificando conexión")
            self._show_error_alert("Error del Sistema", f"Error verificando conexión: {e}")
    
    def _on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.scanning:
            messagebox.showwarning("Escaneo en Progreso", "Hay un escaneo en progreso. Espere a que termine.")
            return
        
        # Limpiar lector biométrico
        try:
            biometric_scanner.disconnect()
        except:
            pass
        
        # Si hay una ventana padre, restaurarla
        if self.parent and hasattr(self.parent, 'deiconify'):
            try:
                self.parent.deiconify()
                self.parent.lift()
                self.parent.focus_force()
            except:
                pass
        
        # Destruir la ventana y limpiar la referencia
        self.window.destroy()
        self.window = None

# Función para mostrar la interfaz desde el sistema principal
def show_fingerprint_registration_interface(parent=None):
    """Muestra la interfaz de registro de huellas"""
    interface = FingerprintRegistrationInterface(parent)
    interface.show_fingerprint_registration()
    return interface
