#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleaning_interface.py
- Interfaz de aseo del sistema de dispensación biométrica
- Gestión de limpieza y mantenimiento del campus
"""

import tkinter as tk
from tkinter import messagebox
import styles
from config import *
from utils import *

class CleaningInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_cleaning_interface(self):
        """Muestra la interfaz de aseo con selección de ambientes de la base de datos"""
        # Crear ventana principal de aseo optimizada para 7 pulgadas
        cleaning_win = styles.create_modal_window(self.parent, "🧹 INTERFAZ DE ASEO - SISTEMA CEFA", "800x600")
        
        # Configurar para pantalla de 7 pulgadas
        cleaning_win.configure(bg="#0a0a0a")
        
        # Contenedor principal con padding optimizado
        main_container = tk.Frame(cleaning_win, bg="#0a0a0a")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header con título y efectos
        self._create_cleaning_header(main_container)
        
        # Contenedor de información principal
        info_container = tk.Frame(main_container, bg="#0a0a0a")
        info_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Selección de ambientes disponibles
        self._show_environment_selection(info_container)
        
        # Footer con botón de cerrar sesión
        self._create_cleaning_footer(main_container, cleaning_win)
        
        # Centrar la ventana
        styles.center_window(cleaning_win)

    def _create_cleaning_header(self, parent_container):
        """Crea el header futurista para la interfaz de aseo"""
        # Frame del header
        header_frame = tk.Frame(parent_container, bg="#0a0a0a")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal con efectos
        title_frame = tk.Frame(header_frame, bg="#0a0a0a")
        title_frame.pack(expand=True)
        
        # Icono de aseo
        cleaning_icon = tk.Label(
            title_frame,
            text="🧹",
            font=("Arial", 48, "bold"),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        cleaning_icon.pack()
        
        # Título principal
        welcome_label = tk.Label(
            title_frame,
            text="¡BIENVENIDO PERSONAL DE ASEO!",
            font=("Arial", 20, "bold"),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        welcome_label.pack(pady=(10, 0))
        
        # Línea decorativa
        line_frame = tk.Frame(header_frame, bg="#00ff88", height=2)
        line_frame.pack(fill="x", pady=(15, 0))
        
        # Efecto de brillo
        glow_frame = tk.Frame(header_frame, bg="#00ff88", height=1)
        glow_frame.pack(fill="x")
        glow_frame.configure(relief="raised", bd=1)

    def _show_environment_selection(self, parent_container):
        """Muestra la selección de ambientes disponibles de la base de datos"""
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
            text="SELECCIONAR AMBIENTE PARA LIMPIEZA",
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
            
            # Crear botones para cada ambiente
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
                
                # Botón del ambiente
                env_btn = tk.Button(
                    env_frame,
                    text=f"🏢 {nombre}",
                    font=("Arial", 12, "bold"),
                    bg="#00d4ff",
                    fg="#000000",
                    relief="raised",
                    bd=2,
                    padx=20,
                    pady=10,
                    command=lambda eid=env_id, n=nombre: self._select_environment(eid, n),
                    cursor="hand2"
                )
                env_btn.pack(side="left", padx=10, pady=10)
                
                # Información del ambiente
                info_text = f"📍 {ubicacion} | 🏗️ {tipo_ambiente} | 🏢 {edificio}"
                if piso:
                    info_text += f" | 🏢 Piso {piso}"
                
                info_label = tk.Label(
                    env_frame,
                    text=info_text,
                    font=("Arial", 10),
                    bg="#2a2a3e",
                    fg="#ffffff",
                    anchor="w"
                )
                info_label.pack(side="left", padx=(10, 0), fill="x", expand=True)
                
                # Efecto hover para el botón
                def on_enter(e, btn=env_btn):
                    btn.config(bg="#00ff88", relief="sunken")
                
                def on_leave(e, btn=env_btn):
                    btn.config(bg="#00d4ff", relief="raised")
                
                env_btn.bind("<Enter>", on_enter)
                env_btn.bind("<Leave>", on_leave)
            
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

    def _select_environment(self, environment_id, environment_name):
        """Maneja la selección de un ambiente específico"""
        messagebox.showinfo(
            "🧹 AMBIENTE SELECCIONADO",
            f"Ambiente seleccionado: {environment_name}\n\n"
            f"ID: {environment_id}\n\n"
            "El sistema está configurando la limpieza para este ambiente.\n"
            "Por favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la limpieza del ambiente seleccionado
        print(f"✅ Ambiente seleccionado: {environment_name} (ID: {environment_id})")

    def _create_cleaning_footer(self, parent_container, window):
        """Crea el footer futurista con botón de cerrar sesión"""
        # Frame del footer
        footer_frame = tk.Frame(parent_container, bg="#0a0a0a")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        # Línea decorativa superior
        line_frame = tk.Frame(footer_frame, bg="#00ff88", height=1)
        line_frame.pack(fill="x", pady=(0, 15))
        
        # Botón de cerrar sesión futurista
        logout_btn = tk.Button(
            footer_frame,
            text="🚪 CERRAR SESIÓN",
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
        logout_btn.pack()
        
        # Efecto de hover para el botón
        def on_enter(e):
            logout_btn.config(bg="#ff6666", relief="sunken")
        
        def on_leave(e):
            logout_btn.config(bg="#ff4444", relief="raised")
        
        logout_btn.bind("<Enter>", on_enter)
        logout_btn.bind("<Leave>", on_leave)

    def _show_cleaning_schedule(self, parent_window):
        """Muestra la programación de limpieza del campus"""
        # Crear ventana de programación de limpieza
        schedule_win = styles.create_modal_window(self.parent, "📅 PROGRAMACIÓN DE LIMPIEZA", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(schedule_win, "📅 PROGRAMACIÓN DE LIMPIEZA")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(schedule_win, "Horarios y áreas de limpieza del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(schedule_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Área de texto con scroll
        text_frame = styles.create_main_frame(main_frame)
        text_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        schedule_text = styles.create_text_widget(text_frame, height=20)
        
        schedule_scrollbar = styles.create_scrollbar(text_frame, orient="vertical", command=schedule_text.yview)
        schedule_text.configure(yscrollcommand=schedule_scrollbar.set)
        
        schedule_text.pack(side="left", fill="both", expand=True)
        schedule_scrollbar.pack(side="right", fill="y")
        
        # Contenido de la programación de limpieza
        cleaning_schedule_content = """
📅 PROGRAMACIÓN DE LIMPIEZA - SISTEMA CEFA

🕐 HORARIOS DE LIMPIEZA:

LUNES A VIERNES:
   • 5:00 AM - 7:00 AM: Limpieza general del campus
   • 8:00 AM - 9:00 AM: Limpieza de aulas y laboratorios
   • 12:00 PM - 1:00 PM: Limpieza de cafetería y áreas comunes
   • 3:00 PM - 4:00 PM: Limpieza de oficinas administrativas
   • 6:00 PM - 7:00 PM: Limpieza de pasillos y entradas
   • 9:00 PM - 11:00 PM: Limpieza final y desinfección

SÁBADOS:
   • 7:00 AM - 9:00 AM: Limpieza profunda de laboratorios
   • 10:00 AM - 12:00 PM: Limpieza de biblioteca
   • 2:00 PM - 4:00 PM: Limpieza de auditorio y salas

DOMINGOS:
   • 8:00 AM - 10:00 AM: Limpieza general del campus
   • 2:00 PM - 4:00 PM: Mantenimiento preventivo

🧹 ÁREAS DE RESPONSABILIDAD:

ZONA 1 - EDIFICIO PRINCIPAL:
   • Aulas 101-105
   • Pasillos principales
   • Recepción y lobby
   • Baños públicos

ZONA 2 - LABORATORIOS:
   • Laboratorios 201-205
   • Sala de equipos
   • Almacén de materiales
   • Área de trabajo

ZONA 3 - ÁREAS COMUNES:
   • Cafetería
   • Biblioteca
   • Auditorio
   • Salas de reunión

ZONA 4 - EXTERIORES:
   • Entrada principal
   • Estacionamiento
   • Jardines
   • Áreas deportivas

⚠️ NOTAS IMPORTANTES:
   • Usar equipos de protección personal
   • Seguir protocolos de desinfección
   • Reportar daños o problemas
   • Mantener registro de actividades
        """
        
        schedule_text.insert("1.0", cleaning_schedule_content)
        schedule_text.config(state="disabled")  # Solo lectura
        
        # Botón de cerrar
        close_btn = styles.create_accent_button(
            schedule_win, 
            "✅ CERRAR", 
            schedule_win.destroy
        )
        close_btn.pack(pady=20)
        
        # Centrar la ventana
        styles.center_window(schedule_win)

    def _show_maintenance_control(self, parent_window):
        """Muestra el control de mantenimiento del campus"""
        # Crear ventana de control de mantenimiento
        maintenance_win = styles.create_modal_window(self.parent, "🔧 CONTROL DE MANTENIMIENTO", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(maintenance_win, "🔧 CONTROL DE MANTENIMIENTO")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(maintenance_win, "Gestión de mantenimiento preventivo y correctivo")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal para el control de mantenimiento
        grid_container = styles.create_main_frame(maintenance_win)
        grid_container.pack(expand=True, padx=40, pady=20)
        
        # Configurar el grid 3x4
        for i in range(3):
            grid_container.grid_rowconfigure(i, weight=1)
        for i in range(4):
            grid_container.grid_columnconfigure(i, weight=1)
        
        # Lista de áreas de mantenimiento
        maintenance_areas = [
            "Sistema Eléctrico", "Sistema de Agua", "Aire Acondicionado", "Sistema de Seguridad",
            "Equipos de Limpieza", "Mobiliario", "Pintura y Decoración", "Jardinería",
            "Plomería", "Carpintería", "Herrería", "Albañilería"
        ]
        
        # Crear botones de áreas de mantenimiento con estilo futurista
        for i, maintenance_area in enumerate(maintenance_areas):
            row = i // 4
            col = i % 4
            
            maintenance_btn = styles.create_futuristic_button(
                grid_container, 
                maintenance_area, 
                lambda area=maintenance_area: self._control_maintenance_area(area),
                width=15, 
                height=2
            )
            
            # Aplicar efectos de hover
            styles.apply_button_hover_effects(maintenance_btn)
            maintenance_btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Botones de control
        control_frame = styles.create_main_frame(maintenance_win)
        control_frame.pack(fill="x", padx=40, pady=20)
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            maintenance_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(maintenance_win)

    def _show_cleaning_reports(self, parent_window):
        """Muestra los reportes de limpieza"""
        # Crear ventana de reportes de limpieza
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES DE LIMPIEZA", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES DE LIMPIEZA")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes de limpieza del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas de limpieza
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas de limpieza
        cleaning_stats_content = """
📊 ESTADÍSTICAS DE LIMPIEZA

🧹 ACTIVIDADES REALIZADAS:
   • Limpieza de aulas: 45/45 (100%)
   • Limpieza de laboratorios: 12/12 (100%)
   • Limpieza de oficinas: 25/25 (100%)
   • Limpieza de áreas comunes: 15/15 (100%)

⏱️ TIEMPO DE LIMPIEZA:
   • Tiempo promedio por aula: 15 min
   • Tiempo promedio por laboratorio: 25 min
   • Tiempo promedio por oficina: 10 min
   • Tiempo total diario: 8 horas

🔧 MANTENIMIENTO:
   • Equipos revisados: 18/18 (100%)
   • Reparaciones realizadas: 3
   • Mantenimiento preventivo: 5
   • Solicitudes pendientes: 0

👥 PERSONAL:
   • Personal activo: 8
   • Turnos completados: 12/12
   • Horas trabajadas: 96
   • Eficiencia promedio: 95%

📋 MATERIALES UTILIZADOS:
   • Productos de limpieza: 85%
   • Materiales de desinfección: 90%
   • Equipos de protección: 100%
   • Herramientas de mantenimiento: 100%

⚠️ INCIDENTES:
   • Incidentes reportados: 0
   • Problemas de equipos: 0
   • Quejas de usuarios: 0
   • Tiempo de respuesta: < 30 min
        """
        
        # Crear etiquetas para las estadísticas de limpieza
        stats_lines = cleaning_stats_content.strip().split('\n')
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
            lambda: self._export_cleaning_report()
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

    def _control_maintenance_area(self, maintenance_area):
        """Maneja el control de un área de mantenimiento específica"""
        messagebox.showinfo("🔧 CONTROL DE MANTENIMIENTO", 
                           f"Gestionando: {maintenance_area}\n\n"
                           "El sistema está configurando el control de mantenimiento para esta área.\n"
                           "Por favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el control de mantenimiento del área seleccionada

    def _export_cleaning_report(self):
        """Exporta el reporte de limpieza"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_limpieza_{timestamp}.csv"
            
            # Datos del reporte de limpieza
            report_data = [
                ['REPORTE DE LIMPIEZA - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS DE LIMPIEZA'],
                ['Limpieza de aulas', '45/45 (100%)'],
                ['Limpieza de laboratorios', '12/12 (100%)'],
                ['Limpieza de oficinas', '25/25 (100%)'],
                ['Limpieza de áreas comunes', '15/15 (100%)'],
                ['Tiempo total diario', '8 horas'],
                ['Personal activo', '8'],
                ['Turnos completados', '12/12'],
                ['Eficiencia promedio', '95%']
            ]
            
            if export_to_csv(report_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"El reporte de limpieza se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar el reporte de limpieza.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar el reporte de limpieza:\n\n{e}")
