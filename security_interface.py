#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_interface.py
- Interfaz de seguridad del sistema de dispensación biométrica
- Control de acceso y vigilancia del campus
"""

import tkinter as tk
from tkinter import messagebox
import styles
from config import *
from utils import *

class SecurityInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_security_interface(self):
        """Muestra la interfaz de seguridad"""
        # Crear ventana principal de seguridad
        security_win = styles.create_modal_window(self.parent, "🛡️ INTERFAZ DE SEGURIDAD - SISTEMA CEFA", ADMIN_WINDOW_SIZE)
        
        # Contenedor principal
        main_container = styles.create_main_frame(security_win)
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Título de bienvenida
        welcome_label = styles.create_title_label(main_container, "🛡️ INTERFAZ DE SEGURIDAD")
        welcome_label.pack(pady=(0, 40))
        
        # Contenedor para los botones
        buttons_container = styles.create_main_frame(main_container)
        buttons_container.pack(expand=True)
        
        # Botón: Monitoreo en Tiempo Real
        monitoring_btn = styles.create_futuristic_button(
            buttons_container, 
            "Monitoreo en Tiempo Real", 
            lambda: self._show_real_time_monitoring(security_win)
        )
        
        # Aplicar efectos de hover
        styles.apply_button_hover_effects(monitoring_btn)
        monitoring_btn.pack(pady=(0, 30))
        
        # Botón: Control de Acceso
        access_control_btn = styles.create_futuristic_button(
            buttons_container, 
            "Control de Acceso", 
            lambda: self._show_access_control(security_win)
        )
        
        # Aplicar efectos de hover
        styles.apply_button_hover_effects(access_control_btn)
        access_control_btn.pack(pady=(0, 30))
        
        # Botón: Reportes de Seguridad
        security_reports_btn = styles.create_futuristic_button(
            buttons_container, 
            "Reportes de Seguridad", 
            lambda: self._show_security_reports(security_win)
        )
        
        # Aplicar efectos de hover
        styles.apply_button_hover_effects(security_reports_btn)
        security_reports_btn.pack()
        
        # Botón de cerrar sesión
        logout_btn = styles.create_danger_button(
            main_container, 
            "🚪 CERRAR SESIÓN", 
            security_win.destroy
        )
        logout_btn.pack(side="bottom", pady=(20, 0))
        
        # Centrar la ventana
        styles.center_window(security_win)

    def _show_real_time_monitoring(self, parent_window):
        """Muestra el monitoreo en tiempo real del campus"""
        # Crear ventana de monitoreo
        monitoring_win = styles.create_modal_window(self.parent, "📹 MONITOREO EN TIEMPO REAL", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(monitoring_win, "📹 MONITOREO EN TIEMPO REAL")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(monitoring_win, "Estado actual del campus y cámaras de seguridad")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(monitoring_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para el estado del campus
        campus_status_frame = styles.create_main_frame(main_frame)
        campus_status_frame.pack(fill="x", padx=15, pady=15)
        
        # Estado del campus
        campus_status_content = """
🏫 ESTADO ACTUAL DEL CAMPUS

🟢 ZONAS SEGURAS:
   • Edificio Principal: Normal
   • Laboratorios: Normal
   • Biblioteca: Normal
   • Cafetería: Normal
   • Estacionamiento: Normal

📹 CÁMARAS ACTIVAS:
   • Entrada Principal: Funcionando
   • Recepción: Funcionando
   • Pasillos: Funcionando
   • Estacionamiento: Funcionando
   • Salidas de Emergencia: Funcionando

👥 PERSONAL EN CAMPUS:
   • Estudiantes: 245
   • Instructores: 18
   • Administrativos: 12
   • Seguridad: 8
   • Mantenimiento: 5

🚨 ALERTAS ACTIVAS:
   • Ninguna alerta activa
   • Sistema funcionando normalmente
   • Todas las áreas monitoreadas
        """
        
        # Crear etiquetas para el estado del campus
        status_lines = campus_status_content.strip().split('\n')
        for i, line in enumerate(status_lines):
            if line.strip():
                label = styles.create_info_label(campus_status_frame, line)
                label.pack(anchor="w", pady=2)
        
        # Botones de control
        control_frame = styles.create_main_frame(monitoring_win)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón para actualizar estado
        refresh_btn = styles.create_accent_button(
            control_frame, 
            "🔄 ACTUALIZAR", 
            lambda: self._refresh_campus_status()
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            monitoring_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(monitoring_win)

    def _show_access_control(self, parent_window):
        """Muestra el control de acceso con ambientes de la base de datos"""
        # Crear ventana de control de acceso optimizada para 7 pulgadas
        access_win = styles.create_modal_window(self.parent, "🚪 CONTROL DE ACCESO", "800x600")
        
        # Configurar para pantalla de 7 pulgadas
        access_win.configure(bg="#0a0a0a")
        
        # Contenedor principal con padding optimizado
        main_container = tk.Frame(access_win, bg="#0a0a0a")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header con título y efectos
        self._create_security_header(main_container)
        
        # Contenedor de información principal
        info_container = tk.Frame(main_container, bg="#0a0a0a")
        info_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Selección de ambientes para control de acceso
        self._show_access_environment_selection(info_container)
        
        # Footer con botón de cerrar
        self._create_security_footer(main_container, access_win)
        
        # Centrar la ventana
        styles.center_window(access_win)

    def _create_security_header(self, parent_container):
        """Crea el header futurista para la interfaz de seguridad"""
        # Frame del header
        header_frame = tk.Frame(parent_container, bg="#0a0a0a")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal con efectos
        title_frame = tk.Frame(header_frame, bg="#0a0a0a")
        title_frame.pack(expand=True)
        
        # Icono de seguridad
        security_icon = tk.Label(
            title_frame,
            text="🛡️",
            font=("Arial", 48, "bold"),
            bg="#0a0a0a",
            fg="#ff6b35"
        )
        security_icon.pack()
        
        # Título principal
        welcome_label = tk.Label(
            title_frame,
            text="CONTROL DE ACCESO",
            font=("Arial", 24, "bold"),
            bg="#0a0a0a",
            fg="#ff6b35"
        )
        welcome_label.pack(pady=(10, 0))
        
        # Subtítulo
        subtitle_label = tk.Label(
            title_frame,
            text="Gestión de entradas y salidas del campus",
            font=("Arial", 14),
            bg="#0a0a0a",
            fg="#ffffff"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Línea decorativa
        line_frame = tk.Frame(header_frame, bg="#ff6b35", height=2)
        line_frame.pack(fill="x", pady=(15, 0))
        
        # Efecto de brillo
        glow_frame = tk.Frame(header_frame, bg="#ff6b35", height=1)
        glow_frame.pack(fill="x")
        glow_frame.configure(relief="raised", bd=1)

    def _show_access_environment_selection(self, parent_container):
        """Muestra la selección de ambientes para control de acceso"""
        # Frame principal de selección
        selection_main_frame = tk.Frame(parent_container, bg="#0a0a0a")
        selection_main_frame.pack(fill="both", expand=True)
        
        # Título de selección
        selection_title_frame = tk.Frame(selection_main_frame, bg="#0a0a0a")
        selection_title_frame.pack(fill="x", pady=(0, 15))
        
        # Icono y título
        selection_icon = tk.Label(
            selection_title_frame,
            text="🏢",
            font=("Arial", 20),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        selection_icon.pack(side="left")
        
        selection_title = tk.Label(
            selection_title_frame,
            text="SELECCIONAR AMBIENTE PARA CONTROL DE ACCESO",
            font=("Arial", 16, "bold"),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        selection_title.pack(side="left", padx=(10, 0))
        
        # Frame de ambientes con borde futurista
        environments_frame = tk.Frame(
            selection_main_frame,
            bg="#1a1a2e",
            relief="raised",
            bd=2
        )
        environments_frame.pack(fill="both", expand=True)
        
        # Obtener ambientes de la base de datos
        environments = self._get_available_environments()
        
        if not environments:
            # Mostrar mensaje si no hay ambientes
            no_env_label = tk.Label(
                environments_frame,
                text="❌ No hay ambientes disponibles en la base de datos",
                font=("Arial", 14),
                bg="#1a1a2e",
                fg="#ff4444"
            )
            no_env_label.pack(expand=True)
        else:
            # Crear scrollable frame para los ambientes
            canvas = tk.Canvas(environments_frame, bg="#1a1a2e", highlightthickness=0)
            scrollbar = tk.Scrollbar(environments_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Crear botones para cada ambiente con opciones de entrada/salida
            for i, env in enumerate(environments):
                env_id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio = env
                
                # Frame para cada ambiente
                env_frame = tk.Frame(
                    scrollable_frame,
                    bg="#2a2a3e",
                    relief="raised",
                    bd=1
                )
                env_frame.pack(fill="x", padx=10, pady=5)
                
                # Información del ambiente
                info_text = f"🏢 {nombre} | 📍 {ubicacion} | 🏗️ {tipo_ambiente}"
                if piso:
                    info_text += f" | 🏢 Piso {piso}"
                
                info_label = tk.Label(
                    env_frame,
                    text=info_text,
                    font=("Arial", 12, "bold"),
                    bg="#2a2a3e",
                    fg="#ffffff",
                    anchor="w"
                )
                info_label.pack(fill="x", padx=10, pady=(10, 5))
                
                # Frame para botones de entrada y salida
                buttons_frame = tk.Frame(env_frame, bg="#2a2a3e")
                buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
                
                # Botón de entrada
                entry_btn = tk.Button(
                    buttons_frame,
                    text="🚪 ENTRADA",
                    font=("Arial", 10, "bold"),
                    bg="#00ff88",
                    fg="#000000",
                    relief="raised",
                    bd=2,
                    padx=15,
                    pady=8,
                    command=lambda eid=env_id, n=nombre: self._control_environment_access(eid, n, "ENTRADA"),
                    cursor="hand2"
                )
                entry_btn.pack(side="left", padx=(0, 10))
                
                # Botón de salida
                exit_btn = tk.Button(
                    buttons_frame,
                    text="🚪 SALIDA",
                    font=("Arial", 10, "bold"),
                    bg="#ff6b35",
                    fg="#ffffff",
                    relief="raised",
                    bd=2,
                    padx=15,
                    pady=8,
                    command=lambda eid=env_id, n=nombre: self._control_environment_access(eid, n, "SALIDA"),
                    cursor="hand2"
                )
                exit_btn.pack(side="left")
                
                # Efectos hover para los botones
                def on_enter_entry(e, btn=entry_btn):
                    btn.config(bg="#00ffaa", relief="sunken")
                
                def on_leave_entry(e, btn=entry_btn):
                    btn.config(bg="#00ff88", relief="raised")
                
                def on_enter_exit(e, btn=exit_btn):
                    btn.config(bg="#ff8c5a", relief="sunken")
                
                def on_leave_exit(e, btn=exit_btn):
                    btn.config(bg="#ff6b35", relief="raised")
                
                entry_btn.bind("<Enter>", on_enter_entry)
                entry_btn.bind("<Leave>", on_leave_entry)
                exit_btn.bind("<Enter>", on_enter_exit)
                exit_btn.bind("<Leave>", on_leave_exit)
            
            # Pack canvas y scrollbar
            canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")

    def _get_available_environments(self):
        """Obtiene los ambientes disponibles de la base de datos"""
        try:
            from utils import get_available_environments
            return get_available_environments()
        except Exception as e:
            print(f"❌ Error obteniendo ambientes: {e}")
            return []

    def _control_environment_access(self, environment_id, environment_name, access_type):
        """Maneja el control de acceso a un ambiente específico"""
        messagebox.showinfo(
            "🚪 CONTROL DE ACCESO",
            f"Ambiente: {environment_name}\n"
            f"Tipo: {access_type}\n"
            f"ID: {environment_id}\n\n"
            f"El sistema está configurando el control de {access_type.lower()} para este ambiente.\n"
            "Por favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el control de acceso al ambiente seleccionado
        print(f"✅ Control de {access_type} configurado para: {environment_name} (ID: {environment_id})")

    def _create_security_footer(self, parent_container, window):
        """Crea el footer futurista con botón de cerrar"""
        # Frame del footer
        footer_frame = tk.Frame(parent_container, bg="#0a0a0a")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        # Línea decorativa superior
        line_frame = tk.Frame(footer_frame, bg="#ff6b35", height=1)
        line_frame.pack(fill="x", pady=(0, 15))
        
        # Botón de cerrar futurista
        close_btn = tk.Button(
            footer_frame,
            text="❌ CERRAR",
            font=("Arial", 14, "bold"),
            bg="#ff4444",
            fg="#ffffff",
            relief="raised",
            bd=3,
            padx=30,
            pady=10,
            command=window.destroy,
            cursor="hand2"
        )
        close_btn.pack()
        
        # Efecto de hover para el botón
        def on_enter(e):
            close_btn.config(bg="#ff6666", relief="sunken")
        
        def on_leave(e):
            close_btn.config(bg="#ff4444", relief="raised")
        
        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)

    def _show_security_reports(self, parent_window):
        """Muestra los reportes de seguridad"""
        # Crear ventana de reportes de seguridad
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES DE SEGURIDAD", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES DE SEGURIDAD")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes de seguridad del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas de seguridad
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas de seguridad
        security_stats_content = """
📊 ESTADÍSTICAS DE SEGURIDAD

🚪 ACCESOS:
   • Total de accesos hoy: 1,247
   • Accesos autorizados: 1,245
   • Accesos denegados: 2
   • Tasa de éxito: 99.8%

👥 PERSONAS EN CAMPUS:
   • Máximo concurrente: 312
   • Promedio diario: 245
   • Personal autorizado: 43
   • Visitantes: 12

📹 CÁMARAS DE SEGURIDAD:
   • Total de cámaras: 24
   • Cámaras activas: 24
   • Cámaras en mantenimiento: 0
   • Tiempo de grabación: 24/7

🚨 INCIDENTES:
   • Incidentes reportados: 0
   • Alertas de seguridad: 0
   • Llamadas de emergencia: 0
   • Tiempo de respuesta: < 2 min

🛡️ MEDIDAS DE SEGURIDAD:
   • Control biométrico: Activo
   • Verificación de identidad: Activa
   • Monitoreo 24/7: Activo
   • Protocolos de emergencia: Actualizados
        """
        
        # Crear etiquetas para las estadísticas de seguridad
        stats_lines = security_stats_content.strip().split('\n')
        for i, line in enumerate(stats_lines):
            if line.strip():
                label = styles.create_info_label(stats_frame, line)
                label.pack(anchor="w", pady=2)
        
        # Botones de control
        control_frame = styles.create_main_frame(reports_win)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón para exportar reporte
        export_btn = styles.create_accent_button(
            control_frame, 
            "📊 EXPORTAR REPORTE", 
            lambda: self._export_security_report()
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            reports_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(reports_win)

    def _refresh_campus_status(self):
        """Actualiza el estado del campus"""
        messagebox.showinfo("🔄 ACTUALIZACIÓN", 
                           "Estado del campus actualizado.\n\n"
                           "Todas las áreas están siendo monitoreadas en tiempo real.")
        
        # Aquí se integraría con la lógica del sistema original
        # para actualizar el estado real del campus

    def _control_access_point(self, access_point):
        """Maneja el control de un punto de acceso específico"""
        messagebox.showinfo("🚪 CONTROL DE ACCESO", 
                           f"Gestionando: {access_point}\n\n"
                           "El sistema está configurando el control de acceso para este punto.\n"
                           "Por favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el control de acceso al punto seleccionado

    def _export_security_report(self):
        """Exporta el reporte de seguridad"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_seguridad_{timestamp}.csv"
            
            # Datos del reporte de seguridad
            report_data = [
                ['REPORTE DE SEGURIDAD - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS DE SEGURIDAD'],
                ['Total de accesos hoy', '1,247'],
                ['Accesos autorizados', '1,245'],
                ['Accesos denegados', '2'],
                ['Tasa de éxito', '99.8%'],
                ['Máximo concurrente', '312'],
                ['Total de cámaras', '24'],
                ['Cámaras activas', '24'],
                ['Incidentes reportados', '0']
            ]
            
            if export_to_csv(report_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"El reporte de seguridad se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar el reporte de seguridad.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar el reporte de seguridad:\n\n{e}")
