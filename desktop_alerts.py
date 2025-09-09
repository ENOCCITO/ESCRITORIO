#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
desktop_alerts.py
- Sistema de alertas nativas de escritorio con diseño futurista
- Ventanas personalizadas con tkinter para el sistema biométrico
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional, Callable
import math

class DesktopAlertSystem:
    """Sistema de alertas nativas de escritorio con diseño futurista"""
    
    def __init__(self):
        self.active_alerts = []
        self.animation_running = False
    
    def show_access_denied_alert(self, role: str, user_name: Optional[str] = None):
        """Muestra alerta de acceso denegado en escritorio"""
        self._create_alert_window(
            title="🚫 ACCESO DENEGADO",
            icon="🚫",
            primary_text="Esta huella no corresponde a un",
            role_text=role.upper(),
            secondary_text="La huella digital escaneada no tiene permisos para acceder al módulo solicitado.",
            instruction_text="Por favor, contacte al administrador del sistema para obtener los permisos necesarios.",
            user_name=user_name,
            alert_type="denied",
            color_theme="red"
        )
    
    def show_fingerprint_not_found_alert(self):
        """Muestra alerta de huella no encontrada en escritorio"""
        self._create_alert_window(
            title="🔍 HUELLA NO RECONOCIDA",
            icon="🔍",
            primary_text="Huella digital no encontrada en el sistema",
            role_text="",
            secondary_text="La huella digital escaneada no se encuentra registrada en la base de datos del sistema.",
            instruction_text="Por favor, asegúrese de que su huella esté registrada en el sistema o contacte al administrador.",
            user_name=None,
            alert_type="not_found",
            color_theme="orange"
        )
    
    def show_access_granted_alert(self, role: str, user_name: str):
        """Muestra alerta de acceso concedido en escritorio"""
        self._create_alert_window(
            title="✅ ACCESO CONCEDIDO",
            icon="✅",
            primary_text="Bienvenido,",
            role_text=user_name,
            secondary_text=f"Verificación de identidad exitosa. Acceso concedido al módulo de {role.upper()}.",
            instruction_text="Iniciando interfaz del sistema...",
            user_name=None,
            alert_type="granted",
            color_theme="green",
            auto_close=True
        )
    
    def _create_alert_window(self, title: str, icon: str, primary_text: str, role_text: str, 
                           secondary_text: str, instruction_text: str, user_name: Optional[str],
                           alert_type: str, color_theme: str, auto_close: bool = False):
        """Crea una ventana de alerta personalizada"""
        
        # Crear ventana principal
        alert_window = tk.Toplevel()
        alert_window.title(title)
        alert_window.geometry("500x400")
        alert_window.resizable(False, False)
        alert_window.configure(bg="#0a0a0a")
        
        # Centrar ventana en pantalla
        self._center_window(alert_window)
        
        # Configurar tema de colores
        colors = self._get_color_theme(color_theme)
        
        # Hacer ventana modal
        alert_window.transient()
        alert_window.grab_set()
        
        # Frame principal con gradiente
        main_frame = tk.Frame(alert_window, bg="#0a0a0a", relief="flat", bd=0)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Borde con efecto neón
        border_frame = tk.Frame(main_frame, bg=colors["accent"], relief="flat", bd=2)
        border_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Frame de contenido
        content_frame = tk.Frame(border_frame, bg="#1a1a2e", relief="flat", bd=0)
        content_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Título principal
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),
            fg=colors["accent"],
            bg="#1a1a2e",
            relief="flat"
        )
        title_label.pack(pady=(20, 10))
        
        # Icono principal
        icon_label = tk.Label(
            content_frame,
            text=icon,
            font=("Segoe UI", 48),
            fg=colors["accent"],
            bg="#1a1a2e",
            relief="flat"
        )
        icon_label.pack(pady=(0, 15))
        
        # Texto principal
        primary_label = tk.Label(
            content_frame,
            text=primary_text,
            font=("Segoe UI", 16),
            fg="#ffffff",
            bg="#1a1a2e",
            relief="flat"
        )
        primary_label.pack(pady=(0, 5))
        
        # Texto del rol (si existe)
        if role_text:
            role_label = tk.Label(
                content_frame,
                text=role_text,
                font=("Segoe UI", 18, "bold"),
                fg=colors["accent"],
                bg="#1a1a2e",
                relief="flat"
            )
            role_label.pack(pady=(0, 15))
        
        # Texto secundario
        secondary_label = tk.Label(
            content_frame,
            text=secondary_text,
            font=("Segoe UI", 12),
            fg="#cccccc",
            bg="#1a1a2e",
            relief="flat",
            wraplength=450,
            justify="center"
        )
        secondary_label.pack(pady=(0, 10))
        
        # Texto de instrucción
        instruction_label = tk.Label(
            content_frame,
            text=instruction_text,
            font=("Segoe UI", 11, "bold"),
            fg=colors["instruction"],
            bg="#1a1a2e",
            relief="flat",
            wraplength=450,
            justify="center"
        )
        instruction_label.pack(pady=(0, 15))
        
        # Información del usuario (si existe)
        if user_name:
            user_label = tk.Label(
                content_frame,
                text=f"Usuario identificado: {user_name}",
                font=("Segoe UI", 10),
                fg="#888888",
                bg="#1a1a2e",
                relief="flat"
            )
            user_label.pack(pady=(0, 20))
        
        # Frame de botones
        button_frame = tk.Frame(content_frame, bg="#1a1a2e", relief="flat")
        button_frame.pack(pady=(0, 20))
        
        # Botón principal
        if auto_close:
            button_text = "CONTINUAR"
            button_command = lambda: self._close_alert(alert_window)
        else:
            button_text = "ENTENDIDO"
            button_command = lambda: self._close_alert(alert_window)
        
        main_button = tk.Button(
            button_frame,
            text=button_text,
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg=colors["button"],
            activeforeground="#ffffff",
            activebackground=colors["button_hover"],
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=button_command
        )
        main_button.pack(side="left", padx=10)
        
        # Efectos visuales
        self._add_visual_effects(alert_window, content_frame, colors)
        
        # Auto-cerrar si es necesario
        if auto_close:
            alert_window.after(3000, lambda: self._close_alert(alert_window))
        
        # Agregar a lista de alertas activas
        self.active_alerts.append(alert_window)
        
        # Configurar cierre
        alert_window.protocol("WM_DELETE_WINDOW", lambda: self._close_alert(alert_window))
        
        return alert_window
    
    def _get_color_theme(self, theme: str) -> dict:
        """Obtiene el tema de colores según el tipo de alerta"""
        themes = {
            "red": {
                "accent": "#ff6b6b",
                "button": "#ff6b6b",
                "button_hover": "#ff5252",
                "instruction": "#ffd93d"
            },
            "orange": {
                "accent": "#ffa726",
                "button": "#ffa726",
                "button_hover": "#ff9800",
                "instruction": "#ffd93d"
            },
            "green": {
                "accent": "#4caf50",
                "button": "#4caf50",
                "button_hover": "#45a049",
                "instruction": "#81c784"
            }
        }
        return themes.get(theme, themes["red"])
    
    def _center_window(self, window):
        """Centra la ventana en la pantalla"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _add_visual_effects(self, window, parent_frame, colors):
        """Agrega efectos visuales a la ventana"""
        # Efecto de pulso en el borde
        self._start_pulse_effect(window, parent_frame, colors["accent"])
        
        # Efecto de partículas (simulado con puntos)
        self._add_particle_effect(parent_frame, colors["accent"])
    
    def _start_pulse_effect(self, window, parent_frame, accent_color):
        """Inicia efecto de pulso en el borde"""
        def pulse():
            if window.winfo_exists():
                # Alternar entre colores para efecto de pulso
                current_bg = parent_frame.cget("bg")
                if current_bg == "#1a1a2e":
                    parent_frame.configure(bg=accent_color)
                else:
                    parent_frame.configure(bg="#1a1a2e")
                
                # Programar siguiente pulso
                window.after(1000, pulse)
        
        # Iniciar efecto después de un breve delay
        window.after(500, pulse)
    
    def _add_particle_effect(self, parent_frame, accent_color):
        """Agrega efecto de partículas simuladas"""
        # Crear canvas para partículas
        canvas = tk.Canvas(
            parent_frame,
            width=500,
            height=50,
            bg="#1a1a2e",
            highlightthickness=0,
            relief="flat"
        )
        canvas.pack(pady=(0, 10))
        
        # Dibujar partículas estáticas (simuladas)
        for i in range(20):
            x = i * 25
            y = 25
            canvas.create_oval(x, y-1, x+2, y+1, fill=accent_color, outline="")
    
    def _close_alert(self, window):
        """Cierra una alerta específica"""
        try:
            if window in self.active_alerts:
                self.active_alerts.remove(window)
            window.destroy()
        except:
            pass
    
    def close_all_alerts(self):
        """Cierra todas las alertas activas"""
        for alert in self.active_alerts[:]:
            self._close_alert(alert)
    
    def cleanup(self):
        """Limpia el sistema de alertas"""
        self.close_all_alerts()

# Instancia global del sistema de alertas de escritorio
desktop_alert_system = DesktopAlertSystem()
