#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
administrative_interface.py
- Interfaz de administrativo del sistema de dispensación biométrica
- Gestión administrativa del campus
"""

import tkinter as tk
from tkinter import messagebox
import styles
from config import *
from utils import *

class AdministrativeInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_administrative_interface(self):
        """Muestra la interfaz de administrativo con ambientes asignados"""
        # Crear ventana principal de administrativo optimizada para 7 pulgadas
        admin_win = styles.create_modal_window(self.parent, "📋 INTERFAZ ADMINISTRATIVA - SISTEMA CEFA", "800x600")
        
        # Configurar para pantalla de 7 pulgadas
        admin_win.configure(bg="#0a0a0a")
        
        # Contenedor principal con padding optimizado
        main_container = tk.Frame(admin_win, bg="#0a0a0a")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header con título y efectos
        self._create_administrative_header(main_container)
        
        # Contenedor de información principal
        info_container = tk.Frame(main_container, bg="#0a0a0a")
        info_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Mostrar ambientes asignados
        self._show_assigned_environments(info_container)
        
        # Footer con botón de cerrar sesión
        self._create_administrative_footer(main_container, admin_win)
        
        # Centrar la ventana
        styles.center_window(admin_win)

    def _create_administrative_header(self, parent_container):
        """Crea el header futurista para la interfaz administrativa"""
        # Frame del header
        header_frame = tk.Frame(parent_container, bg="#0a0a0a")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal con efectos
        title_frame = tk.Frame(header_frame, bg="#0a0a0a")
        title_frame.pack(expand=True)
        
        # Icono administrativo
        admin_icon = tk.Label(
            title_frame,
            text="📋",
            font=("Arial", 48, "bold"),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        admin_icon.pack()
        
        # Título principal
        welcome_label = tk.Label(
            title_frame,
            text="¡BIENVENIDO PERSONAL ADMINISTRATIVO!",
            font=("Arial", 20, "bold"),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        welcome_label.pack(pady=(10, 0))
        
        # Línea decorativa
        line_frame = tk.Frame(header_frame, bg="#00d4ff", height=2)
        line_frame.pack(fill="x", pady=(15, 0))
        
        # Efecto de brillo
        glow_frame = tk.Frame(header_frame, bg="#00d4ff", height=1)
        glow_frame.pack(fill="x")
        glow_frame.configure(relief="raised", bd=1)

    def _show_assigned_environments(self, parent_container):
        """Muestra los ambientes asignados al personal administrativo"""
        # Frame principal de ambientes
        environments_main_frame = tk.Frame(parent_container, bg="#0a0a0a")
        environments_main_frame.pack(fill="both", expand=True)
        
        # Título de ambientes
        environments_title_frame = tk.Frame(environments_main_frame, bg="#0a0a0a")
        environments_title_frame.pack(fill="x", pady=(0, 15))
        
        # Icono y título
        environments_icon = tk.Label(
            environments_title_frame,
            text="🏢",
            font=("Arial", 20),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        environments_icon.pack(side="left")
        
        environments_title = tk.Label(
            environments_title_frame,
            text="AMBIENTES ASIGNADOS",
            font=("Arial", 16, "bold"),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        environments_title.pack(side="left", padx=(10, 0))
        
        # Frame de ambientes con borde futurista
        environments_frame = tk.Frame(
            environments_main_frame,
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
                text="❌ No hay ambientes asignados en la base de datos",
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
            
            # Crear tarjetas para cada ambiente asignado
            for i, env in enumerate(environments):
                env_id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio = env
                
                # Frame para cada ambiente
                env_frame = tk.Frame(
                    scrollable_frame,
                    bg="#2a2a3e",
                    relief="raised",
                    bd=1
                )
                env_frame.pack(fill="x", padx=10, pady=8)
                
                # Header del ambiente
                env_header_frame = tk.Frame(env_frame, bg="#2a2a3e")
                env_header_frame.pack(fill="x", padx=15, pady=(15, 5))
                
                # Nombre del ambiente
                env_name_label = tk.Label(
                    env_header_frame,
                    text=f"🏢 {nombre}",
                    font=("Arial", 14, "bold"),
                    bg="#2a2a3e",
                    fg="#00d4ff",
                    anchor="w"
                )
                env_name_label.pack(side="left")
                
                # Tipo de ambiente
                env_type_label = tk.Label(
                    env_header_frame,
                    text=f"🏗️ {tipo_ambiente}",
                    font=("Arial", 12),
                    bg="#2a2a3e",
                    fg="#00ff88",
                    anchor="e"
                )
                env_type_label.pack(side="right")
                
                # Información detallada del ambiente
                info_frame = tk.Frame(env_frame, bg="#2a2a3e")
                info_frame.pack(fill="x", padx=15, pady=(0, 10))
                
                # Ubicación
                location_label = tk.Label(
                    info_frame,
                    text=f"📍 Ubicación: {ubicacion}",
                    font=("Arial", 11),
                    bg="#2a2a3e",
                    fg="#ffffff",
                    anchor="w"
                )
                location_label.pack(anchor="w")
                
                # Edificio y piso
                building_text = f"🏢 Edificio: {edificio}" if edificio else "🏢 Edificio: No especificado"
                if piso:
                    building_text += f" | Piso: {piso}"
                
                building_label = tk.Label(
                    info_frame,
                    text=building_text,
                    font=("Arial", 11),
                    bg="#2a2a3e",
                    fg="#ffffff",
                    anchor="w"
                )
                building_label.pack(anchor="w")
                
                # Descripción si existe
                if descripcion:
                    desc_label = tk.Label(
                        info_frame,
                        text=f"📝 {descripcion}",
                        font=("Arial", 10),
                        bg="#2a2a3e",
                        fg="#cccccc",
                        anchor="w",
                        wraplength=600
                    )
                    desc_label.pack(anchor="w", pady=(5, 0))
                
                # Botón de acceso al ambiente
                access_btn = tk.Button(
                    env_frame,
                    text="🚪 ACCEDER AL AMBIENTE",
                    font=("Arial", 11, "bold"),
                    bg="#00d4ff",
                    fg="#000000",
                    relief="raised",
                    bd=2,
                    padx=20,
                    pady=8,
                    command=lambda eid=env_id, n=nombre: self._access_environment(eid, n),
                    cursor="hand2"
                )
                access_btn.pack(pady=(0, 15), padx=15)
                
                # Efecto hover para el botón
                def on_enter(e, btn=access_btn):
                    btn.config(bg="#00ff88", relief="sunken")
                
                def on_leave(e, btn=access_btn):
                    btn.config(bg="#00d4ff", relief="raised")
                
                access_btn.bind("<Enter>", on_enter)
                access_btn.bind("<Leave>", on_leave)
            
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

    def _access_environment(self, environment_id, environment_name):
        """Maneja el acceso a un ambiente específico"""
        messagebox.showinfo(
            "🚪 ACCESO AL AMBIENTE",
            f"Ambiente: {environment_name}\n"
            f"ID: {environment_id}\n\n"
            "El sistema está configurando el acceso administrativo para este ambiente.\n"
            "Por favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el acceso administrativo al ambiente seleccionado
        print(f"✅ Acceso administrativo configurado para: {environment_name} (ID: {environment_id})")

    def _create_administrative_footer(self, parent_container, window):
        """Crea el footer futurista con botón de cerrar sesión"""
        # Frame del footer
        footer_frame = tk.Frame(parent_container, bg="#0a0a0a")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        # Línea decorativa superior
        line_frame = tk.Frame(footer_frame, bg="#00d4ff", height=1)
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

    def _show_personnel_management(self, parent_window):
        """Muestra la gestión de personal"""
        # Crear ventana de gestión de personal
        personnel_win = styles.create_modal_window(self.parent, "👥 GESTIÓN DE PERSONAL", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(personnel_win, "👥 GESTIÓN DE PERSONAL")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(personnel_win, "Administración del personal del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(personnel_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para información del personal
        personnel_frame = styles.create_main_frame(main_frame)
        personnel_frame.pack(fill="x", padx=15, pady=15)
        
        # Información del personal
        personnel_content = """
👥 INFORMACIÓN DEL PERSONAL

📊 ESTADÍSTICAS GENERALES:
   • Total de empleados: 85
   • Personal activo: 82
   • Personal en licencia: 3
   • Nuevas contrataciones: 5

👨‍🏫 INSTRUCTORES:
   • Total: 25
   • Tiempo completo: 18
   • Tiempo parcial: 7
   • Especializaciones: 12

👨‍💼 ADMINISTRATIVOS:
   • Total: 15
   • Recepción: 3
   • Contabilidad: 4
   • Recursos Humanos: 3
   • Tecnología: 5

🛡️ SEGURIDAD:
   • Total: 12
   • Turno día: 6
   • Turno noche: 6
   • Supervisores: 2

🧹 MANTENIMIENTO:
   • Total: 8
   • Limpieza: 5
   • Técnicos: 3

📅 GESTIÓN DE PERSONAL:
   • Contratos vigentes: 78
   • Contratos por vencer: 7
   • Evaluaciones pendientes: 12
   • Capacitaciones programadas: 8

💰 RECURSOS HUMANOS:
   • Presupuesto asignado: $125,000
   • Presupuesto utilizado: $98,500
   • Presupuesto disponible: $26,500
        """
        
        # Crear etiquetas para la información del personal
        personnel_lines = personnel_content.strip().split('\n')
        for i, line in enumerate(personnel_lines):
            if line.strip():
                label = styles.create_info_label(personnel_frame, line)
                label.pack(anchor="w", pady=2)
        
        # Botones de control
        control_frame = styles.create_main_frame(personnel_win)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón para exportar información
        export_btn = styles.create_accent_button(
            control_frame, 
            "📊 EXPORTAR INFORMACIÓN", 
            lambda: self._export_personnel_info()
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            personnel_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(personnel_win)

    def _show_resource_management(self, parent_window):
        """Muestra la gestión de recursos"""
        # Crear ventana de gestión de recursos
        resource_win = styles.create_modal_window(self.parent, "💰 GESTIÓN DE RECURSOS", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(resource_win, "💰 GESTIÓN DE RECURSOS")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(resource_win, "Administración de recursos del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal para la gestión de recursos
        grid_container = styles.create_main_frame(resource_win)
        grid_container.pack(expand=True, padx=40, pady=20)
        
        # Configurar el grid 3x4
        for i in range(3):
            grid_container.grid_rowconfigure(i, weight=1)
        for i in range(4):
            grid_container.grid_columnconfigure(i, weight=1)
        
        # Lista de áreas de recursos
        resource_areas = [
            "Presupuesto General", "Recursos Humanos", "Equipos y Tecnología", "Infraestructura",
            "Materiales de Oficina", "Servicios Públicos", "Mantenimiento", "Capacitación",
            "Marketing", "Investigación", "Desarrollo", "Innovación"
        ]
        
        # Crear botones de áreas de recursos con estilo futurista
        for i, resource_area in enumerate(resource_areas):
            row = i // 4
            col = i % 4
            
            resource_btn = styles.create_futuristic_button(
                grid_container, 
                resource_area, 
                lambda area=resource_area: self._manage_resource_area(area),
                width=15, 
                height=2
            )
            
            # Aplicar efectos de hover
            styles.apply_button_hover_effects(resource_btn)
            resource_btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Botones de control
        control_frame = styles.create_main_frame(resource_win)
        control_frame.pack(fill="x", padx=40, pady=20)
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            resource_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(resource_win)

    def _show_administrative_reports(self, parent_window):
        """Muestra los reportes administrativos"""
        # Crear ventana de reportes administrativos
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES ADMINISTRATIVOS", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES ADMINISTRATIVOS")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes administrativos del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas administrativas
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas administrativas
        admin_stats_content = """
📊 ESTADÍSTICAS ADMINISTRATIVAS

💰 FINANZAS:
   • Presupuesto anual: $2,500,000
   • Presupuesto ejecutado: $1,850,000
   • Presupuesto disponible: $650,000
   • Eficiencia presupuestaria: 74%

👥 RECURSOS HUMANOS:
   • Total de empleados: 85
   • Costo promedio por empleado: $45,000
   • Rotación de personal: 8%
   • Satisfacción laboral: 87%

🏗️ INFRAESTRUCTURA:
   • Edificios: 5
   • Aulas: 25
   • Laboratorios: 12
   • Oficinas: 18
   • Estado general: Excelente

📱 TECNOLOGÍA:
   • Equipos de cómputo: 150
   • Equipos funcionando: 148
   • Equipos en mantenimiento: 2
   • Actualizaciones pendientes: 5

📚 SERVICIOS EDUCATIVOS:
   • Programas activos: 15
   • Estudiantes matriculados: 1,250
   • Tasa de retención: 92%
   • Satisfacción estudiantil: 89%

📈 INDICADORES DE GESTIÓN:
   • Eficiencia operativa: 91%
   • Cumplimiento de objetivos: 88%
   • Innovación: 85%
   • Sostenibilidad: 93%
        """
        
        # Crear etiquetas para las estadísticas administrativas
        stats_lines = admin_stats_content.strip().split('\n')
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
            lambda: self._export_administrative_report()
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

    def _manage_resource_area(self, resource_area):
        """Maneja la gestión de un área de recursos específica"""
        messagebox.showinfo("💰 GESTIÓN DE RECURSOS", 
                           f"Gestionando: {resource_area}\n\n"
                           "El sistema está configurando la gestión de recursos para esta área.\n"
                           "Por favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la gestión de recursos del área seleccionada

    def _export_personnel_info(self):
        """Exporta la información del personal"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"informacion_personal_{timestamp}.csv"
            
            # Datos de la información del personal
            personnel_data = [
                ['INFORMACIÓN DEL PERSONAL - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS DEL PERSONAL'],
                ['Total de empleados', '85'],
                ['Personal activo', '82'],
                ['Personal en licencia', '3'],
                ['Nuevas contrataciones', '5'],
                ['Instructores', '25'],
                ['Administrativos', '15'],
                ['Seguridad', '12'],
                ['Mantenimiento', '8']
            ]
            
            if export_to_csv(personnel_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"La información del personal se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar la información del personal.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar la información del personal:\n\n{e}")

    def _export_administrative_report(self):
        """Exporta el reporte administrativo"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_administrativo_{timestamp}.csv"
            
            # Datos del reporte administrativo
            admin_data = [
                ['REPORTE ADMINISTRATIVO - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS ADMINISTRATIVAS'],
                ['Presupuesto anual', '$2,500,000'],
                ['Presupuesto ejecutado', '$1,850,000'],
                ['Presupuesto disponible', '$650,000'],
                ['Total de empleados', '85'],
                ['Edificios', '5'],
                ['Aulas', '25'],
                ['Laboratorios', '12'],
                ['Eficiencia operativa', '91%']
            ]
            
            if export_to_csv(admin_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"El reporte administrativo se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar el reporte administrativo.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar el reporte administrativo:\n\n{e}")
