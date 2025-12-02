#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
administrative_interface.py
- Interfaz administrativa (PySide6)
"""

from src.utils import styles
from src.config.config import *
from src.utils.utils import *
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox, 
                               QPushButton, QScrollArea, QFrame, QGridLayout, QSpacerItem, 
                               QSizePolicy)
from PySide6.QtCore import Qt
from src.interfaces.dialog_utils import CleanCloseDialog

class AdministrativeInterface:
    def __init__(self, parent):
        self.parent = parent

    def show_administrative_interface(self):
        # Crear ventana principal en pantalla completa real
        admin_win = CleanCloseDialog(self.parent)
        admin_win.setWindowTitle("📋 INTERFAZ ADMINISTRATIVA - SISTEMA CEFA")
        admin_win.setModal(False)
        
        # PANTALLA COMPLETA REAL (sin barra de tareas de Windows)
        admin_win.showFullScreen()
        print("📱 Interfaz administrativa en pantalla completa real")
        
        # Layout principal con scroll
        main_layout = QVBoxLayout(admin_win)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #0D6EFD;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #0b5ed7;
            }
        """)
        
        # Widget contenido responsive
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #ffffff;")
        content_layout = QVBoxLayout(content_widget)
        
        # Márgenes responsive basados en el tamaño de pantalla
        try:
            margin_base = max(30, min(60, int(base_width * 0.03)))
            spacing_base = max(20, min(40, int(base_height * 0.025)))
            content_layout.setContentsMargins(margin_base, margin_base, margin_base, margin_base)
            content_layout.setSpacing(spacing_base)
        except Exception:
            content_layout.setContentsMargins(40, 40, 40, 40)
            content_layout.setSpacing(30)
        
        # Header limpio
        self._create_modern_header(content_widget, content_layout)
        
        # Contenido principal
        self._create_main_content(content_widget, content_layout)
        
        # Footer
        self._create_modern_footer(content_widget, content_layout)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Ya está maximizada, no es necesario centrar ni mostrar
        print("✅ Interfaz administrativa lista en pantalla completa")

    def _create_modern_header(self, parent, layout):
        """Crea un header moderno limpio y blanco"""
        # Calcular escala responsive
        try:
            screen_width = parent.window().screen().availableGeometry().width()
            scale_factor = max(0.7, min(1.5, screen_width / 1200.0))
        except Exception:
            scale_factor = 1.0
        
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
                border-bottom: 2px solid #e9ecef;
            }
        """)
        
        # Altura responsive
        header_height = max(80, int(100 * scale_factor))
        header_frame.setMinimumHeight(header_height)
        
        # Márgenes responsive
        margin_size = max(20, int(30 * scale_factor))
        padding_size = max(15, int(20 * scale_factor))
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(margin_size, padding_size, margin_size, padding_size)
        header_layout.setSpacing(max(15, int(20 * scale_factor)))
        
        # Título principal responsive
        title_font_size = max(24, int(32 * scale_factor))
        title_text = QLabel("📋 Interfaz Administrativa")
        title_text.setStyleSheet(f"""
            QLabel {{
                font-size: {title_font_size}px;
                font-weight: bold;
                color: #111418;
                background-color: transparent;
                padding: {max(8, int(10 * scale_factor))}px;
            }}
        """)
        title_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Subtítulo
        subtitle_font_size = max(14, int(16 * scale_factor))
        subtitle_text = QLabel("Gestión de recursos y ambientes administrativos")
        subtitle_text.setStyleSheet(f"""
            QLabel {{
                font-size: {subtitle_font_size}px;
                color: #617289;
                background-color: transparent;
            }}
        """)
        
        # Layout vertical para título y subtítulo
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        title_container.addWidget(title_text)
        title_container.addWidget(subtitle_text)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # Botón cerrar (X)
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(
            "QPushButton {"
            "background-color: #f0f2f4; "
            "color: #111418; "
            "border: none; "
            "border-radius: 8px; "
            "font-size: 20px; "
            "font-weight: 600;"
            "}"
            "QPushButton:hover {"
            "background-color: #E5E7EB; "
            "}"
        )
        # Conectar al padre para cerrar
        try:
            parent_window = parent
            while parent_window and not hasattr(parent_window, 'close'):
                parent_window = parent_window.parent()
            if parent_window and hasattr(parent_window, 'close'):
                close_btn.clicked.connect(parent_window.close)
        except Exception:
            pass
        
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header_frame)
    
    def _create_main_content(self, parent, layout):
        """Crea el contenido principal con grid responsive y diseño limpio"""
        # Calcular escala responsive para fuentes y espaciado
        try:
            screen_width = parent.window().screen().availableGeometry().width()
            scale_factor = max(0.7, min(1.5, screen_width / 1200.0))
            font_size = max(18, min(24, int(20 * scale_factor)))
            padding_size = max(12, min(20, int(15 * scale_factor)))
        except Exception:
            scale_factor = 1.0
            font_size = 20
            padding_size = 15
        
        # Título de sección responsive
        section_title = QLabel("🏢 Ambientes Asignados")
        section_title.setStyleSheet(f"""
            QLabel {{
                font-size: {font_size}px;
                font-weight: 600;
                color: #111418;
                background-color: transparent;
                padding: {padding_size}px 0px;
                border: none;
            }}
        """)
        layout.addWidget(section_title)
        
        # Contenedor de ambientes con grid responsive
        environments_container = QFrame()
        environments_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        
        environments_layout = QGridLayout(environments_container)
        
        # Espaciado responsive
        spacing = max(15, min(30, int(25 * scale_factor)))
        environments_layout.setSpacing(spacing)
        environments_layout.setContentsMargins(0, 0, 0, 0)
        
        environments = self._get_available_environments()
        
        if not environments:
            no_envs_label = QLabel("❌ No hay ambientes asignados")
            no_envs_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {max(16, int(18 * scale_factor))}px;
                    color: #617289;
                    background-color: #f8f9fa;
                    padding: {max(40, int(50 * scale_factor))}px;
                    border-radius: 12px;
                    border: 2px dashed #dee2e6;
                }}
            """)
            no_envs_label.setAlignment(Qt.AlignCenter)
            environments_layout.addWidget(no_envs_label, 0, 0, 1, 3)
        else:
            # Calcular número de columnas responsive
            if screen_width < 1024:
                cols = 1
            elif screen_width < 1600:
                cols = 2
            else:
                cols = 3
            
            # Crear tarjetas en grid responsive
            for i, env in enumerate(environments):
                env_id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio = env
                card = self._create_environment_card(environments_container, env_id, nombre, descripcion, ubicacion, piso, edificio, scale_factor)
                
                # Calcular posición en grid responsive
                row = i // cols
                col = i % cols
                environments_layout.addWidget(card, row, col)
        
        layout.addWidget(environments_container)
    
    def _create_environment_card(self, parent, env_id, nombre, descripcion, ubicacion, piso, edificio, scale_factor=1.0):
        """Crea una tarjeta moderna limpia para cada ambiente"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 12px;
            }
            QFrame:hover {
                border-color: #0D6EFD;
                background-color: #f8f9fa;
            }
        """)
        
        # Altura mínima responsive
        min_height = max(180, int(220 * scale_factor))
        card.setMinimumHeight(min_height)
        
        # Márgenes y espaciado responsive
        margin_size = max(20, int(25 * scale_factor))
        spacing_size = max(12, int(15 * scale_factor))
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(margin_size, margin_size, margin_size, margin_size)
        card_layout.setSpacing(spacing_size)
        
        # Header de la tarjeta responsive
        header_layout = QHBoxLayout()
        
        # Título responsive
        title_font_size = max(16, int(18 * scale_factor))
        title_label = QLabel(nombre)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {title_font_size}px;
                font-weight: 600;
                color: #111418;
                background-color: transparent;
            }}
        """)
        title_label.setWordWrap(True)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Detalles del ambiente responsive
        details_frame = QFrame()
        details_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: {max(12, int(15 * scale_factor))}px;
            }}
        """)
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(max(8, int(10 * scale_factor)))
        
        # Tamaños de fuente responsive para detalles
        detail_font_size = max(13, int(14 * scale_factor))
        
        # Ubicación
        if ubicacion:
            ubicacion_label = QLabel(f"📍 {ubicacion}")
            ubicacion_label.setStyleSheet(f"QLabel {{ color: #617289; font-size: {detail_font_size}px; }}")
            details_layout.addWidget(ubicacion_label)
        
        # Edificio y piso
        building_text = f"🏢 {edificio}" if edificio else "🏢 No especificado"
        if piso:
            building_text += f" - Piso {piso}"
        building_label = QLabel(building_text)
        building_label.setStyleSheet(f"QLabel {{ color: #617289; font-size: {detail_font_size}px; }}")
        details_layout.addWidget(building_label)
        
        # Descripción
        if descripcion:
            desc_label = QLabel(f"📝 {descripcion}")
            desc_label.setStyleSheet(f"QLabel {{ color: #8f9bb3; font-size: {detail_font_size}px; }}")
            desc_label.setWordWrap(True)
            details_layout.addWidget(desc_label)
        
        card_layout.addWidget(details_frame)
        
        # Espacio flexible
        card_layout.addStretch()
        
        # Botón de acceso responsive
        button_font_size = max(14, int(15 * scale_factor))
        button_padding = max(12, int(14 * scale_factor))
        
        access_btn = QPushButton("🚪 Acceder")
        access_btn.setCursor(Qt.PointingHandCursor)
        access_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #0D6EFD;
                color: #ffffff;
                font-size: {button_font_size}px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: {button_padding}px {button_padding + 8}px;
            }}
            QPushButton:hover {{
                background-color: #0b5ed7;
            }}
            QPushButton:pressed {{
                background-color: #0a58ca;
            }}
        """)
        access_btn.clicked.connect(lambda checked, eid=env_id, n=nombre: self._access_environment(eid, n))
        
        card_layout.addWidget(access_btn)
        
        return card
    
    def _create_modern_footer(self, parent, layout):
        """Crea un footer moderno limpio y minimalista"""
        # Calcular escala responsive
        try:
            screen_width = parent.window().screen().availableGeometry().width()
            scale_factor = max(0.7, min(1.5, screen_width / 1200.0))
        except Exception:
            scale_factor = 1.0
        
        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
                border-top: 2px solid #e9ecef;
            }
        """)
        
        # Altura responsive
        footer_height = max(50, int(60 * scale_factor))
        footer_frame.setMinimumHeight(footer_height)
        
        # Márgenes responsive
        margin_size = max(20, int(30 * scale_factor))
        padding_size = max(15, int(20 * scale_factor))
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(margin_size, padding_size, margin_size, padding_size)
        
        # Información del sistema responsive
        info_font_size = max(13, int(14 * scale_factor))
        info_label = QLabel("Sistema CEFA - Gestión Administrativa")
        info_label.setStyleSheet(f"""
            QLabel {{
                color: #8f9bb3;
                font-size: {info_font_size}px;
            }}
        """)
        
        footer_layout.addWidget(info_label)
        footer_layout.addStretch()
        
        layout.addWidget(footer_frame)


    def _get_available_environments(self):
        """Obtiene los ambientes disponibles de la base de datos"""
        try:
            from src.utils.utils import get_available_environments
            return get_available_environments()
        except Exception as e:
            print(f"❌ Error obteniendo ambientes: {e}")
            return []

    def _access_environment(self, environment_id, environment_name):
        QMessageBox.information(
            self.parent,
            "🚪 ACCESO AL AMBIENTE",
            f"Ambiente: {environment_name}\nID: {environment_id}\n\nEl sistema está configurando el acceso administrativo para este ambiente.\nPor favor, espere la confirmación del sistema."
        )
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el acceso administrativo al ambiente seleccionado
        print(f"✅ Acceso administrativo configurado para: {environment_name} (ID: {environment_id})")


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
                QMessageBox.information(self.parent, "📊 EXPORTACIÓN EXITOSA", f"La información del personal se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                QMessageBox.critical(self.parent, "❌ ERROR", "Error al exportar la información del personal.")
                
        except Exception as e:
            QMessageBox.critical(self.parent, "🚨 ERROR", f"Error al exportar la información del personal:\n\n{e}")

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
                QMessageBox.information(self.parent, "📊 EXPORTACIÓN EXITOSA", f"El reporte administrativo se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                QMessageBox.critical(self.parent, "❌ ERROR", "Error al exportar el reporte administrativo.")
                
        except Exception as e:
            QMessageBox.critical(self.parent, "🚨 ERROR", f"Error al exportar el reporte administrativo:\n\n{e}")
