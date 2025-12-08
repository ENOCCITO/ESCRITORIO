# Guía rápida: GUI y API

## GUI (PySide6)
- Lanzar: `python main.py` (bootstrap que delega a `src/app/gui/main_window.py`).
- Estilos: `assets/styles/app.qss`.
- Configuración: variables via `.env` → `src/config/settings.py` (shim en `src/config/config.py`).

## API (FastAPI)
- Lanzar: `uvicorn src.app.api.main:app --reload`
- Docs: `http://localhost:8000/api/docs`
- Rutas actuales:
  - `GET /api/health`
  - `POST /api/auth/fingerprint` (matcher simple, sin hardware; usa plantillas de DB)

## Capas
- `src/app/gui/`: GUI PySide6 (clase `App` en `main_window.py`)
- `src/app/api/`: FastAPI (`main.py`, routers, schemas)
- `src/app/services/`: Servicios de aplicación (auth de huella)
- `src/domain/`: Modelo y servicios de dominio
- `src/infra/`: Adaptadores DB (`infra/db`) y hardware (`infra/hardware`)
- `src/config/`: `settings.py` (Pydantic Settings) y shim `config.py`
- `assets/styles/`: QSS

## Configuración (.env)
Variables principales (ver `env.example`):
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=sicefa
FINGERPRINT_PORT_DEFAULT=COM3
ARDUINO_PORT_DEFAULT=COM4
DEFAULT_THRESHOLD=50
DEFAULT_TOPN=5
```
