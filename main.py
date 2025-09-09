#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
- Archivo principal del sistema de dispensación biométrica
- Integra todas las interfaces y mantiene la funcionalidad original
"""

import json
import time
import threading
import os
from datetime import datetime
from typing import List, Tuple, Optional

import tkinter as tk
from tkinter import ttk, messagebox

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
from admin_interface import AdminInterface
from instructor_interface import InstructorInterface
from security_interface import SecurityInterface
from cleaning_interface import CleaningInterface
from administrative_interface import AdministrativeInterface
from schedule_interface import ScheduleInterface
from alert_system import alert_system
from desktop_alerts import desktop_alert_system
from role_validator import role_validator
from fingerprint_registration_interface import show_fingerprint_registration_interface

# ---------------------- UI PRINCIPAL ----------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA")
        self.geometry(MAIN_WINDOW_SIZE)
        self.minsize(*MAIN_WINDOW_MIN_SIZE)
        
        # Configurar tema oscuro futurista
        self.configure(bg=BG_DARK)

        # estado
        self.candidates: List[Tuple[int, str, List[int]]] = []
        self.best: Optional[Tuple[int, str, int]] = None  # (id, name, score)
        self.working = False
        self.worker: Optional[threading.Thread] = None
        self.fingerprint_modal = None  # Referencia al modal de escaneo de huella

        # Inicializar contadores y estadísticas
        self.operations_count = 0
        self.start_time = time.time()

        # Inicializar interfaces
        self.admin_interface = AdminInterface(self)
        self.instructor_interface = InstructorInterface(self)
        self.security_interface = SecurityInterface(self)
        self.cleaning_interface = CleaningInterface(self)
        self.administrative_interface = AdministrativeInterface(self)
        self.schedule_interface = ScheduleInterface(self)

        # Configurar estilos
        styles.setup_futuristic_styles(self)
        
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

    def _build_ui(self):
        # Configurar el fondo principal con el tema futurista
        self.configure(bg=BG_DARK)
        
        # Título principal futurista
        title_frame = tk.Frame(self, bg=BG_DARK, height=80)
        title_frame.pack(fill="x", padx=20, pady=(20,10))
        title_frame.pack_propagate(False)
        
        title_label = styles.create_title_label(title_frame, "🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA")
        title_label.pack(expand=True)
        
        subtitle_label = styles.create_subtitle_label(title_frame, "Control de Acceso por Huella Digital - CEFA")
        subtitle_label.pack()
        
        # Panel principal de botones - Cuadrícula 3x2 como en las imágenes
        buttons_frame = tk.Frame(self, bg=BG_DARK)
        buttons_frame.pack(expand=True, pady=20)
        
        # Configurar el grid para centrar los botones
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(2, weight=1)
        
        # Crear los 6 botones principales con el estilo de las imágenes
        button_configs = [
            ("ADMINISTRADOR", 0, 0, lambda: self._handle_biometric_access("admin")),
            ("INSTRUCTOR", 0, 1, lambda: self._handle_biometric_access("instructor")),
            ("SEGURIDAD", 1, 0, lambda: self._handle_biometric_access("security")),
            ("ASEO", 1, 1, lambda: self._handle_biometric_access("cleaning")),
            ("ADMINISTRATIVO", 2, 0, lambda: self._handle_biometric_access("administrative")),
            ("VER PROGRAMACIÓN", 2, 1, self._show_schedule_interface)
        ]
        
        # Crear los botones con el estilo futurista de las imágenes
        for text, row, col, command in button_configs:
            btn = styles.create_futuristic_button(buttons_frame, text, command)
            
            # Aplicar efectos de hover
            styles.apply_button_hover_effects(btn)
            
            btn.grid(row=row, column=col, padx=BUTTON_GRID_PADDING, pady=BUTTON_GRID_PADDING, sticky="nsew")
        
        # Panel de estado del sistema en la parte inferior
        status_frame = tk.Frame(self, bg=BG_DARK, height=120)
        status_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        status_frame.pack_propagate(False)
        
        # Estado del sistema
        self.var_status = tk.StringVar(value="🟢 SISTEMA LISTO Y OPERATIVO")
        status_label = styles.create_status_label(status_frame, "")
        status_label.configure(textvariable=self.var_status)
        status_label.pack(expand=True)
        
        # Información adicional del sistema
        info_label = styles.create_info_label(status_frame, "Sistema de Control de Acceso Biométrico - CEFA")
        info_label.pack()
        
        # Botón de recarga de candidatos (opcional)
        reload_frame = tk.Frame(status_frame, bg=BG_DARK)
        reload_frame.pack(pady=(5, 0))
        
        reload_btn = styles.create_small_button(
            reload_frame, 
            "🔄 RECARGAR CANDIDATOS", 
            self._manual_reload_candidates
        )
        reload_btn.pack(side="left", padx=(0, 10))
        
        # Botón de configuración de base de datos
        db_config_btn = styles.create_accent_button(
            reload_frame, 
            "⚙️ CONFIGURAR BD", 
            self._show_database_config
        )
        db_config_btn.pack(side="left")
        
        # Variables para el lector biométrico
        self.var_fp_port = tk.StringVar(value=FINGERPRINT_PORT_DEFAULT)
        self.var_fp_baud = tk.IntVar(value=FINGERPRINT_BAUD_DEFAULT)
        self.var_threshold = tk.IntVar(value=DEFAULT_THRESHOLD)
        self.var_topn = tk.IntVar(value=DEFAULT_TOPN)
        self.var_dwell = tk.IntVar(value=DEFAULT_DWELL)
        
        # Variable para rastrear la interfaz solicitada
        self.requested_interface = None

    def _handle_biometric_access(self, interface_type):
        """Maneja el acceso biométrico para diferentes tipos de interfaz"""
        self.requested_interface = interface_type
        self._show_fingerprint_modal()

    def _open_requested_interface(self):
        """Abre la interfaz solicitada después de la autenticación exitosa"""
        if not self.requested_interface:
            return
            
        print(f"🚪 Abriendo interfaz solicitada: {self.requested_interface}")
        
        # Mapear el tipo de interfaz a la función correspondiente
        interface_map = {
            "admin": self.admin_interface.show_admin_interface,
            "instructor": self.instructor_interface.show_instructor_interface,
            "security": self.security_interface.show_security_interface,
            "cleaning": self.cleaning_interface.show_cleaning_interface,
            "administrative": self.administrative_interface.show_administrative_interface
        }
        
        # Obtener y ejecutar la función de la interfaz
        interface_func = interface_map.get(self.requested_interface)
        if interface_func:
            # Cerrar la ventana de escaneo de huella
            self.after(0, self._close_fingerprint_scan_window)
            # Abrir la interfaz solicitada
            self.after(100, interface_func)
            # Limpiar la interfaz solicitada
            self.requested_interface = None
        else:
            print(f"⚠️ Tipo de interfaz no reconocido: {self.requested_interface}")
    
    def _close_fingerprint_scan_window(self):
        """Cierra solo el modal de escaneo de huella después del login exitoso"""
        try:
            print("🚪 Cerrando modal de escaneo de huella...")
            
            # Cerrar solo el modal de escaneo, no toda la aplicación
            if hasattr(self, 'fingerprint_modal') and self.fingerprint_modal:
                self.fingerprint_modal.destroy()
                self.fingerprint_modal = None
            
            # Log del cierre
            log_file("🚪 Modal de escaneo de huella cerrado después de login exitoso")
            
        except Exception as e:
            print(f"⚠️ Error cerrando modal de escaneo: {e}")
            log_file(f"⚠️ Error cerrando modal de escaneo: {e}")
    
    def _restore_main_window(self):
        """Restaura la ventana principal si es necesario"""
        try:
            print("🔄 Restaurando ventana principal...")
            self.deiconify()
            self.lift()
            self.focus_force()
            log_file("🔄 Ventana principal restaurada")
        except Exception as e:
            print(f"⚠️ Error restaurando ventana principal: {e}")
            log_file(f"⚠️ Error restaurando ventana principal: {e}")
    
    def _cancel_fingerprint_scan(self):
        """Cancela el escaneo de huella y cierra el modal"""
        try:
            print("❌ Cancelando escaneo de huella...")
            
            # Detener el worker si está ejecutándose
            if self.working and self.worker:
                self.working = False
                if self.worker.is_alive():
                    print("⏹️ Deteniendo worker de escaneo...")
            
            # Cerrar el modal
            if self.fingerprint_modal:
                self.fingerprint_modal.destroy()
                self.fingerprint_modal = None
            
            # Limpiar estado
            self.requested_interface = None
            
            log_file("❌ Escaneo de huella cancelado por el usuario")
            
        except Exception as e:
            print(f"⚠️ Error cancelando escaneo: {e}")
            log_file(f"⚠️ Error cancelando escaneo: {e}")

    def _auto_load_candidates(self):
        """Carga automáticamente los candidatos desde la base de datos sistema_llaves_v2"""
        try:
            print("🔄 Conectando a la base de datos sistema_llaves_v2...")
            
            # Intentar conectar a la base de datos real
            try:
                # Verificar conexión a MySQL
                mysql, err = _import_mysql()
                if not mysql:
                    raise Exception(f"MySQL no disponible: {err}")
                
                # Intentar conectar a la base de datos
                connection = mysql.connect(**DB_CONFIG)
                cursor = connection.cursor()
                
                # Verificar que la tabla personal existe
                cursor.execute("SHOW TABLES LIKE 'personal'")
                if not cursor.fetchone():
                    raise Exception("La tabla 'personal' no existe en la base de datos")
                
                # Contar registros en la tabla personal
                cursor.execute("SELECT COUNT(*) FROM personal WHERE activo = 1")
                total_people = cursor.fetchone()[0]
                print(f"📊 Total de personas en la base de datos: {total_people}")
                
                # Contar personas con huella digital
                cursor.execute("SELECT COUNT(*) FROM personal WHERE huella_digital IS NOT NULL AND activo = 1")
                biometric_people = cursor.fetchone()[0]
                print(f"🔐 Personas con huella digital: {biometric_people}")
                
                # Cargar candidatos reales desde la base de datos
                self.candidates = load_candidates_from_db()
                
                if self.candidates:
                    print(f"✅ {len(self.candidates)} candidatos cargados desde sistema_llaves_v2")
                    self._set_status(f"🟢 {len(self.candidates)} CANDIDATOS CARGADOS DESDE SISTEMA_LLAVES_V2 - SISTEMA LISTO")
                    
                    # Mostrar algunos candidatos para verificación
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
                
                # Si no se puede conectar a la BD, crear candidatos de ejemplo
                print("🔄 Creando candidatos de ejemplo para desarrollo...")
                self._create_sample_candidates()
                
        except Exception as e:
            print(f"❌ Error crítico cargando candidatos: {e}")
            self._set_status("🔴 ERROR CRÍTICO CARGANDO CANDIDATOS")
            self._create_sample_candidates()

    def _create_sample_candidates(self):
        """Crea candidatos de ejemplo para desarrollo y pruebas"""
        try:
            print("🔄 Creando candidatos de ejemplo...")
            
            # Usar candidatos de ejemplo desde config
            self.candidates = create_sample_candidates()
            
            print(f"✅ {len(self.candidates)} candidatos de ejemplo creados")
            self._set_status("🟡 CANDIDATOS DE EJEMPLO CARGADOS - MODO DESARROLLO")
            
        except Exception as e:
            print(f"❌ Error creando candidatos de ejemplo: {e}")
            self._set_status("🔴 ERROR CRÍTICO - SIN CANDIDATOS")
            self.candidates = []

    def _set_status(self, status):
        """Establece el estado del sistema"""
        if hasattr(self, 'var_status'):
            self.var_status.set(status)

    def _manual_reload_candidates(self):
        """Recarga manualmente los candidatos"""
        try:
            self._auto_load_candidates()
            messagebox.showinfo("✅ ÉXITO", "Candidatos recargados correctamente.")
        except Exception as e:
            messagebox.showerror("❌ ERROR", f"Error recargando candidatos:\n\n{e}")

    def _show_database_config(self):
        """Muestra la configuración de base de datos"""
        messagebox.showinfo("⚙️ CONFIGURACIÓN BD", 
                           f"Configuración actual de la base de datos:\n\n"
                           f"Host: {DB_CONFIG['host']}\n"
                           f"Usuario: {DB_CONFIG['user']}\n"
                           f"Base de datos: {DB_CONFIG['database']}\n\n"
                           "Para cambiar la configuración, edite el archivo config.py")

    # ============ INTERFACES DE USUARIOS ============
    
    def _show_admin_interface(self):
        """Muestra la interfaz de administrador"""
        self.admin_interface.show_admin_interface()

    def _show_instructor_interface(self):
        """Muestra la interfaz de instructor"""
        self.instructor_interface.show_instructor_interface()

    def _show_security_interface(self):
        """Muestra la interfaz de seguridad"""
        self.security_interface.show_security_interface()

    def _show_cleaning_interface(self):
        """Muestra la interfaz de aseo"""
        self.cleaning_interface.show_cleaning_interface()

    def _show_administrative_interface(self):
        """Muestra la interfaz administrativa"""
        self.administrative_interface.show_administrative_interface()

    def _show_schedule_interface(self):
        """Muestra la interfaz de programación"""
        self.schedule_interface.show_schedule_interface()
    

    # ============ FUNCIONALIDADES DEL SISTEMA ORIGINAL ============
    
    def _show_fingerprint_modal(self):
        """Muestra el modal de escaneo de huella como en las imágenes"""
        # Crear ventana modal
        self.fingerprint_modal = styles.create_modal_window(self, "Escaneo de Huella", MODAL_SIZE)
        modal = self.fingerprint_modal
        
        # Contenedor principal del modal
        main_container = styles.create_main_frame(modal)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título del modal
        title_label = styles.create_title_label(main_container, "Escanea huella")
        title_label.configure(font=FONT_BUTTON_SMALL)
        title_label.pack(pady=(0, 30))
        
        # Contenedor del icono de huella con efectos de luz
        fingerprint_frame = tk.Frame(main_container, bg=BG_DARK, width=200, height=200)
        fingerprint_frame.pack(expand=True)
        fingerprint_frame.pack_propagate(False)
        
        # Crear el icono de huella estilizado
        canvas = tk.Canvas(fingerprint_frame, bg=BG_DARK, highlightthickness=0, 
                          width=200, height=200)
        canvas.pack(expand=True)
        
        # Dibujar el icono de huella con estilo futurista
        self._draw_fingerprint_icon(canvas)
        
        # Botones de control del modal
        buttons_frame = styles.create_main_frame(main_container)
        buttons_frame.pack(fill="x", pady=(30, 0))
        
        # Botón de escanear
        scan_btn = styles.create_accent_button(
            buttons_frame, 
            "🔍 ESCANEAR HUELLA", 
            self._start_fingerprint_scan
        )
        scan_btn.pack(side="left", padx=(0, 10))
        
        # Botón de cancelar
        cancel_btn = styles.create_danger_button(
            buttons_frame, 
            "❌ CANCELAR", 
            lambda: self._cancel_fingerprint_scan()
        )
        cancel_btn.pack(side="right")
        
        # Iniciar la animación de escaneo
        self._animate_fingerprint_scan(canvas)

    def _draw_fingerprint_icon(self, canvas):
        """Dibuja el icono de huella con estilo futurista"""
        # Limpiar el canvas
        canvas.delete("all")
        
        # Dimensiones del canvas
        width = canvas.winfo_reqwidth()
        height = canvas.winfo_reqheight()
        center_x = width // 2
        center_y = height // 2
        
        # Dibujar el contorno de la huella
        canvas.create_oval(center_x - 60, center_y - 80, center_x + 60, center_y + 80,
                          outline=ACCENT_CYAN, width=3, fill=BG_MEDIUM)
        
        # Dibujar líneas de la huella (simulando crestas)
        for i in range(-40, 41, 8):
            y = center_y + i
            if abs(i) < 60:  # Solo dentro del óvalo
                # Líneas curvas simulando crestas de huella
                start_x = center_x - int(30 * (1 - abs(i) / 60))
                end_x = center_x + int(30 * (1 - abs(i) / 60))
                canvas.create_line(start_x, y, end_x, y, fill=ACCENT_CYAN, width=2)
        
        # Agregar puntos de referencia
        canvas.create_oval(center_x - 3, center_y - 3, center_x + 3, center_y + 3,
                          fill=ACCENT_BLUE, outline=ACCENT_CYAN)
        
        # Agregar el marco L-shaped en las esquinas
        corner_size = 15
        corners = [
            (center_x - 70, center_y - 90),  # Top-left
            (center_x + 55, center_y - 90),  # Top-right
            (center_x - 70, center_y + 75),  # Bottom-left
            (center_x + 55, center_y + 75)   # Bottom-right
        ]
        
        for x, y in corners:
            # L-shaped brackets
            canvas.create_line(x, y, x + corner_size, y, fill=ACCENT_BLUE, width=2)
            canvas.create_line(x, y, x, y + corner_size, fill=ACCENT_BLUE, width=2)

    def _animate_fingerprint_scan(self, canvas):
        """Anima el escaneo de huella con líneas de luz"""
        def animate_scan():
            # Limpiar líneas de escaneo anteriores
            canvas.delete("scan_lines")
            
            # Crear líneas de escaneo animadas
            for i in range(-80, 81, 20):
                y = 100 + i
                # Líneas de escaneo con efecto de luz
                canvas.create_line(50, y, 150, y, fill=ACCENT_BLUE, width=2, 
                                 tags="scan_lines", stipple="gray50")
            
            # Efecto de parpadeo
            canvas.after(500, lambda: canvas.delete("scan_lines"))
            canvas.after(1000, animate_scan)
        
        animate_scan()

    def _start_fingerprint_scan(self):
        """Inicia el proceso real de escaneo de huella con el lector biométrico físico"""
        # Verificar que haya candidatos cargados
        if not hasattr(self, 'candidates') or not self.candidates:
            messagebox.showerror("❌ ERROR", "No hay candidatos cargados en el sistema.\n\n"
                               "Por favor, recargue los candidatos desde la base de datos.")
            return
        
        # Verificar que el lector biométrico esté disponible
        try:
            fp_mod, err = _import_pyfingerprint()
            if not fp_mod:
                messagebox.showerror("❌ ERROR", f"Lector biométrico no disponible: {err}\n\n"
                                   "Instale pyfingerprint para usar esta funcionalidad.")
                return
        except Exception as e:
            messagebox.showerror("❌ ERROR", f"Error verificando lector biométrico: {e}")
            return
        
        # Iniciar el proceso real de escaneo
        self._start_real_fingerprint_scan()

    def _start_real_fingerprint_scan(self):
        """Inicia el escaneo real de huella con el lector biométrico físico"""
        # Verificar que haya candidatos reales de la base de datos
        if not self.candidates:
            messagebox.showerror("❌ ERROR", "No hay candidatos cargados desde la base de datos SICEFA.\n\n"
                               "Verifique la conexión a la base de datos.")
            return
        
        # Mostrar instrucciones claras para el usuario
        messagebox.showinfo("🔍 ESCANEO REAL INICIADO", 
                           "INSTRUCCIONES PARA ESCANEO DE HUELLA:\n\n"
                           "1️⃣ Coloque su dedo en el lector biométrico físico\n"
                           "2️⃣ Mantenga el dedo en el sensor hasta que se complete la captura\n"
                           "3️⃣ El sistema validará su huella contra la base de datos SICEFA\n"
                           "4️⃣ Si es administrador, tendrá acceso completo\n\n"
                           "⚠️ IMPORTANTE: Asegúrese de que el lector esté conectado al puerto " + 
                           self.var_fp_port.get())
        
        # Iniciar el proceso en un hilo separado para no bloquear la UI
        self.working = True
        self._set_status("🔍 ESCANEANDO HUELLA DIGITAL - Coloque su dedo en el sensor físico...")
        
        # Mostrar información del lector biométrico
        print(f"🔐 Configuración del lector biométrico:")
        print(f"   Puerto: {self.var_fp_port.get()}")
        print(f"   Baud Rate: {self.var_fp_baud.get()}")
        print(f"   Candidatos disponibles: {len(self.candidates)}")
        
        # Iniciar el worker en un hilo separado
        self.worker = threading.Thread(target=self._real_fingerprint_worker, daemon=True)
        self.worker.start()

    def _real_fingerprint_worker(self):
        """Worker que ejecuta el escaneo real de huella"""
        try:
            print("🚀 INICIANDO ESCANEO REAL DE HUELLA...")
            
            # Imports necesarios para el lector biométrico
            fp_mod, err = _import_pyfingerprint()
            if not fp_mod:
                self._end_error(f"Lector biométrico no disponible: {err}")
                return
            
            PyFingerprint, F1, F2 = fp_mod
            
            # 1) Abrir el sensor físico
            print(f"🔌 Conectando al lector biométrico en puerto {self.var_fp_port.get()}...")
            self.after(0, lambda: self._set_status("🔌 CONECTANDO AL LECTOR BIOMÉTRICO..."))
            
            try:
                sensor = PyFingerprint(self.var_fp_port.get().strip(), int(self.var_fp_baud.get()),
                                       0xFFFFFFFF, 0x00000000)
                
                print("✅ Lector biométrico conectado, verificando contraseña...")
                
                if not sensor.verifyPassword():
                    self._end_error("Contraseña del sensor incorrecta")
                    return
                
                print("✅ Contraseña del sensor verificada correctamente")
                self.after(0, lambda: self._set_status("✅ SENSOR CONECTADO - Coloque su dedo en el lector..."))
                self.after(0, lambda: log_file("✅ Sensor biométrico conectado y verificado"))
                
            except Exception as e:
                error_msg = f"Error conectando al lector biométrico: {e}"
                print(f"❌ {error_msg}")
                self._end_error(f"Error conectando al lector biométrico: {e}")
                return
            
            # 2) Capturar huella real
            print("📱 Iniciando captura de huella digital...")
            self.after(0, lambda: self._set_status("📱 CAPTURANDO HUELLA - Mantenga el dedo en el sensor..."))
            self.after(0, lambda: log_file("📱 Iniciando captura de huella digital..."))
            
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
            
            # 3) Convertir imagen capturada
            print("🔄 Convirtiendo imagen capturada...")
            try:
                sensor.convertImage(F1)
                print("✅ Imagen convertida correctamente")
                self.after(0, lambda: log_file("✅ Huella capturada y convertida correctamente"))
            except Exception as e:
                self._end_error(f"No se pudo convertir la imagen capturada: {e}")
                return
            
            # 4) Comparar con candidatos en la base de datos SICEFA
            print(f"🔍 Comparando huella con {len(self.candidates)} candidatos de SICEFA...")
            self.after(0, lambda: self._set_status("🔍 COMPARANDO HUELLA CON BASE DE DATOS SICEFA..."))
            self.after(0, lambda: log_file("🔍 Comparando huella capturada con candidatos de SICEFA..."))
            
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
                        self.after(0, lambda: log_file(f"Plantilla corrupta para {name or pid}: {ex}"))
                
                scored.sort(key=lambda x: x[2], reverse=True)
                best = scored[0] if scored else None
                
                print(f"🏆 Mejor puntuación: {best[2] if best else 'N/A'}")
                
                # Aquí se procesarían los resultados
                # self.after(0, lambda: self._update_scores, scored[:topn], best, threshold)
                
            except Exception as e:
                self._end_error(f"Error al comparar huella: {e}")
                return
            
            # 5) Si hay ganador sobre umbral, verificar rol específico
            if best and best[2] >= threshold:
                pid, name, score = best
                print(f"🎉 IDENTIFICACIÓN EXITOSA: {name} (ID: {pid}) con puntuación {score}")
                self.after(0, lambda: log_file(f"✅ Identificación exitosa: {name} (ID: {pid}) con puntuación {score}"))
                
                # Verificar si el usuario tiene acceso al rol solicitado
                if self.requested_interface:
                    has_access, user_name, user_role = role_validator.validate_role_access(pid, self.requested_interface)
                    
                    if has_access:
                        print(f"🔐 Usuario {name} tiene acceso al rol {self.requested_interface}")
                        self.after(0, lambda: self._set_status(f"🔐 {user_role.upper()} IDENTIFICADO - Acceso concedido"))
                        self.after(0, lambda: log_file(f"🔐 Acceso de {user_role} concedido"))
                        
                        # Mostrar alerta de acceso concedido
                        self.after(0, lambda: desktop_alert_system.show_access_granted_alert(self.requested_interface, user_name))
                        
                        # Abrir la interfaz solicitada después de un breve delay
                        self.after(2000, self._open_requested_interface)
                    else:
                        print(f"❌ Usuario {name} no tiene acceso al rol {self.requested_interface}")
                        self.after(0, lambda: self._set_status(f"❌ ACCESO DENEGADO - Rol incorrecto"))
                        self.after(0, lambda: log_file(f"❌ Acceso denegado: {name} no es {self.requested_interface}"))
                        
                        # Mostrar alerta de acceso denegado
                        self.after(0, lambda: desktop_alert_system.show_access_denied_alert(self.requested_interface, user_name))
                else:
                    # Si no hay interfaz solicitada, usar lógica antigua
                    if is_administrator(pid, name):
                        print("🔐 Usuario identificado como ADMINISTRADOR")
                        self.after(0, lambda: self._set_status("🔐 ADMINISTRADOR IDENTIFICADO - Acceso concedido"))
                        self.after(0, lambda: log_file("🔐 Acceso de administrador concedido"))
                        
                        # Cerrar ventana de escaneo y abrir interfaz de administrador
                        self.after(0, self._close_fingerprint_scan_window)
                        self.after(100, self.admin_interface.show_admin_interface)
                    else:
                        print("👤 Usuario identificado con acceso limitado")
                        self.after(0, lambda: self._set_status("👤 USUARIO IDENTIFICADO - Acceso limitado"))
                        self.after(0, lambda: log_file(f"👤 Usuario {name} identificado - Acceso limitado"))
                        # Cerrar ventana de escaneo y mostrar interfaz de usuario
                        self.after(0, self._close_fingerprint_scan_window)
                        self.after(100, lambda: self._show_user_access_interface(name, pid))
                    
            else:
                print(f"❌ Sin coincidencias válidas. Mejor puntuación: {best[2] if best else 'N/A'} (umbral: {threshold})")
                self.after(0, lambda: self._set_status("❌ HUELLA NO RECONOCIDA"))
                self.after(0, lambda: log_file("❌ Huella no reconocida en el sistema"))
                
                # Mostrar alerta de huella no encontrada
                self.after(0, lambda: desktop_alert_system.show_fingerprint_not_found_alert())
                return
                
        except Exception as e:
            print(f"❌ Error crítico en el escaneo de huella: {e}")
            self._end_error(f"Error crítico en el escaneo de huella: {e}")
        finally:
            self.working = False
            print("🏁 Proceso de escaneo finalizado")

    def _show_user_access_interface(self, name: str, pid: int):
        """Muestra interfaz para usuarios no administradores"""
        messagebox.showinfo("👤 ACCESO DE USUARIO", 
                           f"Usuario identificado: {name}\nID: {pid}\n\n"
                           "Acceso limitado concedido.\n"
                           "Contacte al administrador para permisos adicionales.")
    
    def cleanup(self):
        """Limpia recursos al cerrar la aplicación"""
        try:
            alert_system.cleanup()
            desktop_alert_system.cleanup()
        except Exception as e:
            print(f"⚠️ Error en limpieza: {e}")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        try:
            self.cleanup()
            self.destroy()
        except Exception as e:
            print(f"⚠️ Error al cerrar: {e}")
            self.destroy()

    def _end_error(self, msg: str):
        """Maneja errores en el escaneo de huella"""
        error_msg = f"❌ ERROR EN ESCANEO DE HUELLA: {msg}"
        self.after(0, lambda: log_file(error_msg))
        self.after(0, lambda: self._set_status("🔴 ERROR EN ESCANEO DE HUELLA"))
        self.after(0, lambda: messagebox.showerror("🚨 ERROR", f"Error en el escaneo de huella:\n\n{msg}"))
        self.working = False

    def _end_info(self, msg: str):
        """Maneja información del escaneo de huella"""
        info_msg = f"ℹ️ INFORMACIÓN: {msg}"
        self.after(0, lambda: log_file(info_msg))
        self.after(0, lambda: self._set_status("ℹ️ INFORMACIÓN PROCESADA"))
        self.after(0, lambda: messagebox.showinfo("ℹ️ INFORMACIÓN", f"Información del sistema:\n\n{msg}"))
        self.working = False

# ============ FUNCIÓN PRINCIPAL ============
def main():
    """Función principal del sistema"""
    try:
        # Crear y ejecutar la aplicación principal
        app = App()
        
        # Configurar manejador de cierre
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        app.mainloop()
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO en la aplicación principal: {e}")
        log_file(f"❌ ERROR CRÍTICO en la aplicación principal: {e}")
        
        # Mostrar mensaje de error al usuario
        try:
            import tkinter.messagebox as msgbox
            msgbox.showerror("🚨 ERROR CRÍTICO", 
                           f"Error crítico en la aplicación:\n\n{e}\n\n"
                           "La aplicación se cerrará.")
        except:
            pass

if __name__ == "__main__":
    main()
