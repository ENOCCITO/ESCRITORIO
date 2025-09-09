#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schedule_interface.py
- Interfaz de programación del sistema de dispensación biométrica
- Visualización de horarios y programación del campus con diseño futurista
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import time
import threading
import styles
from config import *
from utils import *
from db_utils import get_daily_schedule, search_schedule_by_name

class ScheduleInterface:
    def __init__(self, parent):
        self.parent = parent
        
    def show_schedule_interface(self):
        """Muestra la interfaz de programación del día actual con diseño futurista"""
        # Crear ventana de programación
        self.schedule_win = styles.create_modal_window(self.parent, "📅 VER PROGRAMACIÓN - SISTEMA CEFA", "1200x800")
        self.schedule_win.resizable(True, True)
        self.schedule_win.configure(bg='#0a0a0a')
        
        # Variables para animaciones
        self.animation_running = True
        self.glow_intensity = 0
        
        # Crear fondo animado
        self._create_animated_background()
        
        # Header futurista con efectos
        self._create_futuristic_header()
        
        # Panel de búsqueda futurista
        self._create_search_panel()
        
        # Tabla de programación con diseño futurista
        self._create_schedule_table()
        
        # Panel de controles futurista
        self._create_control_panel()
        
        # Iniciar animaciones
        self._start_animations()
        
        # Cargar datos iniciales
        self._load_schedule_data()
        
        # Centrar la ventana
        styles.center_window(self.schedule_win)

    def _create_animated_background(self):
        """Crea un fondo animado con efectos de partículas"""
        self.bg_canvas = tk.Canvas(
            self.schedule_win,
            bg='#0a0a0a',
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear líneas de conexión animadas
        self.connection_lines = []
        for i in range(20):
            line = self.bg_canvas.create_line(
                0, 0, 0, 0,
                fill='#00d4ff',
                width=1,
                state='hidden'
            )
            self.connection_lines.append(line)

    def _create_futuristic_header(self):
        """Crea el header con efectos futuristas"""
        header_frame = tk.Frame(self.schedule_win, bg='#0a0a0a', height=120)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Título principal con efecto de brillo
        title_frame = tk.Frame(header_frame, bg='#0a0a0a')
        title_frame.pack(expand=True)
        
        # Icono animado
        self.title_icon = tk.Label(
            title_frame,
            text="⚡",
            font=("Segoe UI", 48),
            fg='#00d4ff',
            bg='#0a0a0a'
        )
        self.title_icon.pack(side="left", padx=(0, 20))
        
        # Título con fecha
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.title_label = tk.Label(
            title_frame,
            text=f"PROGRAMACIÓN DEL DÍA",
            font=("Segoe UI", 28, "bold"),
            fg='#00ffff',
            bg='#0a0a0a'
        )
        self.title_label.pack(side="left", padx=(0, 20))
        
        # Fecha con efecto especial
        self.date_label = tk.Label(
            title_frame,
            text=current_date,
            font=("Segoe UI", 24, "bold"),
            fg='#ffffff',
            bg='#0a0a0a'
        )
        self.date_label.pack(side="left")
        
        # Línea decorativa
        self.decorative_line = tk.Frame(header_frame, height=3, bg='#00d4ff')
        self.decorative_line.pack(fill="x", pady=(10, 0))

    def _create_search_panel(self):
        """Crea el panel de búsqueda con diseño futurista"""
        search_container = tk.Frame(self.schedule_win, bg='#0a0a0a')
        search_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Panel de búsqueda con borde brillante
        self.search_panel = tk.Frame(
            search_container,
            bg='#1a1a2e',
            relief='flat',
            bd=2
        )
        self.search_panel.pack(fill="x", pady=(0, 10))
        
        # Título del buscador
        search_title = tk.Label(
            self.search_panel,
            text="🔍 BÚSQUEDA AVANZADA",
            font=("Segoe UI", 14, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        search_title.pack(pady=(15, 10))
        
        # Frame interno para controles
        search_inner = tk.Frame(self.search_panel, bg='#1a1a2e')
        search_inner.pack(fill="x", padx=20, pady=(0, 15))
        
        # Label del buscador
        search_label = tk.Label(
            search_inner,
            text="Buscar por nombre del instructor:",
            font=("Segoe UI", 12),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        search_label.pack(side="left", padx=(0, 15))
        
        # Campo de búsqueda futurista
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_inner,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            bg='#2a2f3e',
            fg='#ffffff',
            insertbackground='#00d4ff',
            relief='flat',
            bd=5,
            width=35
        )
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind('<KeyRelease>', self._on_search_change)
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)
        
        # Botón de limpiar con efecto hover
        self.clear_btn = tk.Button(
            search_inner,
            text="🗑️ LIMPIAR",
            font=("Segoe UI", 11, "bold"),
            bg='#ff6b6b',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            command=self._clear_search,
            cursor='hand2'
        )
        self.clear_btn.pack(side="left", padx=(10, 0))
        
        # Efectos hover para botones
        self.clear_btn.bind('<Enter>', lambda e: self.clear_btn.config(bg='#ff5252'))
        self.clear_btn.bind('<Leave>', lambda e: self.clear_btn.config(bg='#ff6b6b'))

    def _create_schedule_table(self):
        """Crea la tabla de programación con diseño futurista"""
        table_container = tk.Frame(self.schedule_win, bg='#0a0a0a')
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Panel de tabla con borde brillante
        self.table_panel = tk.Frame(
            table_container,
            bg='#1a1a2e',
            relief='flat',
            bd=2
        )
        self.table_panel.pack(fill="both", expand=True)
        
        # Título de la tabla
        table_title = tk.Label(
            self.table_panel,
            text="📊 PROGRAMACIÓN DETALLADA",
            font=("Segoe UI", 16, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        table_title.pack(pady=(15, 10))
        
        # Frame para la tabla
        table_frame = tk.Frame(self.table_panel, bg='#1a1a2e')
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Configurar estilo de Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Futuristic.Treeview",
            background='#2a2f3e',
            foreground='#ffffff',
            fieldbackground='#2a2f3e',
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        style.configure(
            "Futuristic.Treeview.Heading",
            background='#00d4ff',
            foreground='#0a0a0a',
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0
        )
        style.map(
            "Futuristic.Treeview",
            background=[('selected', '#00d4ff')],
            foreground=[('selected', '#0a0a0a')]
        )
        
        # Crear Treeview con estilo futurista
        columns = ('Hora', 'Ambiente', 'Instructor', 'Programa de Formación')
        self.schedule_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=12,
            style="Futuristic.Treeview"
        )
        
        # Configurar columnas con iconos
        self.schedule_tree.heading('Hora', text='🕐 HORA')
        self.schedule_tree.heading('Ambiente', text='🏢 AMBIENTE')
        self.schedule_tree.heading('Instructor', text='👨‍🏫 INSTRUCTOR')
        self.schedule_tree.heading('Programa de Formación', text='📚 PROGRAMA DE FORMACIÓN')
        
        # Configurar ancho de columnas
        self.schedule_tree.column('Hora', width=120, anchor='center')
        self.schedule_tree.column('Ambiente', width=180, anchor='center')
        self.schedule_tree.column('Instructor', width=200, anchor='center')
        self.schedule_tree.column('Programa de Formación', width=350, anchor='w')
        
        # Scrollbar personalizada
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.schedule_tree.yview
        )
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.schedule_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_control_panel(self):
        """Crea el panel de controles con diseño futurista"""
        control_container = tk.Frame(self.schedule_win, bg='#0a0a0a')
        control_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Panel de controles
        self.control_panel = tk.Frame(
            control_container,
            bg='#1a1a2e',
            relief='flat',
            bd=2
        )
        self.control_panel.pack(fill="x")
        
        # Frame interno para botones
        button_frame = tk.Frame(self.control_panel, bg='#1a1a2e')
        button_frame.pack(fill="x", padx=20, pady=15)
        
        # Botón de actualizar
        self.refresh_btn = tk.Button(
            button_frame,
            text="🔄 ACTUALIZAR",
            font=("Segoe UI", 12, "bold"),
            bg='#4CAF50',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=25,
            pady=10,
            command=self._refresh_schedule,
            cursor='hand2'
        )
        self.refresh_btn.pack(side="left", padx=(0, 15))
        
        # Botón de exportar
        self.export_btn = tk.Button(
            button_frame,
            text="📊 EXPORTAR",
            font=("Segoe UI", 12, "bold"),
            bg='#2196F3',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=25,
            pady=10,
            command=self._export_schedule,
            cursor='hand2'
        )
        self.export_btn.pack(side="left", padx=(0, 15))
        
        # Botón de cerrar
        self.close_btn = tk.Button(
            button_frame,
            text="✅ CERRAR",
            font=("Segoe UI", 12, "bold"),
            bg='#f44336',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=25,
            pady=10,
            command=self._close_window,
            cursor='hand2'
        )
        self.close_btn.pack(side="right")
        
        # Efectos hover para todos los botones
        self._setup_button_hovers()

    def _setup_button_hovers(self):
        """Configura efectos hover para los botones"""
        buttons = [
            (self.refresh_btn, '#45a049'),
            (self.export_btn, '#1976D2'),
            (self.close_btn, '#d32f2f')
        ]
        
        for btn, hover_color in buttons:
            btn.bind('<Enter>', lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind('<Leave>', lambda e, b=btn, c=btn.cget('bg'): b.config(bg=c))

    def _start_animations(self):
        """Inicia las animaciones de la interfaz"""
        self._animate_title_icon()
        self._animate_background_lines()

    def _animate_title_icon(self):
        """Anima el icono del título"""
        if not self.animation_running:
            return
            
        # Rotar el icono
        current_text = self.title_icon.cget('text')
        icons = ['⚡', '🔮', '🌟', '💫', '⭐']
        current_index = icons.index(current_text) if current_text in icons else 0
        next_index = (current_index + 1) % len(icons)
        self.title_icon.config(text=icons[next_index])
        
        # Cambiar color
        colors = ['#00d4ff', '#00ffff', '#ff00ff', '#ffff00', '#ff6b6b']
        self.title_icon.config(fg=colors[next_index])
        
        # Programar siguiente animación
        self.schedule_win.after(2000, self._animate_title_icon)

    def _animate_background_lines(self):
        """Anima las líneas de fondo"""
        if not self.animation_running:
            return
            
        # Limpiar líneas anteriores
        for line in self.connection_lines:
            self.bg_canvas.itemconfig(line, state='hidden')
        
        # Crear nuevas líneas aleatorias
        import random
        for i in range(5):
            x1 = random.randint(0, 1200)
            y1 = random.randint(0, 800)
            x2 = random.randint(0, 1200)
            y2 = random.randint(0, 800)
            
            self.bg_canvas.coords(self.connection_lines[i], x1, y1, x2, y2)
            self.bg_canvas.itemconfig(self.connection_lines[i], state='normal')
        
        # Programar siguiente animación
        self.schedule_win.after(3000, self._animate_background_lines)

    def _on_search_focus_in(self, event):
        """Efecto cuando el campo de búsqueda recibe foco"""
        self.search_entry.config(bg='#3a3f4e', fg='#00d4ff')

    def _on_search_focus_out(self, event):
        """Efecto cuando el campo de búsqueda pierde foco"""
        self.search_entry.config(bg='#2a2f3e', fg='#ffffff')

    def _close_window(self):
        """Cierra la ventana y detiene animaciones"""
        self.animation_running = False
        self.schedule_win.destroy()

    def _load_schedule_data(self, search_term=""):
        """Carga los datos de programación en la tabla con efectos visuales"""
        try:
            # Limpiar tabla actual
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            # Mostrar indicador de carga
            self.schedule_tree.insert('', 'end', values=(
                "🔄", "Cargando...", "Por favor espere", "Obteniendo datos"
            ))
            self.schedule_win.update()
            
            # Obtener datos de programación
            if search_term:
                schedule_data = search_schedule_by_name(search_term)
            else:
                schedule_data = get_daily_schedule()
            
            # Limpiar indicador de carga
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            # Insertar datos en la tabla con efectos
            for i, item in enumerate(schedule_data):
                hora = f"{item['hora_inicio']} - {item['hora_fin']}"
                
                # Agregar con delay para efecto visual
                self.schedule_win.after(i * 100, lambda it=item, h=hora: 
                    self.schedule_tree.insert('', 'end', values=(
                        h,
                        it['ambiente'],
                        it['instructor'],
                        it['programa_formacion']
                    ))
                )
            
            # Mostrar mensaje si no hay resultados
            if not schedule_data:
                self.schedule_tree.insert('', 'end', values=(
                    "❌", "Sin datos", "No hay programación", "para este criterio de búsqueda"
                ))
                
        except Exception as e:
            messagebox.showerror("❌ ERROR", f"Error cargando programación:\n\n{e}")

    def _on_search_change(self, event):
        """Maneja el cambio en el campo de búsqueda con debounce"""
        # Cancelar búsqueda anterior si existe
        if hasattr(self, 'search_timer'):
            self.schedule_win.after_cancel(self.search_timer)
        
        # Programar nueva búsqueda con delay
        self.search_timer = self.schedule_win.after(300, self._perform_search)

    def _perform_search(self):
        """Realiza la búsqueda después del delay"""
        search_term = self.search_var.get().strip()
        self._load_schedule_data(search_term)

    def _clear_search(self):
        """Limpia el campo de búsqueda y recarga todos los datos"""
        self.search_var.set("")
        self._load_schedule_data()
        
        # Efecto visual de limpieza
        self.search_entry.config(bg='#2a2f3e')
        self.schedule_win.after(100, lambda: self.search_entry.config(bg='#3a3f4e'))
        self.schedule_win.after(200, lambda: self.search_entry.config(bg='#2a2f3e'))

    def _refresh_schedule(self):
        """Actualiza la programación con efectos visuales"""
        # Efecto de botón presionado
        original_bg = self.refresh_btn.cget('bg')
        self.refresh_btn.config(bg='#2e7d32')
        self.schedule_win.after(150, lambda: self.refresh_btn.config(bg=original_bg))
        
        # Actualizar datos
        search_term = self.search_var.get().strip()
        self._load_schedule_data(search_term)
        
        # Mostrar mensaje de confirmación
        self.schedule_win.after(500, lambda: 
            messagebox.showinfo("🔄 ACTUALIZADO", "La programación se ha actualizado correctamente."))

    def _export_schedule(self):
        """Exporta la programación a un archivo CSV con efectos visuales"""
        try:
            # Efecto de botón presionado
            original_bg = self.export_btn.cget('bg')
            self.export_btn.config(bg='#1565C0')
            self.schedule_win.after(150, lambda: self.export_btn.config(bg=original_bg))
            
            # Obtener datos actuales de la tabla
            search_term = self.search_var.get().strip()
            if search_term:
                schedule_data = search_schedule_by_name(search_term)
            else:
                schedule_data = get_daily_schedule()
            
            if not schedule_data:
                messagebox.showwarning("⚠️ ADVERTENCIA", "No hay datos para exportar.")
                return
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"programacion_dia_{timestamp}.csv"
            
            # Preparar datos para exportación
            export_data = [
                ['PROGRAMACIÓN DEL DÍA - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ['Criterio de búsqueda', search_term if search_term else 'Todos los registros'],
                [],
                ['Hora', 'Ambiente', 'Instructor', 'Programa de Formación']
            ]
            
            # Agregar datos de programación
            for item in schedule_data:
                hora = f"{item['hora_inicio']} - {item['hora_fin']}"
                export_data.append([
                    hora,
                    item['ambiente'],
                    item['instructor'],
                    item['programa_formacion']
                ])
            
            if export_to_csv(export_data, filename):
                messagebox.showinfo("📊 EXPORTACIÓN EXITOSA", 
                                  f"La programación se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                messagebox.showerror("❌ ERROR", "Error al exportar la programación.")
                
        except Exception as e:
            messagebox.showerror("🚨 ERROR", f"Error al exportar la programación:\n\n{e}")
