from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QScrollArea, QFrame, 
                               QCalendarWidget, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QFont, QPalette, QColor
from datetime import datetime, timedelta
import styles
from db_utils import get_weekly_schedule

class ScheduleCard(QFrame):
    """Tarjeta individual para mostrar un elemento de programación"""
    
    def __init__(self, schedule_item, parent=None):
        super().__init__(parent)
        self.schedule_item = schedule_item
        self.setup_card()
        
    def setup_card(self):
        """Configura la tarjeta con estilo limpio"""
        self.setMinimumHeight(80)
        self.setMaximumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                margin: 2px;
            }
            QFrame:hover {
                border: 1px solid #4a9eff;
                background-color: #353535;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Columna izquierda - Día y hora
        left_column = QVBoxLayout()
        left_column.setSpacing(5)
        
        day_label = QLabel(self.schedule_item['dia_semana'])
        day_label.setStyleSheet("""
            QLabel {
                color: #4a9eff;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        
        time_label = QLabel(f"{self.schedule_item['hora_inicio']} - {self.schedule_item['hora_fin']}")
        time_label.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 12px;
            }
        """)
        
        left_column.addWidget(day_label)
        left_column.addWidget(time_label)
        layout.addLayout(left_column)
        
        # Columna central - Instructor
        instructor_label = QLabel(self.schedule_item['instructor'])
        instructor_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        instructor_label.setWordWrap(True)
        layout.addWidget(instructor_label)
        
        # Columna derecha - Ambiente y programa
        right_column = QVBoxLayout()
        right_column.setSpacing(5)
        
        environment_label = QLabel(self.schedule_item['ambiente'])
        environment_label.setStyleSheet("""
            QLabel {
                color: #10b981;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        environment_label.setWordWrap(True)
        
        program_label = QLabel(self.schedule_item['programa_formacion'])
        program_label.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 11px;
            }
        """)
        program_label.setWordWrap(True)
        
        right_column.addWidget(environment_label)
        right_column.addWidget(program_label)
        layout.addLayout(right_column)

class ScheduleInterface(QWidget):
    """Interfaz de programación semanal"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.schedule_win = None
        self.schedule_data = []
        self.current_date = datetime.now()

    def show_schedule_interface(self):
        """Muestra la interfaz de programación limpia y profesional"""
        if self.schedule_win is None:
            self.schedule_win = QWidget()
            self.schedule_win.setWindowTitle("Sistema de Programación - CEFA")
            self.schedule_win.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
            """)
            
            # Configurar tamaño responsive
            screen = self.parent.screen().availableGeometry()
            screen_width = screen.width()
            screen_height = screen.height()
            
            # Cálculo responsive
            if screen_width <= 1024:
                width = int(screen_width * 0.95)
                height = int(screen_height * 0.90)
            elif screen_width <= 1440:
                width = int(screen_width * 0.90)
                height = int(screen_height * 0.85)
            else:
                width = min(1400, int(screen_width * 0.80))
                height = min(900, int(screen_height * 0.80))
            
            self.schedule_win.resize(width, height)
            self.schedule_win.setMinimumSize(800, 600)
            
            # Layout principal
            main_layout = QVBoxLayout(self.schedule_win)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(15)
            
            # Crear componentes limpios
            self._create_clean_header(main_layout)
            self._create_clean_control_panel(main_layout)
            self._create_clean_content_area(main_layout)
            
            # Cargar programación inicial
            self._load_weekly_schedule()
        
        # Centrar y mostrar
        styles.center_window(self.schedule_win)
        self.schedule_win.show()

    def _create_clean_header(self, parent_layout):
        """Crea el header limpio y profesional"""
        # Header container
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Icono simple
        icon_label = QLabel("📅")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #4a9eff;
                background: transparent;
                border: none;
            }
        """)
        header_layout.addWidget(icon_label)
        
        # Título principal
        title_label = QLabel("Sistema de Programación")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #ffffff;
                background: transparent;
                border: none;
                margin-left: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Espaciador
        header_layout.addStretch()
        
        # Fecha actual
        date_label = QLabel(f"{self.current_date.strftime('%d/%m/%Y')}")
        date_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #a0a0a0;
                background: transparent;
                border: none;
            }
        """)
        header_layout.addWidget(date_label)
        
        parent_layout.addWidget(header_frame)
        
    def _create_clean_control_panel(self, parent_layout):
        """Crea el panel de control limpio y profesional"""
        # Panel de control
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(20, 15, 20, 15)
        control_layout.setSpacing(20)
        
        # Campo de búsqueda
        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por instructor, ambiente, programa o día...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 8px 12px;
                color: #e0e0e0;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
                background-color: #252525;
            }
        """)
        self.search_input.textChanged.connect(self._on_search_changed)
        control_layout.addWidget(self.search_input)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        refresh_btn = QPushButton("Actualizar")
        refresh_btn.setStyleSheet(self._get_clean_button_style("#4a9eff"))
        refresh_btn.clicked.connect(self._refresh_schedule)
        
        export_btn = QPushButton("Exportar")
        export_btn.setStyleSheet(self._get_clean_button_style("#10b981"))
        export_btn.clicked.connect(self._export_schedule)
        
        clear_btn = QPushButton("Limpiar")
        clear_btn.setStyleSheet(self._get_clean_button_style("#ef4444"))
        clear_btn.clicked.connect(self._clear_search)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_btn)
        
        control_layout.addLayout(button_layout)
        parent_layout.addWidget(control_frame)
        
    def _create_clean_content_area(self, parent_layout):
        """Crea el área de contenido limpia y profesional"""
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setMinimumHeight(400)
        
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4a9eff;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5ba8ff;
            }
        """)
        
        # Contenedor para las tarjetas
        self.cards_container = QWidget()
        self.cards_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(15, 15, 15, 15)
        self.cards_layout.setSpacing(10)
        
        scroll_area.setWidget(self.cards_container)
        parent_layout.addWidget(scroll_area)
        
    def _get_clean_button_style(self, color):
        """Genera estilo CSS limpio para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """
        
    def _get_button_style(self, color, font_size="14px"):
        """Genera estilo CSS para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: {font_size};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
                transform: translateY(0px);
            }}
        """
        
    def _load_weekly_schedule(self):
        """Carga la programación semanal (lunes a viernes)"""
        try:
            print("🔄 Cargando programación semanal...")
            
            # Mostrar indicador de carga
            self._show_loading_indicator()
            
            # Obtener datos reales de la tabla programaciones
            try:
                real_data = get_weekly_schedule()
                if real_data and len(real_data) > 0:
                    print(f"✅ Programación cargada: {len(real_data)} elementos")
                    self.schedule_data = real_data
                else:
                    print("📭 No hay programación en la base de datos")
                    self.schedule_data = []
            except Exception as db_error:
                print(f"❌ Error de base de datos: {db_error}")
                print("📭 No se pudieron obtener datos de la base de datos")
                self.schedule_data = []
            
            # Filtrar por término de búsqueda si existe
            search_term = self.search_input.text().strip()
            if search_term:
                print(f"🔍 Filtrando por término: '{search_term}'")
                original_count = len(self.schedule_data)
                self.schedule_data = [
                    item for item in self.schedule_data
                    if (search_term.lower() in item['instructor'].lower() or
                        search_term.lower() in item['ambiente'].lower() or
                        search_term.lower() in item['programa_formacion'].lower() or
                        search_term.lower() in item['dia_semana'].lower())
                ]
                print(f"🔍 Filtrados: {original_count} -> {len(self.schedule_data)} elementos")
            
            # Mostrar los datos
            print(f"📋 Mostrando {len(self.schedule_data)} elementos en la interfaz")
            self._display_schedule_cards()
            
        except Exception as e:
            print(f"❌ Error cargando programación: {e}")
            self.schedule_data = []
            self._display_schedule_cards()
            
    def _show_loading_indicator(self):
        """Muestra indicador de carga"""
        # Limpiar contenedor de forma segura
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        loading_frame = QFrame()
        loading_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1f2e;
                border: 1px solid #2a3f5f;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        loading_layout = QVBoxLayout(loading_frame)
        loading_layout.setAlignment(Qt.AlignCenter)
        
        loading_label = QLabel("🔄 Cargando programación...")
        loading_label.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        loading_label.setAlignment(Qt.AlignCenter)
        
        loading_layout.addWidget(loading_label)
        self.cards_layout.addWidget(loading_frame)
        
    def _display_schedule_cards(self):
        """Muestra las tarjetas de programación"""
        print(f"🔄 Mostrando tarjetas de programación...")
        
        # Limpiar contenedor de forma segura
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        print(f"📊 Datos a mostrar: {len(self.schedule_data) if self.schedule_data else 0} elementos")
        
        if not self.schedule_data or len(self.schedule_data) == 0:
            print("📭 No hay datos, mostrando mensaje de no datos")
            # Mostrar mensaje de no hay datos
            no_data_frame = QFrame()
            no_data_frame.setStyleSheet("""
                QFrame {
                    background-color: #1a1f2e;
                    border: 2px solid #ff6b6b;
                    border-radius: 15px;
                    padding: 40px;
                }
            """)
            
            no_data_layout = QVBoxLayout(no_data_frame)
            no_data_layout.setAlignment(Qt.AlignCenter)
            
            no_data_label = QLabel("📭 No hay programación disponible\n\nLos instructores no tienen programación asignada")
            no_data_label.setStyleSheet("""
                QLabel {
                    color: #00d4ff;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setWordWrap(True)
            
            no_data_layout.addWidget(no_data_label)
            self.cards_layout.addWidget(no_data_frame)
            print("✅ Mensaje de no datos mostrado")
            return
            
        # Crear tarjetas para cada elemento de programación
        print(f"🎴 Creando {len(self.schedule_data)} tarjetas...")
        for i, item in enumerate(self.schedule_data):
            print(f"   Tarjeta {i+1}: {item['instructor']} - {item['hora_inicio']}-{item['hora_fin']}")
            card = ScheduleCard(item)
            self.cards_layout.addWidget(card)
            
        # Actualizar contador
        if hasattr(self, 'count_label'):
            self.count_label.setText(f"📊 {len(self.schedule_data)} elementos")
            
        # Agregar espaciador al final
        self.cards_layout.addStretch()
        print("✅ Tarjetas creadas y mostradas correctamente")
        
    def _on_search_changed(self):
        """Maneja cambios en el campo de búsqueda"""
        self._load_weekly_schedule()

    def _refresh_schedule(self):
        """Actualiza la programación"""
        self._load_weekly_schedule()

    def _export_schedule(self):
        """Exporta la programación"""
        if not self.schedule_data:
            QMessageBox.information(self, "Exportar", "No hay datos para exportar")
            return
            
        try:
            from datetime import datetime
            filename = f"programacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Día,Instructor,Ambiente,Programa,Hora Inicio,Hora Fin\n")
                for item in self.schedule_data:
                    f.write(f"{item['dia_semana']},{item['instructor']},{item['ambiente']},{item['programa_formacion']},{item['hora_inicio']},{item['hora_fin']}\n")
            
            QMessageBox.information(self, "Exportar", f"Programación exportada a {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")
            
    def _clear_search(self):
        """Limpia el campo de búsqueda"""
        self.search_input.setText("")
        
    def _close_window(self):
        """Cierra la ventana"""
        if self.schedule_win:
            self.schedule_win.close()
