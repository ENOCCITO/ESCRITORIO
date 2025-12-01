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

### 2. Ejecutar la Aplicación

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
ESCRITORIO/
├── src/                     # Código fuente
│   ├── interfaces/          # Interfaces de usuario
│   ├── core/                # Lógica de negocio
│   ├── utils/               # Utilidades
│   └── config/              # Configuración
├── arduino/                 # Código Arduino
├── docs/                    # Documentación
├── data/                    # Datos exportados
├── assets/                  # Recursos gráficos
├── scripts/                 # Scripts de utilidad
├── main.py                  # Punto de entrada
└── requirements.txt         # Dependencias
```

📖 **Ver documentación completa:** [`ESTRUCTURA_PROYECTO.md`](ESTRUCTURA_PROYECTO.md)

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

Edita `src/config/config.py` para configurar:

- **Base de datos MySQL**
- **Puerto de Arduino**
- **Parámetros del sistema**

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_password',
    'database': 'sistema_llaves_v2'
}
```

## 📚 Documentación

### Documentación Principal
- [`ESTRUCTURA_PROYECTO.md`](ESTRUCTURA_PROYECTO.md) - Estructura detallada del proyecto
- [`RESUMEN_REORGANIZACION.md`](RESUMEN_REORGANIZACION.md) - Resumen de cambios de reorganización

### Documentación por Módulos
- [`docs/README.md`](docs/README.md) - Documentación general
- [`docs/README_BIOMETRICO.md`](docs/README_BIOMETRICO.md) - Sistema biométrico
- [`docs/README_ARDUINO_INTEGRATION.md`](docs/README_ARDUINO_INTEGRATION.md) - Integración Arduino
- [`docs/README_ALERTAS.md`](docs/README_ALERTAS.md) - Sistema de alertas
- [`docs/README_REGISTRO_HUELLAS.md`](docs/README_REGISTRO_HUELLAS.md) - Registro de huellas

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

### Interfaces de Usuario

1. **Interfaz de Administrador** - Gestión del sistema
2. **Interfaz de Instructor** - Gestión de instructores
3. **Interfaz de Seguridad** - Control de seguridad
4. **Interfaz de Aseo** - Gestión de limpieza
5. **Interfaz Administrativa** - Administración general
6. **Interfaz de Programación** - Gestión de horarios
7. **Registro de Huellas** - Registro biométrico

### Módulos Core

- **Sistema de Alertas** - Notificaciones del sistema
- **Controlador Arduino** - Integración con hardware
- **Escáner Biométrico** - Lectura de huellas
- **Validador de Huellas** - Verificación biométrica
- **Gestor de Llaves** - Control de llaves
- **Validador de Roles** - Control de acceso
- **Sincronización de Huellas** - Sync con BD

## 🔍 Troubleshooting

### Error de Imports

```bash
# Verificar que el entorno virtual esté activado
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Arduino

```bash
# Liberar puerto Arduino
python scripts/liberar_puerto_arduino.py

# Verificar conexión
python scripts/debug_arduino_complete.py
```

### Error de Base de Datos

```bash
# Diagnosticar BD
python scripts/diagnose_database_error.py

# Verificar configuración en src/config/config.py
```

## 📊 Base de Datos

### Tablas Principales

- **personal** - Información del personal
- **ambientes** - Ambientes/espacios
- **programacion** - Programación de accesos
- **huellas_digitales** - Datos biométricos

### Configuración de MySQL

```sql
CREATE DATABASE sistema_llaves_v2;
USE sistema_llaves_v2;

-- Las tablas se crean automáticamente al ejecutar el sistema
```

## 🎨 Assets y Recursos

Los recursos gráficos están en `assets/`:

- **images/** - Imágenes de la interfaz
- **idear.png** - Logo IDEAR
- **sena.png** - Logo SENA

## 📦 Datos Exportados

Los archivos CSV se guardan en `data/`:

- Programaciones
- Reportes
- Exportaciones del sistema

## 🔒 Seguridad

- Autenticación biométrica
- Control de roles y permisos
- Registro de auditoría
- Encriptación de datos sensibles

## 🤝 Contribución

Para contribuir al proyecto:

1. Mantener la estructura de carpetas
2. Seguir las convenciones de imports
3. Documentar los cambios
4. Probar antes de hacer commit

## 📝 Notas Importantes

1. **Usar un solo entorno virtual:** `.venv`
2. **No versionar archivos sensibles:** Credenciales en `.gitignore`
3. **Mantener documentación actualizada**
4. **Probar cambios antes de desplegar**

## 📞 Soporte

Para soporte técnico, consultar:

- Documentación en `docs/`
- Scripts de diagnóstico en `scripts/`
- Logs del sistema en archivos `.log`

## 📄 Licencia

[Especificar licencia del proyecto]

## 👥 Autores

[Especificar autores del proyecto]

---

**Última actualización:** 30 de noviembre de 2025  
**Versión del sistema:** 2.0  
**Python:** 3.12.10
