#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleaning_interface.py
- Interfaz de aseo (PySide6)
"""

import styles
from config import *
from utils import *
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox

class CleaningInterface:
    def __init__(self, parent):
        self.parent = parent

    def show_cleaning_interface(self):
        cleaning_win = styles.create_modal_window(self.parent, "🧹 INTERFAZ DE ASEO - SISTEMA CEFA", "800x600")
        main_layout = QVBoxLayout(cleaning_win)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        self._create_cleaning_header(cleaning_win, main_layout)

        content_holder = styles.create_main_frame(cleaning_win)
        content_layout = QVBoxLayout(content_holder)
        self._show_environment_selection(content_holder, content_layout)
        main_layout.addWidget(content_holder)

        self._create_cleaning_footer(cleaning_win, cleaning_win, main_layout)
        styles.center_window(cleaning_win)
        cleaning_win.show()

    def _create_cleaning_header(self, parent, layout):
        header = styles.create_main_frame(parent)
        header_layout = QVBoxLayout(header)
        icon = styles.create_title_label(header, "🧹")
        title = styles.create_title_label(header, "¡BIENVENIDO PERSONAL DE ASEO!")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        layout.addWidget(header)

    def _show_environment_selection(self, parent, layout):
        title_row = styles.create_main_frame(parent)
        title_layout = QHBoxLayout(title_row)
        title_layout.addWidget(styles.create_subtitle_label(title_row, "🏢"))
        title_layout.addWidget(styles.create_subtitle_label(title_row, "SELECCIONAR AMBIENTE PARA LIMPIEZA"))
        title_layout.addStretch(1)
        layout.addWidget(title_row)

        environments_frame = styles.create_main_frame(parent)
        environments_layout = QVBoxLayout(environments_frame)
        environments = self._get_available_environments()
        if not environments:
            environments_layout.addWidget(styles.create_info_label(environments_frame, "❌ No hay ambientes disponibles en la base de datos"))
        else:
            for env in environments:
                env_id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio = env
                btn_text = f"🏢 {nombre}"
                btn = styles.create_futuristic_button(environments_frame, btn_text, lambda eid=env_id, n=nombre: self._select_environment(eid, n))
                environments_layout.addWidget(btn)
                info_text = f"📍 {ubicacion} | 🏗️ {tipo_ambiente} | 🏢 {edificio}" + (f" | 🏢 Piso {piso}" if piso else "")
                environments_layout.addWidget(styles.create_info_label(environments_frame, info_text))
        layout.addWidget(environments_frame)

    def _get_available_environments(self):
        """Obtiene los ambientes disponibles de la base de datos"""
        try:
            from utils import get_available_environments
            return get_available_environments()
        except Exception as e:
            print(f"❌ Error obteniendo ambientes: {e}")
            return []

    def _select_environment(self, environment_id, environment_name):
        QMessageBox.information(
            self.parent,
            "🧹 AMBIENTE SELECCIONADO",
            f"Ambiente seleccionado: {environment_name}\n\nID: {environment_id}\n\nEl sistema está configurando la limpieza para este ambiente.\nPor favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar la limpieza del ambiente seleccionado
        print(f"✅ Ambiente seleccionado: {environment_name} (ID: {environment_id})")

    def _create_cleaning_footer(self, parent, window, layout):
        footer = styles.create_main_frame(parent)
        footer_layout = QHBoxLayout(footer)
        logout_btn = styles.create_danger_button(footer, "🚪 CERRAR SESIÓN", window.close)
        footer_layout.addStretch(1)
        footer_layout.addWidget(logout_btn)
        layout.addWidget(footer)

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
