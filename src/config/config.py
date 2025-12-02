#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py
- Configuración centralizada del sistema de dispensación biométrica
- Constantes y parámetros del sistema
"""

# ============ CONFIGURACIÓN DE BASE DE DATOS ============
DB_CONFIG = dict(host="localhost", user="root", password="", database="sicefa")

# ============ CONFIGURACIÓN DE PUERTOS ============
FINGERPRINT_PORT_DEFAULT = "COM3"
FINGERPRINT_BAUD_DEFAULT = 57600

ARDUINO_PORT_DEFAULT = "COM4"
ARDUINO_BAUD_DEFAULT = 115200

# ============ CALIBRACIÓN MECÁNICA (PASOS) ============
# Pasos nativos del motor por vuelta
STEPS_PER_REV = 200
# 1 para full-step (L298N con secuencia de 4 estados), 2 si usas half‑step de 8 estados
MICROSTEP_FACTOR = 1
# Relación de transmisión rueda/motor calibrada: 1360 pasos por vuelta / (200*1) = 6.8
GEAR_RATIO = 6.8

# ============ COMPORTAMIENTO DE MOVIMIENTO ============
# Si True, tras abrir la llave vuelve automáticamente a HOME
AUTO_HOME_AFTER_OPEN = True

# ============ CONFIGURACIÓN DEL SISTEMA ============
DEFAULT_THRESHOLD = 50
DEFAULT_TOPN = 5
DEFAULT_TIMEOUT_S = 30
DEFAULT_DWELL = 2  # segundos (mantener 2s antes de volver a HOME)
LOG_FILE = "dispenser.log"

# ============ CONFIGURACIÓN DE INTERFAZ ============
# Colores del tema futurista (Dark Slate refinado)
BG_DARK = '#0b1220'
BG_MEDIUM = '#111a2b'
BG_LIGHT = '#162235'
ACCENT_BLUE = '#00e5ff'
ACCENT_CYAN = '#7dd3fc'
TEXT_WHITE = '#e6f3ff'
TEXT_GRAY = '#9fb3c8'

# ============ CONFIGURACIÓN DE VENTANAS ============
MAIN_WINDOW_SIZE = "1200x800"
MAIN_WINDOW_MIN_SIZE = (1000, 700)
MODAL_SIZE = "500x400"
ADMIN_WINDOW_SIZE = "600x500"
ENVIRONMENT_WINDOW_SIZE = "800x700"
REGISTRATION_WINDOW_SIZE = "900x700"
SCHEDULE_WINDOW_SIZE = "800x600"
HELP_WINDOW_SIZE = "600x500"
SYSTEM_INFO_WINDOW_SIZE = "600x500"
HISTORY_WINDOW_SIZE = "800x600"

# ============ CONFIGURACIÓN DE FUENTES ============
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_BUTTON_SMALL = ("Segoe UI", 12, "bold")
FONT_LABEL = ("Segoe UI", 9)
FONT_TEXT = ("Segoe UI", 10)
FONT_MONOSPACE = ("Consolas", 10)

# ============ CONFIGURACIÓN DE BOTONES ============
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 3
BUTTON_PADDING_X = 30
BUTTON_PADDING_Y = 20
BUTTON_GRID_PADDING = 20

# ============ CONFIGURACIÓN DE AMBIENTES ============
ENVIRONMENTS = [
    "Ambiente 1", "Ambiente 2", "Ambiente 3",
    "Ambiente 4", "Ambiente 5", "Ambiente 6", 
    "Ambiente 7", "Ambiente 8", "Ambiente 9",
    "Ambiente 10", "Ambiente 11", "Ambiente 12"
]

# ============ CONFIGURACIÓN DE USUARIOS DE EJEMPLO ============
SAMPLE_USERS = [
    {"id": 4052624, "name": "Mina Sitin", "document": "ID 4052624"},
    {"id": 2051321, "name": "Moradico Nomo", "document": "ID 2051321"},
    {"id": 4052819, "name": "Mora Sitin", "document": "ID 4052819"},
    {"id": 4052428, "name": "Mora Sitán", "document": "ID 4052428"},
    {"id": 2051621, "name": "Nhandio Nama", "document": "ID 2051621"},
    {"id": 4051629, "name": "Mora Sitin", "document": "ID 4051629"},
    {"id": 2077491, "name": "Hesopro", "document": "ID 2077491"}
]

# ============ CONFIGURACIÓN DE CANDIDATOS DE EJEMPLO ============
SAMPLE_CANDIDATES = [
    (1001, "Administrador Principal", [1, 2, 3, 4, 5]),
    (1002, "Instructor Senior", [6, 7, 8, 9, 10]),
    (1003, "Seguridad Campus", [11, 12, 13, 14, 15]),
    (1004, "Personal Aseo", [16, 17, 18, 19, 20]),
    (1005, "Administrativo", [21, 22, 23, 24, 25]),
    (1006, "Usuario Prueba", [26, 27, 28, 29, 30])
]
