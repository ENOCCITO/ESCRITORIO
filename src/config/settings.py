"""
Configuración centralizada usando Pydantic Settings.
- Lee valores desde variables de entorno y opcionalmente desde .env
- Expone un objeto `settings` reutilizable por GUI, scripts y futuras APIs
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Base de datos
    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "sicefa"

    # Puertos y hardware
    fingerprint_port_default: str = "COM3"
    fingerprint_baud_default: int = 57600
    arduino_port_default: str = "COM4"
    arduino_baud_default: int = 115200

    # Calibración y movimiento
    steps_per_rev: int = 200
    microstep_factor: int = 1
    gear_ratio: float = 6.8
    auto_home_after_open: bool = True

    # Lógica de huella
    default_threshold: int = 50
    default_topn: int = 5
    default_timeout_s: int = 30
    default_dwell: int = 2

    # Logging
    log_file: str = "dispenser.log"

    # Interfaz (mantener nombres usados en el código actual)
    modal_size: str = "500x400"
    admin_window_size: str = "600x500"
    environment_window_size: str = "800x700"
    registration_window_size: str = "900x700"
    schedule_window_size: str = "800x600"
    help_window_size: str = "600x500"
    system_info_window_size: str = "600x500"
    main_window_size: str = "1200x800"
    main_window_min_width: int = 1000
    main_window_min_height: int = 700

    # Estilos
    bg_dark: str = "#0b1220"
    bg_medium: str = "#111a2b"
    bg_light: str = "#162235"
    accent_blue: str = "#00e5ff"
    accent_cyan: str = "#7dd3fc"
    text_white: str = "#e6f3ff"
    text_gray: str = "#9fb3c8"

    # Botones y fuentes
    font_title: tuple[str, int, str] = ("Segoe UI", 24, "bold")
    font_subtitle: tuple[str, int] = ("Segoe UI", 12)
    font_button: tuple[str, int, str] = ("Segoe UI", 14, "bold")
    font_button_small: tuple[str, int, str] = ("Segoe UI", 12, "bold")
    font_label: tuple[str, int] = ("Segoe UI", 9)
    font_text: tuple[str, int] = ("Segoe UI", 10)
    font_monospace: tuple[str, int] = ("Consolas", 10)
    button_width: int = 20
    button_height: int = 3
    button_padding_x: int = 30
    button_padding_y: int = 20
    button_grid_padding: int = 20

    # Datos de ejemplo
    environments: list[str] = [
        "Ambiente 1",
        "Ambiente 2",
        "Ambiente 3",
        "Ambiente 4",
        "Ambiente 5",
        "Ambiente 6",
        "Ambiente 7",
        "Ambiente 8",
        "Ambiente 9",
        "Ambiente 10",
        "Ambiente 11",
        "Ambiente 12",
    ]
    sample_users: list[dict] = [
        {"id": 4052624, "name": "Mina Sitin", "document": "ID 4052624"},
        {"id": 2051321, "name": "Moradico Nomo", "document": "ID 2051321"},
        {"id": 4052819, "name": "Mora Sitin", "document": "ID 4052819"},
        {"id": 4052428, "name": "Mora Sitán", "document": "ID 4052428"},
        {"id": 2051621, "name": "Nhandio Nama", "document": "ID 2051621"},
        {"id": 4051629, "name": "Mora Sitin", "document": "ID 4051629"},
        {"id": 2077491, "name": "Hesopro", "document": "ID 2077491"},
    ]
    sample_candidates: list[tuple[int, str, list[int]]] = [
        (1001, "Administrador Principal", [1, 2, 3, 4, 5]),
        (1002, "Instructor Senior", [6, 7, 8, 9, 10]),
        (1003, "Seguridad Campus", [11, 12, 13, 14, 15]),
        (1004, "Personal Aseo", [16, 17, 18, 19, 20]),
        (1005, "Administrativo", [21, 22, 23, 24, 25]),
        (1006, "Usuario Prueba", [26, 27, 28, 29, 30]),
    ]

    @property
    def db_config(self) -> dict[str, str]:
        return {
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "database": self.db_name,
        }


# Instancia global para uso inmediato
settings = Settings()
