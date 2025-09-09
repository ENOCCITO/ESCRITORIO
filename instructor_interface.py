#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instructor_interface.py
- Interfaz de instructor del sistema de dispensación biométrica
- Acceso a aulas y laboratorios asignados
"""

import tkinter as tk
from tkinter import messagebox
import styles
from config import *
from utils import *

class InstructorInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_instructor_interface(self):
        """Muestra la interfaz de instructor con información directa y diseño futurista"""
        # Crear ventana principal de instructor optimizada para 7 pulgadas
        instructor_win = styles.create_modal_window(self.parent, "👨‍🏫 INTERFAZ DE INSTRUCTOR - SISTEMA CEFA", "800x600")
        
        # Configurar para pantalla de 7 pulgadas
        instructor_win.configure(bg="#0a0a0a")
        
        # Contenedor principal con padding optimizado
        main_container = tk.Frame(instructor_win, bg="#0a0a0a")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header con título y efectos
        self._create_futuristic_header(main_container)
        
        # Contenedor de información principal
        info_container = tk.Frame(main_container, bg="#0a0a0a")
        info_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Información del ambiente asignado con diseño mejorado
        self._show_assigned_environment_futuristic(info_container)
        
        # Horario del instructor con diseño mejorado
        self._show_instructor_schedule_futuristic(info_container)
        
        # Footer con botón de cerrar sesión
        self._create_futuristic_footer(main_container, instructor_win)
        
        # Centrar la ventana
        styles.center_window(instructor_win)

    def _create_futuristic_header(self, parent_container):
        """Crea el header futurista con efectos visuales"""
        # Frame del header
        header_frame = tk.Frame(parent_container, bg="#0a0a0a")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal con efectos
        title_frame = tk.Frame(header_frame, bg="#0a0a0a")
        title_frame.pack(expand=True)
        
        # Icono de instructor
        instructor_icon = tk.Label(
            title_frame,
            text="👨‍🏫",
            font=("Arial", 48, "bold"),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        instructor_icon.pack()
        
        # Título principal
        welcome_label = tk.Label(
            title_frame,
            text="¡BIENVENIDO INSTRUCTOR!",
            font=("Arial", 24, "bold"),
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

    def _show_assigned_environment_futuristic(self, parent_container):
        """Muestra la información del ambiente con diseño futurista"""
        # Frame principal del ambiente
        env_main_frame = tk.Frame(parent_container, bg="#0a0a0a")
        env_main_frame.pack(fill="x", pady=(0, 15))
        
        # Título del ambiente con icono
        env_title_frame = tk.Frame(env_main_frame, bg="#0a0a0a")
        env_title_frame.pack(fill="x", pady=(0, 10))
        
        # Icono y título
        env_icon = tk.Label(
            env_title_frame,
            text="🏫",
            font=("Arial", 20),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        env_icon.pack(side="left")
        
        env_title = tk.Label(
            env_title_frame,
            text="AMBIENTE ASIGNADO",
            font=("Arial", 16, "bold"),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        env_title.pack(side="left", padx=(10, 0))
        
        # Frame de información con borde futurista
        env_info_frame = tk.Frame(
            env_main_frame,
            bg="#1a1a2e",
            relief="raised",
            bd=2
        )
        env_info_frame.pack(fill="x", padx=(0, 0))
        
        # Configurar grid para información
        env_info_frame.grid_rowconfigure(0, weight=1)
        env_info_frame.grid_columnconfigure(0, weight=1)
        
        # Información del ambiente con iconos mejorados
        env_info = [
            ("📍", "AULA PRINCIPAL", "Aula 101 - Laboratorio de Programación"),
            ("🔧", "EQUIPOS", "25 computadoras, Proyector 4K, Pizarra digital"),
            ("👥", "CAPACIDAD", "30 estudiantes"),
            ("🌐", "CONECTIVIDAD", "WiFi de alta velocidad, Red cableada"),
            ("📚", "RECURSOS", "Software de desarrollo, Bibliotecas digitales")
        ]
        
        for i, (icon, label, value) in enumerate(env_info):
            # Frame para cada línea de información
            info_line_frame = tk.Frame(env_info_frame, bg="#1a1a2e")
            info_line_frame.grid(row=i, column=0, sticky="ew", padx=15, pady=8)
            
            # Icono
            icon_label = tk.Label(
                info_line_frame,
                text=icon,
                font=("Arial", 14),
                bg="#1a1a2e",
                fg="#00d4ff"
            )
            icon_label.pack(side="left")
            
            # Label
            label_label = tk.Label(
                info_line_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                bg="#1a1a2e",
                fg="#ffffff"
            )
            label_label.pack(side="left", padx=(8, 5))
            
            # Valor
            value_label = tk.Label(
                info_line_frame,
                text=value,
                font=("Arial", 11),
                bg="#1a1a2e",
                fg="#00ff88",
                wraplength=500
            )
            value_label.pack(side="left")

    def _show_instructor_schedule_futuristic(self, parent_container):
        """Muestra el horario con diseño futurista"""
        # Frame principal del horario
        schedule_main_frame = tk.Frame(parent_container, bg="#0a0a0a")
        schedule_main_frame.pack(fill="both", expand=True)
        
        # Título del horario con icono
        schedule_title_frame = tk.Frame(schedule_main_frame, bg="#0a0a0a")
        schedule_title_frame.pack(fill="x", pady=(0, 10))
        
        # Icono y título
        schedule_icon = tk.Label(
            schedule_title_frame,
            text="📅",
            font=("Arial", 20),
            bg="#0a0a0a",
            fg="#ff6b35"
        )
        schedule_icon.pack(side="left")
        
        schedule_title = tk.Label(
            schedule_title_frame,
            text="HORARIO DE CLASES",
            font=("Arial", 16, "bold"),
            bg="#0a0a0a",
            fg="#ff6b35"
        )
        schedule_title.pack(side="left", padx=(10, 0))
        
        # Frame de horario con borde futurista
        schedule_info_frame = tk.Frame(
            schedule_main_frame,
            bg="#1a1a2e",
            relief="raised",
            bd=2
        )
        schedule_info_frame.pack(fill="both", expand=True)
        
        # Área de texto con scroll para el horario
        text_frame = tk.Frame(schedule_info_frame, bg="#1a1a2e")
        text_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Crear text widget con scroll
        schedule_text = tk.Text(
            text_frame,
            height=12,
            width=70,
            font=("Consolas", 10),
            bg="#0f0f23",
            fg="#00d4ff",
            insertbackground="#00d4ff",
            selectbackground="#00ff88",
            selectforeground="#000000",
            relief="flat",
            bd=0,
            wrap="word"
        )
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=schedule_text.yview)
        schedule_text.configure(yscrollcommand=scrollbar.set)
        
        schedule_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del horario con formato mejorado
        schedule_content = """🕐 HORARIOS DE CLASES - SEMANA ACTUAL

LUNES:
   • 8:00 AM - 10:00 AM: Aula 101 - Programación Básica (Grupo A)
   • 2:00 PM - 4:00 PM: Lab 201 - Prácticas de Código (Grupo B)

MARTES:
   • 9:00 AM - 11:00 AM: Aula 102 - Estructuras de Datos (Grupo A)
   • 3:00 PM - 5:00 PM: Lab 202 - Algoritmos (Grupo C)

MIÉRCOLES:
   • 8:00 AM - 10:00 AM: Aula 103 - Bases de Datos (Grupo B)
   • 2:00 PM - 4:00 PM: Lab 203 - SQL (Grupo A)

JUEVES:
   • 9:00 AM - 11:00 AM: Aula 104 - Programación Web (Grupo C)
   • 3:00 PM - 5:00 PM: Lab 204 - HTML/CSS/JS (Grupo B)

VIERNES:
   • 8:00 AM - 10:00 AM: Aula 105 - Proyecto Final (Grupo A)
   • 2:00 PM - 4:00 PM: Lab 205 - Desarrollo (Grupo C)

👥 ESTUDIANTES ASIGNADOS: 75 estudiantes (3 grupos)
📚 MATERIALES: Presentaciones, ejercicios, recursos multimedia
⚠️ NOTAS: Llegar 10 min antes, verificar equipos, reportar incidencias"""
        
        schedule_text.insert("1.0", schedule_content)
        schedule_text.config(state="disabled")

    def _create_futuristic_footer(self, parent_container, window):
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

    def _show_assigned_environment(self, parent_container):
        """Muestra la información del ambiente asignado al instructor"""
        # Frame para información del ambiente
        env_frame = styles.create_content_frame(parent_container)
        env_frame.pack(fill="x", pady=(0, 20))
        
        # Título de ambiente
        env_title = styles.create_subtitle_label(env_frame, "🏫 AMBIENTE ASIGNADO")
        env_title.pack(pady=(0, 15))
        
        # Información del ambiente
        env_info = """
📍 AULA PRINCIPAL: Aula 101 - Laboratorio de Programación
🔧 EQUIPOS: 25 computadoras, Proyector 4K, Pizarra digital
👥 CAPACIDAD: 30 estudiantes
🌐 CONECTIVIDAD: WiFi de alta velocidad, Red cableada
📚 RECURSOS: Software de desarrollo, Bibliotecas digitales
        """
        
        env_text = styles.create_text_widget(env_frame, height=6, state="disabled")
        env_text.pack(fill="x", padx=10, pady=10)
        env_text.config(state="normal")
        env_text.insert("1.0", env_info.strip())
        env_text.config(state="disabled")

    def _show_instructor_schedule_direct(self, parent_container):
        """Muestra el horario del instructor directamente en la interfaz"""
        # Frame para horario
        schedule_frame = styles.create_content_frame(parent_container)
        schedule_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título de horario
        schedule_title = styles.create_subtitle_label(schedule_frame, "📅 HORARIO DE CLASES")
        schedule_title.pack(pady=(0, 15))
        
        # Horario del instructor
        schedule_content = """
🕐 HORARIOS DE CLASES - SEMANA ACTUAL:

LUNES:
   • 8:00 AM - 10:00 AM: Aula 101 - Programación Básica (Grupo A)
   • 2:00 PM - 4:00 PM: Lab 201 - Prácticas de Código (Grupo B)

MARTES:
   • 9:00 AM - 11:00 AM: Aula 102 - Estructuras de Datos (Grupo A)
   • 3:00 PM - 5:00 PM: Lab 202 - Algoritmos (Grupo C)

MIÉRCOLES:
   • 8:00 AM - 10:00 AM: Aula 103 - Bases de Datos (Grupo B)
   • 2:00 PM - 4:00 PM: Lab 203 - SQL (Grupo A)

JUEVES:
   • 9:00 AM - 11:00 AM: Aula 104 - Programación Web (Grupo C)
   • 3:00 PM - 5:00 PM: Lab 204 - HTML/CSS/JS (Grupo B)

VIERNES:
   • 8:00 AM - 10:00 AM: Aula 105 - Proyecto Final (Grupo A)
   • 2:00 PM - 4:00 PM: Lab 205 - Desarrollo (Grupo C)

👥 ESTUDIANTES ASIGNADOS: 75 estudiantes (3 grupos)
📚 MATERIALES: Presentaciones, ejercicios, recursos multimedia
⚠️ NOTAS: Llegar 10 min antes, verificar equipos, reportar incidencias
        """
        
        schedule_text = styles.create_text_widget(schedule_frame, height=15, state="disabled")
        schedule_text.pack(fill="both", expand=True, padx=10, pady=10)
        schedule_text.config(state="normal")
        schedule_text.insert("1.0", schedule_content.strip())
        schedule_text.config(state="disabled")

    def _show_instructor_schedule(self, parent_window):
        """Muestra los horarios del instructor"""
        # Crear ventana de horarios
        schedule_win = styles.create_modal_window(self.parent, "📅 HORARIOS DEL INSTRUCTOR", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(schedule_win, "📅 HORARIOS DEL INSTRUCTOR")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(schedule_win, "Programación de clases y actividades")
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
        
        # Contenido de la programación del instructor
        schedule_content = """
📅 PROGRAMACIÓN DEL INSTRUCTOR - SISTEMA CEFA

🕐 HORARIOS DE CLASES:

LUNES:
   • 8:00 AM - 10:00 AM: Aula 101 - Programación Básica
   • 2:00 PM - 4:00 PM: Laboratorio 201 - Prácticas de Código

MARTES:
   • 9:00 AM - 11:00 AM: Aula 102 - Estructuras de Datos
   • 3:00 PM - 5:00 PM: Laboratorio 202 - Algoritmos

MIÉRCOLES:
   • 8:00 AM - 10:00 AM: Aula 103 - Bases de Datos
   • 2:00 PM - 4:00 PM: Laboratorio 203 - SQL

JUEVES:
   • 9:00 AM - 11:00 AM: Aula 104 - Programación Web
   • 3:00 PM - 5:00 PM: Laboratorio 204 - HTML/CSS/JS

VIERNES:
   • 8:00 AM - 10:00 AM: Aula 105 - Proyecto Final
   • 2:00 PM - 4:00 PM: Laboratorio 205 - Desarrollo

👥 ESTUDIANTES ASIGNADOS:
   • Grupo A: 25 estudiantes
   • Grupo B: 22 estudiantes
   • Grupo C: 28 estudiantes

📚 MATERIALES DISPONIBLES:
   • Presentaciones digitales
   • Ejercicios prácticos
   • Recursos multimedia
   • Bibliografía recomendada

⚠️ NOTAS IMPORTANTES:
   • Llegar 10 minutos antes de cada clase
   • Verificar equipos antes de iniciar
   • Reportar incidencias al administrador
   • Mantener registro de asistencia
        """
        
        schedule_text.insert("1.0", schedule_content)
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

    def _show_classroom_access(self, parent_window):
        """Muestra el acceso a aulas del instructor"""
        # Crear ventana de acceso a aulas
        access_win = styles.create_modal_window(self.parent, "🚪 ACCESO A AULAS", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(access_win, "🚪 ACCESO A AULAS")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(access_win, "Aulas y laboratorios asignados")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal para la cuadrícula de aulas
        grid_container = styles.create_main_frame(access_win)
        grid_container.pack(expand=True, padx=40, pady=20)
        
        # Configurar el grid 3x4
        for i in range(3):
            grid_container.grid_rowconfigure(i, weight=1)
        for i in range(4):
            grid_container.grid_columnconfigure(i, weight=1)
        
        # Lista de aulas disponibles
        classrooms = [
            "Aula 101", "Aula 102", "Aula 103", "Aula 104",
            "Aula 105", "Lab 201", "Lab 202", "Lab 203",
            "Lab 204", "Lab 205", "Auditorio", "Sala VIP"
        ]
        
        # Crear botones de aulas con estilo futurista
        for i, classroom_name in enumerate(classrooms):
            row = i // 4
            col = i % 4
            
            classroom_btn = styles.create_futuristic_button(
                grid_container, 
                classroom_name, 
                lambda name=classroom_name: self._access_classroom(name),
                width=12, 
                height=2
            )
            
            # Aplicar efectos de hover
            styles.apply_button_hover_effects(classroom_btn)
            classroom_btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Botones de control
        control_frame = styles.create_main_frame(access_win)
        control_frame.pack(fill="x", padx=40, pady=20)
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            access_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(access_win)

    def _show_instructor_reports(self, parent_window):
        """Muestra los reportes del instructor"""
        # Crear ventana de reportes
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES DEL INSTRUCTOR", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES DEL INSTRUCTOR")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes de actividades")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas del instructor
        stats_content = """
📊 ESTADÍSTICAS DEL INSTRUCTOR

👥 ESTUDIANTES:
   • Total de estudiantes: 75
   • Asistencia promedio: 92%
   • Calificación promedio: 8.7/10

📚 CLASES:
   • Clases impartidas este mes: 45
   • Horas de clase: 90 horas
   • Materiales entregados: 180

🎯 RENDIMIENTO:
   • Estudiantes aprobados: 68
   • Estudiantes en riesgo: 7
   • Tasa de aprobación: 90.7%

📅 ACTIVIDADES:
   • Evaluaciones realizadas: 15
   • Proyectos entregados: 25
   • Tutorías individuales: 12

🏆 LOGROS:
   • Mejor calificación: 9.8/10
   • Estudiantes destacados: 8
   • Proyectos sobresalientes: 5
        """
        
        # Crear etiquetas para las estadísticas
        stats_lines = stats_content.strip().split('\n')
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
            lambda: self._export_instructor_report()
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

    def _access_classroom(self, classroom_name):
        """Maneja el acceso a un aula específica"""
        messagebox.showinfo("🚪 ACCESO A AULA", 
                           f"Accediendo a: {classroom_name}\n\n"
                           "El sistema está configurando el acceso a esta aula.\n"
                           "Por favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el acceso al aula seleccionada

    def _export_instructor_report(self):
        """Exporta el reporte del instructor"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_instructor_{timestamp}.csv"
            
            # Datos del reporte
            report_data = [
                ['REPORTE DEL INSTRUCTOR - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS GENERALES'],
                ['Total de estudiantes', '75'],
                ['Asistencia promedio', '92%'],
                ['Calificación promedio', '8.7/10'],
                ['Clases impartidas este mes', '45'],
                ['Horas de clase', '90'],
                ['Tasa de aprobación', '90.7%']
            ]
            
            if export_to_csv(report_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"El reporte se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar el reporte.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar el reporte:\n\n{e}")
