# 🔐 Sistema de Dispensación Biométrica - CEFA

Sistema integral de control de acceso biométrico con integración Arduino para gestión de llaves y ambientes.

## 🚀 Inicio Rápido

### 1. Activar el Entorno Virtual

**PowerShell:**
```powershell
.\activate.ps1
```

**CMD:**
```cmd
activate.bat
```

**Manual (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Ejecutar la Aplicación (GUI)

```bash
python main.py
```

### 3. Ejecutar la API
```bash
uvicorn src.app.api.main:app --reload
```

## 📁 Estructura del Proyecto

```
ESCRITORIO/
├── src/                     # Código fuente
│   ├── app/                 # GUI y API
│   ├── interfaces/          # Interfaces de usuario
│   ├── core/                # Lógica de negocio
│   ├── domain/              # Dominio
│   ├── infra/               # Adaptadores
│   ├── utils/               # Utilidades
│   └── config/              # Configuración
├── arduino/                 # Código Arduino
├── documentacion/           # Documentos
├── assets/                  # Recursos gráficos
├── scripts/                 # Scripts de utilidad
├── main.py                  # Bootstrap GUI
└── requirements.txt         # Dependencias
```

📖 Ver documentación completa: `documentacion/ESTRUCTURA_PROYECTO.md`

## 🔧 Instalación

### Requisitos Previos

- Python 3.12+
- MySQL Server
- Arduino (opcional, para control de hardware)

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Dependencias Principales

- **PySide6** - Interfaz gráfica
- **mysql-connector-python** - Conexión a MySQL
- **pyserial** - Comunicación con Arduino
- **pyfingerprint** - Gestión de huellas
- **psutil** - Información del sistema

## ⚙️ Configuración

Edita `.env` y `src/config/settings.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_password',
    'database': 'sistema_llaves_v2'
}
```

## 📚 Documentación

- `documentacion/ESTRUCTURA_PROYECTO.md` - Estructura detallada
- `documentacion/RESUMEN_REORGANIZACION.md` - Resumen de cambios
- `documentacion/README_API_GUI.md` - Guía rápida GUI/API

## 🛠️ Scripts de Utilidad

Los scripts de diagnóstico están en la carpeta `scripts/`:

```bash
# Diagnosticar Arduino
python scripts/debug_arduino_complete.py

# Diagnosticar Base de Datos
python scripts/diagnose_database_error.py

# Diagnosticar Sistema de Huellas
python scripts/diagnose_fingerprints.py

# Liberar puerto Arduino bloqueado
python scripts/liberar_puerto_arduino.py
```

## 🎯 Funcionalidades Principales

- Interfaces: Administrador, Instructor, Seguridad, Aseo, Administrativa, Programación, Registro de Huellas
- Módulos Core: Alertas, Controlador Arduino, Escáner Biométrico, Validador de Huellas, Gestor de Llaves, Validador de Roles, Sincronización de Huellas

## 📊 Base de Datos

- Base de datos: `sicefa`
- Tablas principales: `people`, `ambientes`, `programacion`, `huellas_digitales`

## 🤝 Contribución

1. Mantener la estructura de carpetas
2. Seguir las convenciones de imports
3. Documentar los cambios
4. Probar antes de hacer commit
