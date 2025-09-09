# 🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - sistema_llaves_v2

## 📋 Descripción General

Este sistema ha sido actualizado para trabajar con la base de datos **`sistema_llaves_v2`** que contiene:

- **Personal** con huellas digitales registradas
- **Tipos de personal** con diferentes niveles de permisos
- **Llaves** organizadas por módulos y posiciones
- **Ambientes** para asignación de llaves
- **Sistema de logs** para auditoría completa

## 🗄️ Estructura de la Base de Datos

### Tabla `personal`
- Información completa del personal
- Huellas digitales almacenadas como `LONGBLOB`
- Relación con `tipos_personal` para permisos
- Campos de auditoría (`created_at`, `updated_at`, `deleted_at`)

### Tabla `tipos_personal`
- **ADMINISTRADOR**: 5 llaves por día, permisos especiales ✅
- **ADMINISTRATIVO**: 2 llaves por día, permisos estándar
- **INSTRUCTOR**: 1 llave por día, acceso limitado
- **LIMPIEZA**: 0 llaves por día, permisos especiales ✅
- **SEGURIDAD**: 0 llaves por día, permisos especiales ✅

### Tabla `llaves`
- Organización por módulos (M1, M2, M3, M4)
- Posiciones circulares con ángulos específicos
- Estados: DISPONIBLE, ASIGNADA, PERDIDA, MANTENIMIENTO
- Tipos: MAESTRA, NORMAL, EMERGENCIA

### Tabla `ambientes`
- Información de espacios físicos
- Estados: DISPONIBLE, MANTENIMIENTO, OCUPADO, INACTIVO
- Capacidad y ubicación

### Tabla `asignaciones_llaves`
- Control de préstamos de llaves
- Estados: ACTIVA, DEVUELTA, VENCIDA, PERDIDA
- Fechas de asignación y devolución

### Tabla `logs_acceso`
- Auditoría completa de accesos
- Tipos: ENTRADA, SALIDA, ENTREGA_LLAVE, DEVOLUCION_LLAVE
- Calidad de huella y éxito de operación

## 🚀 Archivos del Sistema

### `config.py`
- Configuración de la base de datos `sistema_llaves_v2`
- Parámetros de puertos y configuración del sistema

### `db_utils.py`
- Utilidades para conexión y consultas a la base de datos
- Funciones para gestionar personal, llaves y ambientes
- Sistema de logs y auditoría

### `fingerprint_validator.py`
- Validador de huellas digitales
- Autenticación biométrica contra la base de datos
- Verificación de permisos y límites diarios

### `key_manager.py`
- Gestor completo de llaves
- Asignación y devolución de llaves
- Control de permisos y límites

### `test_database.py`
- Script de prueba para validar la conexión
- Verificación de todas las tablas y datos

### `explore_tables.py`
- Explorador de estructura de tablas
- Análisis detallado de esquemas

## 🔧 Instalación y Configuración

### 1. Requisitos Previos
```bash
pip install mysql-connector-python
pip install pyfingerprint
pip install pyserial
```

### 2. Configuración de Base de Datos
- Asegúrate de que MySQL esté ejecutándose
- La base de datos `sistema_llaves_v2` debe estar creada
- Usuario `root` sin contraseña (configurable en `config.py`)

### 3. Configuración de Puertos
```python
# En config.py
FINGERPRINT_PORT_DEFAULT = "COM3"  # Puerto del sensor de huellas
ARDUINO_PORT_DEFAULT = "COM8"      # Puerto del Arduino para dispensador
```

## 📱 Uso del Sistema

### 1. Prueba de Conexión
```bash
python test_database.py
```
Verifica que la conexión a la base de datos funcione correctamente.

### 2. Exploración de Estructura
```bash
python explore_tables.py
```
Analiza la estructura exacta de todas las tablas.

### 3. Gestión de Llaves
```bash
python key_manager.py
```
Muestra información general y permite gestionar llaves.

### 4. Validación Biométrica
```bash
python fingerprint_validator.py
```
Sistema completo de autenticación por huellas.

## 🔐 Flujo de Trabajo

### Autenticación
1. Usuario coloca dedo en sensor
2. Sistema valida huella contra base de datos
3. Se verifica tipo de personal y permisos
4. Se registra acceso en logs

### Asignación de Llaves
1. Usuario autenticado solicita llave
2. Sistema verifica límite diario
3. Se asigna llave disponible
4. Se actualiza estado y se registra en logs

### Devolución de Llaves
1. Usuario devuelve llave
2. Sistema marca asignación como devuelta
3. Llave vuelve a estado disponible
4. Se registra devolución en logs

## 📊 Características del Sistema

### ✅ Funcionalidades Implementadas
- Conexión a base de datos MySQL
- Validación biométrica de huellas
- Gestión completa de llaves
- Control de permisos por tipo de personal
- Sistema de logs y auditoría
- Límites diarios de llaves por usuario
- Estados de llaves y ambientes

### 🔄 Funcionalidades en Desarrollo
- Interfaz gráfica integrada
- Control de Arduino para dispensador
- Programación automática de horarios
- Reportes y estadísticas
- Notificaciones y alertas

## 🛠️ Personalización

### Agregar Nuevos Tipos de Personal
1. Insertar en tabla `tipos_personal`
2. Definir `max_llaves_por_dia`
3. Configurar `permisos_especiales`

### Configurar Nuevos Ambientes
1. Insertar en tabla `ambientes`
2. Definir capacidad y ubicación
3. Establecer estado inicial

### Modificar Límites de Llaves
1. Actualizar `max_llaves_por_dia` en `tipos_personal`
2. Los cambios se aplican inmediatamente

## 📝 Logs y Auditoría

El sistema registra automáticamente:
- **Accesos biométricos** exitosos y fallidos
- **Asignaciones** y **devoluciones** de llaves
- **Calidad** de las huellas escaneadas
- **IP** y **timestamp** de cada operación
- **Observaciones** y **notas** de cada transacción

## 🔒 Seguridad

- **Autenticación biométrica** obligatoria
- **Verificación de permisos** por tipo de usuario
- **Límites diarios** para prevenir abusos
- **Logs completos** para auditoría
- **Estados de llaves** para control de inventario

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema:
- Revisar logs en `dispenser.log`
- Verificar conexión a base de datos
- Comprobar configuración de puertos
- Validar permisos de usuario MySQL

---

**🎯 Sistema actualizado y funcionando con `sistema_llaves_v2`**
**✅ Base de datos integrada y validada**
**🔐 Sistema biométrico operativo**
**🔑 Gestión de llaves completamente funcional**
