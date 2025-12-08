#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py
- Shim temporal para mantener compatibilidad con el código existente.
- Carga los valores desde `src/config/settings.py` (Pydantic Settings).
"""
from __future__ import annotations

from src.config.settings import Settings, settings

# Exportar todas las constantes para mantener compatibilidad con los imports con wildcard
__all__ = [
    "settings",
    "DB_CONFIG",
    "FINGERPRINT_PORT_DEFAULT",
    "FINGERPRINT_BAUD_DEFAULT",
    "ARDUINO_PORT_DEFAULT",
    "ARDUINO_BAUD_DEFAULT",
    "STEPS_PER_REV",
    "MICROSTEP_FACTOR",
    "GEAR_RATIO",
    "AUTO_HOME_AFTER_OPEN",
    "DEFAULT_THRESHOLD",
    "DEFAULT_TOPN",
    "DEFAULT_TIMEOUT_S",
    "DEFAULT_DWELL",
    "LOG_FILE",
    "BG_DARK",
    "BG_MEDIUM",
    "BG_LIGHT",
    "ACCENT_BLUE",
    "ACCENT_CYAN",
    "TEXT_WHITE",
    "TEXT_GRAY",
    "MAIN_WINDOW_SIZE",
    "MAIN_WINDOW_MIN_SIZE",
    "MODAL_SIZE",
    "ADMIN_WINDOW_SIZE",
    "ENVIRONMENT_WINDOW_SIZE",
    "REGISTRATION_WINDOW_SIZE",
    "SCHEDULE_WINDOW_SIZE",
    "HELP_WINDOW_SIZE",
    "SYSTEM_INFO_WINDOW_SIZE",
    "HISTORY_WINDOW_SIZE",
    "FONT_TITLE",
    "FONT_SUBTITLE",
    "FONT_BUTTON",
    "FONT_BUTTON_SMALL",
    "FONT_LABEL",
    "FONT_TEXT",
    "FONT_MONOSPACE",
    "BUTTON_WIDTH",
    "BUTTON_HEIGHT",
    "BUTTON_PADDING_X",
    "BUTTON_PADDING_Y",
    "BUTTON_GRID_PADDING",
    "ENVIRONMENTS",
    "SAMPLE_USERS",
    "SAMPLE_CANDIDATES",
]

# ============ CONFIGURACIÓN DE BASE DE DATOS ============
DB_CONFIG = settings.db_config

# ============ CONFIGURACIÓN DE PUERTOS ============
FINGERPRINT_PORT_DEFAULT = settings.fingerprint_port_default
FINGERPRINT_BAUD_DEFAULT = settings.fingerprint_baud_default
ARDUINO_PORT_DEFAULT = settings.arduino_port_default
ARDUINO_BAUD_DEFAULT = settings.arduino_baud_default

# ============ CALIBRACIÓN MECÁNICA (PASOS) ============
STEPS_PER_REV = settings.steps_per_rev
MICROSTEP_FACTOR = settings.microstep_factor
GEAR_RATIO = settings.gear_ratio
AUTO_HOME_AFTER_OPEN = settings.auto_home_after_open

# ============ CONFIGURACIÓN DEL SISTEMA ============
DEFAULT_THRESHOLD = settings.default_threshold
DEFAULT_TOPN = settings.default_topn
DEFAULT_TIMEOUT_S = settings.default_timeout_s
DEFAULT_DWELL = settings.default_dwell  # segundos (mantener 2s antes de volver a HOME)
LOG_FILE = settings.log_file

# ============ CONFIGURACIÓN DE INTERFAZ ============
BG_DARK = settings.bg_dark
BG_MEDIUM = settings.bg_medium
BG_LIGHT = settings.bg_light
ACCENT_BLUE = settings.accent_blue
ACCENT_CYAN = settings.accent_cyan
TEXT_WHITE = settings.text_white
TEXT_GRAY = settings.text_gray

MAIN_WINDOW_SIZE = settings.main_window_size
MAIN_WINDOW_MIN_SIZE = (settings.main_window_min_width, settings.main_window_min_height)
MODAL_SIZE = settings.modal_size
ADMIN_WINDOW_SIZE = settings.admin_window_size
ENVIRONMENT_WINDOW_SIZE = settings.environment_window_size
REGISTRATION_WINDOW_SIZE = settings.registration_window_size
SCHEDULE_WINDOW_SIZE = settings.schedule_window_size
HELP_WINDOW_SIZE = settings.help_window_size
SYSTEM_INFO_WINDOW_SIZE = settings.system_info_window_size
HISTORY_WINDOW_SIZE = settings.system_info_window_size  # Compat con código existente

# ============ CONFIGURACIÓN DE FUENTES ============
FONT_TITLE = settings.font_title
FONT_SUBTITLE = settings.font_subtitle
FONT_BUTTON = settings.font_button
FONT_BUTTON_SMALL = settings.font_button_small
FONT_LABEL = settings.font_label
FONT_TEXT = settings.font_text
FONT_MONOSPACE = settings.font_monospace

# ============ CONFIGURACIÓN DE BOTONES ============
BUTTON_WIDTH = settings.button_width
BUTTON_HEIGHT = settings.button_height
BUTTON_PADDING_X = settings.button_padding_x
BUTTON_PADDING_Y = settings.button_padding_y
BUTTON_GRID_PADDING = settings.button_grid_padding

# ============ CONFIGURACIÓN DE AMBIENTES ============
ENVIRONMENTS = settings.environments

# ============ CONFIGURACIÓN DE USUARIOS DE EJEMPLO ============
SAMPLE_USERS = settings.sample_users

# ============ CONFIGURACIÓN DE CANDIDATOS DE EJEMPLO ============
SAMPLE_CANDIDATES = settings.sample_candidates
