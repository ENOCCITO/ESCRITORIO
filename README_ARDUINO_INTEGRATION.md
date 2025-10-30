# 🤖 INTEGRACIÓN ARDUINO - Sistema de Llaves CEFA

## 📋 Descripción

Este documento describe la integración completa entre el sistema Python y Arduino para controlar un motor paso a paso NEMA17 que maneja la dispensación de llaves físicas.

## 🔧 Hardware Requerido

### Arduino y Motor
- **Arduino Uno/Nano/Mega** con puerto USB
- **Motor paso a paso NEMA17** (200 pasos/vuelta, 1.8°/paso)
- **Driver L298N** para control del motor
- **Fuente de alimentación** 12V para el motor
- **Cables de conexión**

### Conexiones L298N → Arduino
```
L298N    →    Arduino
IN1      →    Pin 8
IN2      →    Pin 9  
IN3      →    Pin 10
IN4      →    Pin 11
VCC      →    5V
GND      →    GND
```

### Conexiones Motor NEMA17 → L298N
```
Motor    →    L298N
A+       →    OUT1
A-       →    OUT2
B+       →    OUT3
B-       →    OUT4
```

## 💾 Software Requerido

### Python
```bash
pip install pyserial mysql-connector-python
```

### Arduino IDE
- Instalar Arduino IDE
- Cargar el código `arduino_nema17_controller.ino`

## 🗄️ Base de Datos

### Estructura de la tabla `llaves`
```sql
CREATE TABLE llaves (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo_llave VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    ambiente_id INT,
    estado ENUM('DISPONIBLE', 'ASIGNADA', 'PERDIDA', 'MANTENIMIENTO'),
    angulo_grados INT,  -- Ángulo en grados (0-360)
    modulo VARCHAR(20),
    posicion_circular INT,
    tipo_llave ENUM('MAESTRA', 'NORMAL', 'EMERGENCIA'),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Ejemplo de datos
```sql
INSERT INTO llaves (codigo_llave, descripcion, ambiente_id, angulo_grados, estado) VALUES
('A101', 'Llave Aula 101', 1, 45, 'DISPONIBLE'),
('A102', 'Llave Aula 102', 2, 90, 'DISPONIBLE'),
('A103', 'Llave Aula 103', 3, 135, 'DISPONIBLE'),
('L201', 'Llave Laboratorio 201', 4, 180, 'DISPONIBLE'),
('L202', 'Llave Laboratorio 202', 5, 225, 'DISPONIBLE');
```

## 🚀 Instalación y Configuración

### 1. Configurar Arduino
1. Abrir Arduino IDE
2. Cargar el código `arduino_nema17_controller.ino`
3. Verificar que el puerto COM sea correcto
4. Subir el código al Arduino
5. Abrir Monitor Serie (115200 baud) para verificar funcionamiento

### 2. Configurar Python
1. Instalar dependencias:
```bash
pip install pyserial mysql-connector-python
```

2. Configurar puerto en `config.py`:
```python
ARDUINO_PORT_DEFAULT = "COM8"  # Cambiar por tu puerto
ARDUINO_BAUD_DEFAULT = 115200
```

3. Configurar base de datos en `config.py`:
```python
DB_CONFIG = dict(
    host="localhost", 
    user="root", 
    password="", 
    database="sistema_llaves_v2"
)
```

### 3. Probar Integración
```bash
python test_arduino_integration.py
```

## 📚 API de Funciones

### Funciones Principales

#### `open_key_by_id(key_id, dwell_seconds=None)`
Abre una llave específica por ID obteniendo el ángulo desde la base de datos.

```python
from utils import open_key_by_id

# Abrir llave ID 1 por 5 segundos
success = open_key_by_id(1, dwell_seconds=5)
```

#### `open_environment_key(environment_id, dwell_seconds=None)`
Abre la llave de un ambiente específico.

```python
from utils import open_environment_key

# Abrir llave del ambiente 1 por 3 segundos
success = open_environment_key(1, dwell_seconds=3)
```

#### `get_arduino_status()`
Obtiene el estado actual del Arduino.

```python
from utils import get_arduino_status

status = get_arduino_status()
print(f"Conectado: {status['connected']}")
print(f"Posición: {status.get('position', 'N/A')} grados")
```

### Clase ArduinoController

Para control más avanzado, usa la clase `ArduinoController`:

```python
from arduino_controller import ArduinoController

# Crear controlador
controller = ArduinoController()

# Conectar
if controller.connect():
    # Mover a llave específica
    controller.move_to_key_position(key_id=1, dwell_seconds=5)
    
    # Mover a ambiente
    controller.move_to_environment(environment_id=1)
    
    # Obtener estado
    status = controller.get_motor_status()
    
    # Desconectar
    controller.disconnect()
```

## 🔄 Flujo de Trabajo

### 1. Autenticación Biométrica
```
Usuario → Escanea huella → Sistema valida → Acceso concedido
```

### 2. Selección de Llave
```
Usuario → Selecciona ambiente/llave → Sistema obtiene ángulo de BD
```

### 3. Control del Motor
```
Sistema → Envía comando OPEN <grados> <tiempo> → Arduino → Motor se mueve
```

### 4. Registro de Acceso
```
Sistema → Registra en logs_acceso → Actualiza estado de llave
```

## 🧪 Pruebas

### Prueba Básica
```bash
python test_arduino_integration.py
```

### Prueba Manual
```python
from utils import open_key_angle, send_home

# Home
send_home("COM8", 115200)

# Mover a 90 grados por 3 segundos
open_key_angle(90, 3, "COM8", 115200)
```

### Prueba con Base de Datos
```python
from utils import open_key_by_id

# Abrir llave ID 1
open_key_by_id(1, dwell_seconds=5)
```

## ⚙️ Comandos Arduino

### Comandos Disponibles
- `HOME` - Mover a posición inicial (0°)
- `OPEN <grados> <tiempo>` - Mover a posición específica
- `STATUS` - Estado actual del motor
- `RESET` - Resetear posición

### Ejemplos de Comandos
```
HOME
OPEN 90 5
OPEN 180 3
STATUS
RESET
```

## 🔧 Configuración Avanzada

### Velocidad del Motor
En el código Arduino, modifica `STEP_DELAY`:
```cpp
const int STEP_DELAY = 2000;  // Microsegundos entre pasos
// Menor valor = más rápido
// Mayor valor = más lento
```

### Precisión del Motor
```cpp
const int STEPS_PER_REVOLUTION = 200;  // Pasos por vuelta
const int STEPS_PER_DEGREE = STEPS_PER_REVOLUTION / 360;  // Pasos por grado
```

### Límites de Movimiento
```cpp
const int MAX_STEPS = STEPS_PER_REVOLUTION * 2;  // Máximo 2 vueltas
```

## 🐛 Solución de Problemas

### Arduino no responde
1. Verificar puerto COM en `config.py`
2. Verificar que Arduino esté conectado
3. Verificar que el código esté cargado
4. Verificar velocidad de baudios (115200)

### Motor no se mueve
1. Verificar conexiones L298N
2. Verificar alimentación 12V
3. Verificar pines de control (8-11)
4. Verificar que ENABLE esté en HIGH

### Base de datos no conecta
1. Verificar MySQL ejecutándose
2. Verificar credenciales en `config.py`
3. Verificar que la base de datos existe
4. Verificar que la tabla `llaves` existe

### Ángulos incorrectos
1. Verificar datos en la tabla `llaves`
2. Verificar que `angulo_grados` esté entre 0-360
3. Verificar que la llave esté en estado 'DISPONIBLE'

## 📊 Monitoreo y Logs

### Logs del Sistema
Los logs se guardan en `dispenser.log`:
```
✅ Arduino conectado en COM8
✅ Llave 1 abierta - Ángulo: 45°
🔑 Moviendo a llave 2 - Ángulo: 90°
```

### Estado del Motor
```python
status = get_arduino_status()
print(status['response'])
```

## 🔒 Seguridad

### Validaciones
- Verificar que la llave esté disponible
- Verificar permisos del usuario
- Verificar límites de tiempo
- Registrar todos los accesos

### Logs de Auditoría
- Todos los movimientos se registran
- Timestamp de cada operación
- Usuario que realizó la acción
- Resultado de la operación

## 📞 Soporte

Para problemas técnicos:
1. Revisar logs en `dispenser.log`
2. Verificar conexiones hardware
3. Probar con `test_arduino_integration.py`
4. Verificar configuración en `config.py`

## 🎯 Próximas Mejoras

- [ ] Control de velocidad variable
- [ ] Calibración automática
- [ ] Detección de obstáculos
- [ ] Interfaz web para monitoreo
- [ ] Notificaciones por email
- [ ] Backup automático de configuración
