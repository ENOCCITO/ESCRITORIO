# 🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA

Sistema avanzado de control de acceso mediante autenticación biométrica por huella digital, reestructurado para seguir las mejores prácticas de programación.

## 📁 ESTRUCTURA DEL PROYECTO

El proyecto ha sido reorganizado en módulos separados para mejorar la mantenibilidad y seguir las mejores prácticas de programación:

```
llaves_escritorio/
├── main.py                           # Archivo principal de la aplicación
├── config.py                         # Configuración centralizada del sistema
├── styles.py                         # Estilos y configuración de la interfaz gráfica
├── utils.py                          # Funciones auxiliares y utilidades del sistema
├── admin_interface.py                # Interfaz de administrador
├── instructor_interface.py           # Interfaz de instructor
├── security_interface.py             # Interfaz de seguridad
├── cleaning_interface.py             # Interfaz de aseo
├── administrative_interface.py       # Interfaz administrativa
├── schedule_interface.py             # Interfaz de programación
├── dispenser.log                     # Archivo de log del sistema
└── README.md                         # Este archivo
```

## 🚀 CARACTERÍSTICAS PRINCIPALES

### 🔐 Autenticación Biométrica
- Captura de huella digital en tiempo real
- Verificación contra base de datos SICEFA
- Control de acceso basado en roles y permisos
- Sistema de logging completo

### 👥 Interfaz de Usuarios
- **ADMINISTRADOR**: Acceso completo al sistema
- **INSTRUCTOR**: Gestión de aulas y laboratorios
- **SEGURIDAD**: Monitoreo y control de acceso
- **ASEO**: Gestión de limpieza y mantenimiento
- **ADMINISTRATIVO**: Gestión administrativa del campus
- **PROGRAMACIÓN**: Visualización de horarios y programación

### 🎨 Interfaz Gráfica
- Tema futurista con colores azules y cian
- Efectos de hover y animaciones
- Diseño responsivo y moderno
- Interfaz intuitiva y fácil de usar

## 🛠️ INSTALACIÓN Y CONFIGURACIÓN

### Requisitos del Sistema
- Python 3.7 o superior
- Tkinter (incluido con Python)
- MySQL Connector para Python (opcional)
- PyFingerprint (opcional)
- PySerial (opcional)

### Instalación de Dependencias
```bash
pip install mysql-connector-python
pip install pyfingerprint
pip install pyserial
pip install psutil
```

### Configuración
1. Edita `config.py` para configurar tu base de datos y puertos
2. Asegúrate de que el lector biométrico esté conectado
3. Verifica la conexión a la base de datos MySQL

## 🚀 EJECUCIÓN

Para ejecutar el sistema:

```bash
python main.py
```

## 📋 FUNCIONALIDADES POR MÓDULO

### 🔧 `config.py`
- Configuración centralizada de la base de datos
- Parámetros del sistema (puertos, umbrales, timeouts)
- Configuración de la interfaz gráfica
- Constantes del sistema

### 🎨 `styles.py`
- Estilos y temas de la interfaz gráfica
- Funciones para crear widgets estilizados
- Configuración de colores y fuentes
- Efectos visuales y animaciones

### ⚙️ `utils.py`
- Funciones de logging del sistema
- Conexión a base de datos
- Comunicación con Arduino
- Funciones auxiliares generales

### 👨‍💼 `admin_interface.py`
- Gestión de ambientes del campus
- Registro de huellas digitales
- Control de usuarios y permisos
- Configuración del sistema

### 👨‍🏫 `instructor_interface.py`
- Visualización de horarios de clases
- Acceso a aulas y laboratorios
- Reportes de actividades académicas
- Gestión de recursos educativos

### 🛡️ `security_interface.py`
- Monitoreo en tiempo real del campus
- Control de puntos de acceso
- Reportes de seguridad
- Gestión de cámaras y vigilancia

### 🧹 `cleaning_interface.py`
- Programación de limpieza del campus
- Control de mantenimiento
- Reportes de limpieza
- Gestión de personal de aseo

### 📋 `administrative_interface.py`
- Gestión de personal del campus
- Control de recursos
- Reportes administrativos
- Gestión financiera

### 📅 `schedule_interface.py`
- Visualización de programación del sistema
- Horarios de operación
- Información de categorías de usuarios
- Exportación de programación

## 🔐 SISTEMA DE AUTENTICACIÓN

### Flujo de Autenticación
1. **Captura de Huella**: El usuario coloca su dedo en el lector biométrico
2. **Verificación**: El sistema compara la huella con la base de datos
3. **Identificación**: Se determina el rol y permisos del usuario
4. **Acceso**: Se concede acceso según el rol identificado

### Roles y Permisos
- **Administrador**: Acceso completo a todas las funcionalidades
- **Instructor**: Acceso a aulas y recursos educativos
- **Seguridad**: Acceso a sistemas de vigilancia y control
- **Aseo**: Acceso a áreas de limpieza y mantenimiento
- **Administrativo**: Acceso a sistemas administrativos

## 📊 LOGGING Y MONITOREO

### Sistema de Logs
- Archivo `dispenser.log` con timestamp
- Registro de todas las operaciones del sistema
- Información de errores y eventos
- Estadísticas de uso del sistema

### Monitoreo en Tiempo Real
- Estado del sistema en tiempo real
- Contadores de operaciones
- Información de rendimiento
- Alertas y notificaciones

## 🔧 MANTENIMIENTO Y SOPORTE

### Mantenimiento Preventivo
- Verificación automática de dependencias
- Monitoreo de recursos del sistema
- Respaldo automático de datos
- Actualizaciones del sistema

### Soporte Técnico
- Sistema de notificaciones integrado
- Reportes de errores detallados
- Documentación completa del sistema
- Herramientas de diagnóstico

## 📈 BENEFICIOS DE LA REESTRUCTURACIÓN

### ✅ Mejoras Implementadas
- **Modularidad**: Código organizado en módulos específicos
- **Mantenibilidad**: Fácil mantenimiento y actualización
- **Escalabilidad**: Estructura preparada para futuras expansiones
- **Reutilización**: Componentes reutilizables entre módulos
- **Legibilidad**: Código más claro y fácil de entender

### 🎯 Mejores Prácticas Aplicadas
- Separación de responsabilidades
- Configuración centralizada
- Manejo de errores robusto
- Documentación completa
- Estructura de archivos organizada

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problemas Comunes
1. **Error de conexión a la base de datos**: Verifica la configuración en `config.py`
2. **Lector biométrico no detectado**: Verifica la conexión del puerto COM
3. **Error de dependencias**: Instala las librerías requeridas con pip

### Logs de Error
- Revisa el archivo `dispenser.log` para errores detallados
- Los errores se muestran también en la consola
- El sistema mantiene un historial completo de eventos

## 📞 CONTACTO Y SOPORTE

Para soporte técnico o reportar problemas:
- Revisa la documentación en este README
- Consulta los logs del sistema
- Contacta al administrador del sistema

## 🔄 ACTUALIZACIONES FUTURAS

### Próximas Mejoras
- Interfaz web adicional
- Aplicación móvil
- Integración con más sistemas
- Análisis avanzado de datos
- Reportes automatizados

### Contribuciones
- El código está estructurado para facilitar contribuciones
- Cada módulo es independiente y puede ser modificado
- Se mantiene compatibilidad con versiones anteriores

---

**🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA**  
*Control de Acceso por Huella Digital*  
*Versión 2.0 - Interfaz Futurista*
