# Estructura del Proyecto - Sistema de Dispensación Biométrica

## 📁 Organización de Carpetas

```
ESCRITORIO/
├── src/                          # Código fuente principal
│   ├── app/                      # Aplicación GUI y API
│   │   ├── gui/                  # GUI PySide6 (main_window.py, launch.py)
│   │   ├── api/                  # FastAPI (main.py, routers/, schemas.py)
│   │   └── services/             # Servicios de aplicación (auth huella)
│   ├── interfaces/               # Interfaces de usuario (PySide6)
│   ├── core/                     # Lógica de negocio central
│   ├── domain/                   # Entidades y servicios de dominio
│   ├── infra/                    # Adaptadores DB (infra/db) y hardware (infra/hardware)
│   ├── utils/                    # Utilidades y helpers (styles, utils, db_utils)
│   └── config/                   # Configuración (settings.py + shim config.py)
│
├── arduino/                      # Código Arduino (.ino)
│   ├── arduino_nema17_CORREGIDO_FINAL.ino
│   ├── arduino_nema17_FINAL_FUNCIONANDO.ino
│   ├── arduino_nema17_controller.ino
│   ├── arduino_nema17_controller_FINAL.ino
│   ├── arduino_nema17_controller_fixed.ino
│   └── arduino_simple_working.ino
│
├── docs/                         # Documentación
│   ├── README.md
│   ├── README_ALERTAS.md
│   ├── README_ARDUINO_INTEGRATION.md
│   ├── README_BIOMETRICO.md
│   ├── README_NUEVO_SISTEMA.md
│   ├── README_REGISTRO_HUELLAS.md
│   ├── PROMPT_STITCH_AMBIENTES_DISPONIBLES.md
│   ├── PROMPT_STITCH_ASEO.md
│   ├── PROMPT_STITCH_INSTRUCTOR.md
│   └── PROMPT_STITCH_SEGURIDAD.md
│
├── data/                         # Datos exportados (CSVs, etc.)
│   ├── programacion_20251015_125355.csv
│   ├── programacion_dia_20250908_102709.csv
│   └── programacion_dia_20251015_105030.csv
│
├── assets/                       # Recursos (imágenes, iconos)
│   ├── images/                   # Imágenes de la interfaz
│   ├── idear.png
│   └── sena.png
│
├── scripts/                      # Scripts de utilidad/diagnóstico
│   ├── debug_arduino_complete.py
│   ├── diagnose_database_error.py
│   ├── diagnose_fingerprints.py
│   ├── explore_tables.py
│   ├── fix_arduino_port.py
│   └── liberar_puerto_arduino.py
│
├── main.py                       # Bootstrap GUI → src/app/gui/main_window.py
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos ignorados por git
└── .venv/                        # Entorno virtual (no versionado)
```

## 🚀 Configuración del Entorno

### Entorno Virtual

El proyecto utiliza un **único entorno virtual** `.venv` para todas las dependencias.

#### Crear y activar el entorno virtual:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Dependencias Principales

- **PySide6** >= 6.5.0 - Framework de interfaz gráfica
- **mysql-connector-python** >= 8.0.0 - Conexión a MySQL
- **pyserial** >= 3.5 - Comunicación serial con Arduino
- **pyfingerprint** >= 0.4 - Gestión de huellas dactilares
- **psutil** >= 5.9.0 - Información del sistema

## 📝 Estructura de Imports

Después de la reorganización, los imports deben seguir esta estructura:

```python
# Imports de interfaces
from src.interfaces.admin_interface import AdminInterface

# Imports de core
from src.core.alert_system import alert_system
from src.core.biometric_scanner import BiometricScanner

# Imports de utils
from src.utils.utils import db_connect
from src.utils import styles
from src.utils.db_utils import get_connection

# Imports de config
from src.config.config import DB_CONFIG
```

## 🎯 Ejecución del Proyecto

```bash
python main.py
```

## 🛠️ Scripts de Utilidad

Los scripts de diagnóstico y utilidad están en la carpeta `scripts/`:

- **debug_arduino_complete.py** - Diagnóstico completo de Arduino
- **diagnose_database_error.py** - Diagnóstico de errores de BD
- **diagnose_fingerprints.py** - Diagnóstico del sistema de huellas
- **explore_tables.py** - Exploración de tablas de BD
- **fix_arduino_port.py** - Corrección de puerto Arduino
- **liberar_puerto_arduino.py** - Liberar puerto Arduino bloqueado

## 📚 Documentación

Toda la documentación del proyecto se encuentra en la carpeta `docs/`:

- **README.md** - Documentación principal
- **README_ALERTAS.md** - Sistema de alertas
- **README_ARDUINO_INTEGRATION.md** - Integración con Arduino
- **README_BIOMETRICO.md** - Sistema biométrico
- **README_NUEVO_SISTEMA.md** - Nuevo sistema
- **README_REGISTRO_HUELLAS.md** - Registro de huellas

## 🔧 Configuración

La configuración del proyecto se encuentra en `src/config/config.py`:

- Configuración de base de datos
- Puertos de Arduino
- Rutas de archivos
- Parámetros del sistema

## 📊 Base de Datos

El sistema utiliza MySQL como base de datos principal:

- Base de datos: `sistema_llaves_v2`
- Tablas principales: `personal`, `ambientes`, `programacion`, etc.

## 🎨 Assets

Los recursos gráficos están organizados en `assets/`:

- **images/** - Imágenes de la interfaz
- **idear.png** - Logo IDEAR
- **sena.png** - Logo SENA

## 📦 Datos

Los archivos de datos exportados (CSV) se guardan en `data/`:

- Programaciones
- Reportes
- Exportaciones del sistema

## 🔒 Seguridad

- El entorno virtual `.venv` está excluido del repositorio
- Las credenciales de BD deben configurarse en `config.py`
- Los archivos de log no se versionan

## 📌 Notas Importantes

1. **Usar solo un entorno virtual**: `.venv` (se eliminó `.venv312`)
2. **Imports actualizados**: Todos los imports ahora usan rutas relativas desde `src/`
3. **Estructura modular**: Código organizado por responsabilidad
4. **Separación de concerns**: Interfaces, lógica de negocio, utilidades y configuración separadas

## 🐛 Troubleshooting

### Error de imports
Si encuentras errores de imports, asegúrate de que:
1. El entorno virtual esté activado
2. Todas las dependencias estén instaladas
3. Los imports usen las rutas correctas (`from src.xxx import ...`)

### Error de Arduino
Si hay problemas con Arduino:
1. Verifica el puerto COM en `config.py`
2. Ejecuta `scripts/liberar_puerto_arduino.py`
3. Revisa la conexión física del dispositivo

### Error de Base de Datos
Si hay problemas de conexión a BD:
1. Verifica las credenciales en `config.py`
2. Asegúrate de que MySQL esté corriendo
3. Ejecuta `scripts/diagnose_database_error.py`
