#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py
- Funciones auxiliares del sistema de dispensación biométrica
- Logging, base de datos, Arduino, y utilidades generales
"""

import json
import time
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from src.config.config import *

# ---- Sistema de logging profesional para dispenser.log ----
def log_file(msg: str):
    """
    Sistema de logging profesional que escribe en dispenser.log
    con formato timestamp y manejo de errores robusto
    """
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {msg}"
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
            f.flush()  # Asegurar que se escriba inmediatamente
        
        # También mostrar en consola para debugging
        print(f"📝 LOG: {formatted_message}")
        
    except PermissionError:
        print(f"❌ ERROR: No se puede escribir en {LOG_FILE} - Permisos insuficientes")
    except Exception as e:
        print(f"❌ ERROR en logging: {e}")
        # Intentar crear el archivo si no existe
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Archivo de log creado\n")
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except Exception:
            print("❌ ERROR CRÍTICO: No se puede crear ni escribir en el archivo de log")


def init_log_file():
    """
    Inicializa el archivo de log con información del sistema
    """
    try:
        import platform
        import os
        
        # Crear encabezado del log
        header = [
            "=" * 80,
            "🔐 SISTEMA DE DISPENSACIÓN BIOMÉTRICA - CEFA",
            "📋 ARCHIVO DE LOG DEL SISTEMA",
            f"📅 Fecha de inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"💻 Sistema operativo: {platform.system()} {platform.release()}",
            f"🐍 Versión Python: {platform.python_version()}",
            f"📁 Directorio de trabajo: {os.getcwd()}",
            "=" * 80,
            ""
        ]
        
        # Escribir encabezado
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            for line in header:
                f.write(line + "\n")
        
        log_file("🚀 SISTEMA DE LOGGING INICIADO CORRECTAMENTE")
        log_file("✅ Archivo dispenser.log creado y configurado")
        
    except Exception as e:
        print(f"❌ ERROR al inicializar archivo de log: {e}")


def log_system_info():
    """
    Registra información del sistema en el log
    """
    try:
        import platform
        import psutil
        
        system_info = [
            f"💻 Información del sistema: {platform.system()} {platform.release()}",
            f"🖥️ Arquitectura: {platform.machine()}",
            f"🐍 Python: {platform.python_version()}",
            f"💾 Memoria RAM: {psutil.virtual_memory().total // (1024**3)} GB",
            f"💿 Espacio en disco: {psutil.disk_usage('/').free // (1024**3)} GB libre"
        ]
        
        for info in system_info:
            log_file(info)
            
    except ImportError:
        log_file("⚠️ psutil no disponible - Información del sistema limitada")
    except Exception as e:
        log_file(f"❌ Error obteniendo información del sistema: {e}")


# --------- Imports diferidos para dependencias opcionales ----------
def _import_mysql():
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e


def _import_pyfingerprint():
    try:
        from pyfingerprint.pyfingerprint import (
            PyFingerprint,
            FINGERPRINT_CHARBUFFER1,
            FINGERPRINT_CHARBUFFER2,
        )
        return (PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2), None
    except Exception as e:
        return None, e


def _import_serial():
    try:
        import serial
        return serial, None
    except Exception as e:
        return None, e


# --------- Acceso BD (imports diferidos) ----------
def db_connect():
    mysql, err = _import_mysql()
    if not mysql:
        raise RuntimeError(f"Falta mysql-connector-python: {err}")
    return mysql.connect(**DB_CONFIG)


def load_candidates_from_db() -> List[Tuple[int, str, List[int]]]:
    """
    Carga candidatos (person_id, full_name, template_list[int]) de SICEFA.
    Usa la tabla 'people' de la base de datos SICEFA.
    Nota: Como SICEFA no tiene huella digital en la tabla people,
    retorna candidatos de ejemplo para desarrollo.
    """
    q = """
        SELECT p.id,
               CONCAT_WS(' ', p.first_name, p.first_last_name, p.second_last_name) AS full_name
        FROM people AS p
        WHERE p.deleted_at IS NULL
        LIMIT 100
    """
    out: List[Tuple[int, str, List[int]]] = []
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            cur.execute(q)
            for pid, full_name in cur.fetchall():
                try:
                    # Crear una plantilla simulada para desarrollo
                    # En producción, las huellas vendrían del hardware del sensor
                    template = [i % 256 for i in range(128)]  # Plantilla simulada de 128 bytes
                    out.append((int(pid), str(full_name or ""), template))
                    log_file(f"Candidato cargado: p.id={pid}, nombre={full_name}")
                except Exception as ex:
                    log_file(f"Error procesando candidato p.id={pid}: {ex}")
                    continue
            cur.close()
    except Exception as e:
        log_file(f"Error conectando a SICEFA: {e}")
        # Si no hay conexión, cargar candidatos de ejemplo
        out = create_sample_candidates()
    
    return out


def query_latest_environment(person_id: int) -> Optional[Tuple[int, str, int]]:
    """
    Retorna (ambiente_id, ambiente_nombre, angulo_grados) para la persona.
    Consulta la tabla environments (flujo SICEFA correcto) usando:
    - environments_instructor_programs para encontrar ambientes del instructor
    - environment_keys para obtener las llaves del ambiente
    - keys para obtener el ángulo de la llave
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Verificar si la persona existe en SICEFA
            cur.execute("SELECT id FROM people WHERE id = %s AND deleted_at IS NULL", (person_id,))
            if not cur.fetchone():
                log_file(f"Persona {person_id} no encontrada o eliminada")
                # Retornar un ambiente por defecto si no se encuentra la persona
                cur.execute("""
                    SELECT id, name
                    FROM environments 
                    WHERE deleted_at IS NULL
                    ORDER BY name
                    LIMIT 1
                """)
                ambiente = cur.fetchone()
                if ambiente:
                    ambiente_id, nombre = ambiente
                    return (ambiente_id, nombre, 90)
                return None
            
            # Consultar ambientes disponibles para el instructor
            cur.execute("""
                SELECT DISTINCT e.id, e.name
                FROM environments e
                INNER JOIN environment_keys ek ON e.id = ek.environment_id
                INNER JOIN keys k ON ek.key_id = k.id
                WHERE e.deleted_at IS NULL 
                AND k.status = 'DISPONIBLE'
                ORDER BY e.name
                LIMIT 1
            """)
            
            ambiente = cur.fetchone()
            if ambiente:
                ambiente_id, nombre = ambiente
                
                # Obtener el ángulo de la primera llave disponible
                cur.execute("""
                    SELECT k.angle_grados
                    FROM keys k
                    INNER JOIN environment_keys ek ON k.id = ek.key_id
                    WHERE ek.environment_id = %s AND k.status = 'DISPONIBLE'
                    LIMIT 1
                """, (ambiente_id,))
                key_result = cur.fetchone()
                angulo = key_result[0] if key_result else 90
                
                log_file(f"Ambiente asignado para persona {person_id}: {nombre} (ID: {ambiente_id}, Ángulo: {angulo}°)")
                cur.close()
                return (ambiente_id, nombre, angulo)
            else:
                log_file(f"No hay ambientes disponibles para persona {person_id}")
                cur.close()
                return None
            
    except Exception as e:
        log_file(f"Error consultando ambiente para persona {person_id}: {e}")
        return None


def get_available_environments() -> List[Tuple[int, str, str, str, str, str, str]]:
    """
    Retorna lista de ambientes disponibles en el sistema SICEFA.
    Usa la tabla 'environments' que es la correcta en el flujo de SICEFA.
    Retorna: [(id, name, description, length, latitude, farm_id, status)]
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Consulta simplificada - solo obtiene ambientes sin filtro de llaves
            cur.execute("""
                SELECT id, name, description, COALESCE(length, ''), COALESCE(latitude, ''), 
                       farm_id, status
                FROM environments 
                WHERE deleted_at IS NULL AND status = 'Disponible'
                ORDER BY name
            """)
            
            ambientes = cur.fetchall()
            cur.close()
            
            log_file(f"Obtenidos {len(ambientes)} ambientes disponibles")
            return ambientes
            
    except Exception as e:
        log_file(f"Error obteniendo ambientes disponibles: {e}")
        return []


def get_environment_by_id(ambiente_id: int) -> Optional[Tuple[int, str, str, str, str, str, str]]:
    """
    Obtiene información detallada de un ambiente específ ico por ID desde la tabla 'environments'.
    Retorna: (id, name, description, longitude, latitude, floor_id, status)
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            cur.execute("""
                SELECT id, name, description, longitude, latitude, floor_id, status
                FROM environments 
                WHERE id = %s AND deleted_at IS NULL
            """, (ambiente_id,))
            
            ambiente = cur.fetchone()
            cur.close()
            
            if ambiente:
                log_file(f"Ambiente {ambiente_id} obtenido: {ambiente[1]}")
                return ambiente
            else:
                log_file(f"Ambiente {ambiente_id} no encontrado")
                return None
            
    except Exception as e:
        log_file(f"Error obteniendo ambiente {ambiente_id}: {e}")
        return None


# --------- Arduino I/O (import diferido) ----------
def _open_serial_ready(arduino_port: str, baud: int, timeout: float):
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    ser = serial.Serial(arduino_port, baud, timeout=timeout)
    # Evitar reinicios: mantener líneas en bajo y no togglear
    try:
        ser.dtr = False
        ser.rts = False
    except Exception:
        pass
    # Dar tiempo a que Arduino esté listo
    time.sleep(0.6)
    # Vaciar buffers
    try:
        ser.reset_input_buffer(); ser.reset_output_buffer()
    except Exception:
        pass
    # Intentar obtener un STATUS rápido (no obligatorio)
    try:
        ser.write(b"STATUS\n"); ser.flush()
        t0 = time.time()
        while time.time() - t0 < 0.6:
            _ = ser.readline()
    except Exception:
        pass
    return ser


def send_home(arduino_port: str, baud: int, timeout: float = 10.0) -> str:
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    
    try:
        ser = _open_serial_ready(arduino_port, baud, timeout)
        time.sleep(0.3)
        ser.write(b"HOME\n"); ser.flush()
        # Leer todas las respuestas del Arduino
        t0 = time.time(); response = ""
        while time.time() - t0 < 5.0:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line:
                response += line + "\n"
        ser.close()
        return response.strip() or ""
    except Exception as e:
        print(f"❌ Error enviando HOME al Arduino: {e}")
        raise e


def open_key_angle(angle_deg: int, dwell_seconds: int, arduino_port: str, baud: int, timeout: float = 10.0) -> str:
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    
    try:
        ser = _open_serial_ready(arduino_port, baud, timeout)
        # Formatear grados con 2 decimales para evitar parsing extraño en Arduino
        cmd = f"OPEN {angle_deg:.2f} {int(dwell_seconds)}\n".encode("utf-8")
        time.sleep(0.2)
        ser.write(cmd); ser.flush()
        # Leer todas las respuestas del Arduino (hasta 8s)
        t0 = time.time(); response = ""
        while time.time() - t0 < (8.0 + max(0, int(dwell_seconds))):
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line:
                response += line + "\n"
                # cortar cuando vemos fin típico
                if "Movimiento completado" in line or "ERROR" in line:
                    break
        ser.close()
        print(f"🔍 Respuesta completa del Arduino: {response}")
        return response.strip() or ""
    except Exception as e:
        print(f"❌ Error enviando comando al Arduino: {e}")
        raise e


def degrees_to_steps(angle_deg: float) -> int:
    """Convierte grados a pasos efectivos considerando microstepping y reductora."""
    try:
        from src.config.config import STEPS_PER_REV, MICROSTEP_FACTOR, GEAR_RATIO
    except Exception:
        # Valores por defecto seguros
        STEPS_PER_REV = 200
        MICROSTEP_FACTOR = 1
        GEAR_RATIO = 1.0
    effective_steps = float(STEPS_PER_REV) * float(MICROSTEP_FACTOR) * float(GEAR_RATIO)
    return int(round((float(angle_deg) / 360.0) * effective_steps))


def move_steps(step_count: int, arduino_port: str, baud: int, timeout: float = 10.0) -> str:
    """Envía un movimiento directo por pasos (relativo). Acepta negativos."""
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    ser = _open_serial_ready(arduino_port, baud, timeout)
    try:
        cmd = f"STEPS {int(step_count)}\n".encode("utf-8")
        time.sleep(0.2)
        ser.write(cmd); ser.flush()
        # Leer respuesta con ventana corta (2.5s + factor por pasos, máx 8s)
        base = 2.5
        factor = abs(step_count) / 800.0
        t_limit = min(base + factor, 8.0)
        t0 = time.time(); response = ""
        while time.time() - t0 < t_limit:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line:
                response += line + "\n"
                if "Movimiento completado" in line or "ERROR" in line:
                    break
        return response.strip() or ""
    finally:
        try:
            ser.close()
        except Exception:
            pass


def open_key_by_id_steps(key_id: int, dwell_seconds: int = None, arduino_port: str = None, baud: int = None) -> bool:
    """Mueve el motor a la llave por pasos calculados desde ángulo BD.
    Flujo: mover pasos -> esperar -> mover pasos de regreso (simétrico)."""
    try:
        from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT, DEFAULT_DWELL
        from src.utils.db_utils import db_connect
        if arduino_port is None:
            arduino_port = ARDUINO_PORT_DEFAULT
        if baud is None:
            baud = ARDUINO_BAUD_DEFAULT
        if dwell_seconds is None:
            dwell_seconds = DEFAULT_DWELL
        # Consultar ángulo
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute("""
                SELECT codigo_llave, angulo_grados
                FROM llaves WHERE id = %s AND activo = 1
            """, (key_id,))
            row = cur.fetchone()
            cur.close()
        if not row:
            print(f"❌ Llave {key_id} no encontrada")
            return False
        angle = float(row.get('angulo_grados') or 0.0)
        steps = degrees_to_steps(angle)
        print(f"📐 Ángulo {angle:.2f}° → {steps} pasos")
        # Ir a posición
        resp1 = move_steps(steps, arduino_port, baud)
        ok1 = "Movimiento completado" in (resp1 or "")
        # Dwell
        if ok1 and dwell_seconds and dwell_seconds > 0:
            time.sleep(dwell_seconds)
        # Regresar de forma simétrica
        resp2 = move_steps(-steps, arduino_port, baud)
        ok2 = "Movimiento completado" in (resp2 or "")
        print(f"🔍 Ida: {resp1}\n🔍 Regreso: {resp2}")
        return ok1 and ok2
    except Exception as e:
        print(f"❌ Error open_key_by_id_steps({key_id}): {e}")
        return False


def open_key_by_id(key_id: int, dwell_seconds: int = None, arduino_port: str = None, baud: int = None) -> bool:
    """Abre una llave específica por ID obteniendo el ángulo desde la base de datos"""
    try:
        from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT, DEFAULT_DWELL
        from src.utils.db_utils import db_connect
        
        if arduino_port is None:
            arduino_port = ARDUINO_PORT_DEFAULT
        if baud is None:
            baud = ARDUINO_BAUD_DEFAULT
        if dwell_seconds is None:
            dwell_seconds = DEFAULT_DWELL
        
        # Obtener información de la llave desde la tabla 'keys' (flujo SICEFA correcto)
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            query = """
                SELECT id, key_code, status, angle_grados
                FROM keys 
                WHERE id = %s AND status = 'DISPONIBLE'
            """
            cur.execute(query, (key_id,))
            key_info = cur.fetchone()
            cur.close()
        
        if not key_info:
            print(f"❌ Llave {key_id} no encontrada o no disponible")
            log_file(f"Error: Llave {key_id} no encontrada o no disponible")
            return False
        
        degrees = key_info.get('angle_grados', 0)
        if degrees is None or degrees < 0 or degrees > 360:
            print(f"❌ Ángulo inválido para llave {key_id}: {degrees}")
            return False
        
        print(f"🔑 Abriendo llave {key_info['key_code']} - Ángulo: {degrees}°")
        
        # Enviar comando al Arduino
        response = open_key_angle(degrees, dwell_seconds, arduino_port, baud)
        
        if "Movimiento completado" in response:
            print(f"✅ Llave {key_info['key_code']} abierta exitosamente")
            log_file(f"✅ Llave {key_id} abierta - Ángulo: {degrees}°")
            
            # Registrar movimiento en key_movements (tabla del flujo SICEFA)
            try:
                with db_connect() as cnx:
                    cur = cnx.cursor()
                    cur.execute("""
                        INSERT INTO key_movements (key_id, status, angle_used, created_at)
                        VALUES (%s, 'COMPLETADO', %s, NOW())
                    """, (key_id, degrees))
                    cnx.commit()
                    cur.close()
            except Exception as e:
                log_file(f"Advertencia: No se pudo registrar movimiento en key_movements: {e}")
            
            # Retorno simétrico por pasos para no depender del estado interno del micro
            step_delta = degrees_to_steps(degrees)
            if dwell_seconds and dwell_seconds > 0:
                time.sleep(dwell_seconds)
            _ = move_steps(-step_delta, arduino_port, baud)
            return True
        else:
            print(f"❌ Error abriendo llave {key_id}: {response}")
            log_file(f"❌ Error abriendo llave {key_id}: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error abriendo llave {key_id}: {e}")
        log_file(f"❌ Error abriendo llave {key_id}: {e}")
        return False


def open_environment_key(environment_id: int, dwell_seconds: int = None, arduino_port: str = None, baud: int = None) -> bool:
    """Abre la llave de un ambiente específico usando la tabla 'environment_keys' del flujo SICEFA"""
    try:
        from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT, DEFAULT_DWELL
        
        if arduino_port is None:
            arduino_port = ARDUINO_PORT_DEFAULT
        if baud is None:
            baud = ARDUINO_BAUD_DEFAULT
        if dwell_seconds is None:
            dwell_seconds = DEFAULT_DWELL
        
        # Obtener llaves del ambiente desde environment_keys (tabla del flujo SICEFA)
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute("""
                SELECT k.id, k.key_code, k.angle_grados, k.status
                FROM keys k
                INNER JOIN environment_keys ek ON k.id = ek.key_id
                WHERE ek.environment_id = %s AND k.status = 'DISPONIBLE'
                LIMIT 1
            """, (environment_id,))
            key_info = cur.fetchone()
            cur.close()
        
        if not key_info:
            print(f"❌ No hay llaves disponibles para ambiente {environment_id}")
            log_file(f"Error: No hay llaves disponibles para ambiente {environment_id}")
            return False
        
        key_id = key_info['id']
        print(f"🏢 Abriendo llave del ambiente {environment_id} - Llave: {key_info['key_code']}")
        print(f"📐 Ángulo: {key_info['angle_grados']}°")
        
        return open_key_by_id(key_id, dwell_seconds, arduino_port, baud)
        
    except Exception as e:
        print(f"❌ Error abriendo llave del ambiente {environment_id}: {e}")
        log_file(f"❌ Error abriendo llave del ambiente {environment_id}: {e}")
        return False


def get_arduino_status(arduino_port: str = None, baud: int = None) -> Dict[str, Any]:
    """Obtiene el estado del Arduino"""
    try:
        from src.config.config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
        
        if arduino_port is None:
            arduino_port = ARDUINO_PORT_DEFAULT
        if baud is None:
            baud = ARDUINO_BAUD_DEFAULT
        
        serial, err = _import_serial()
        if not serial:
            return {'connected': False, 'error': f'PySerial no disponible: {err}'}
        
        try:
            with serial.Serial(arduino_port, baud, timeout=3.0) as ser:
                time.sleep(1)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(b"STATUS\n")
                ser.flush()
                
                response = ""
                start_time = time.time()
                while time.time() - start_time < 5.0:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode("utf-8", errors="ignore").strip()
                        if line:
                            response += line + "\n"
                    time.sleep(0.1)
                
                return {
                    'connected': True,
                    'port': arduino_port,
                    'baud': baud,
                    'response': response
                }
                
        except Exception as e:
            return {'connected': False, 'error': f'Error comunicándose con Arduino: {e}'}
            
    except Exception as e:
        return {'connected': False, 'error': str(e)}


# --------- Funciones de utilidad general ----------
def create_sample_candidates():
    """Crea candidatos de ejemplo para desarrollo y pruebas"""
    return SAMPLE_CANDIDATES


def get_users_from_database(candidates):
    """Obtiene usuarios desde la base de datos"""
    try:
        if candidates:
            users = []
            for pid, name, _ in candidates[:10]:  # Primeros 10 usuarios
                users.append({
                    'id': pid,
                    'name': name or f"Usuario {pid}",
                    'document': f"ID_{pid}"
                })
            return users
        else:
            return []
    except Exception:
        return []


def create_sample_users():
    """Crea usuarios de ejemplo si no hay base de datos"""
    return SAMPLE_USERS


def is_administrator(pid: int, name: str) -> bool:
    """Verifica si el usuario identificado es administrador"""
    # Aquí puedes implementar tu lógica para determinar si es administrador
    # Por ejemplo, consultar una tabla de roles en la base de datos
    
    # Por ahora, asumimos que es administrador si el ID es menor a 1000
    # o si el nombre contiene "admin" o "administrador"
    if pid < 1000:
        return True
    
    if name and any(keyword in name.lower() for keyword in ['admin', 'administrador', 'admin']):
        return True
    
    # También puedes consultar la base de datos para verificar el rol
    try:
        # Aquí podrías hacer una consulta SQL para verificar el rol
        # Por ejemplo: SELECT role FROM users WHERE id = %s
        pass
    except Exception:
        pass
    
    return False


def get_system_info():
    """Obtiene información del sistema en tiempo real"""
    try:
        import platform
        import psutil
        
        system_info = {
            'platform': f"{platform.system()} {platform.release()}",
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'version': platform.version(),
            'python_version': platform.python_version(),
            'python_executable': platform.sys.executable,
            'python_compiler': platform.python_compiler(),
            'memory_total': psutil.virtual_memory().total // (1024**3),
            'memory_used': psutil.virtual_memory().used // (1024**3),
            'memory_free': psutil.virtual_memory().free // (1024**3),
            'memory_percent': psutil.virtual_memory().percent,
            'cpu_cores': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            'disk_total': psutil.disk_usage('/').total // (1024**3),
            'disk_used': psutil.disk_usage('/').used // (1024**3),
            'disk_free': psutil.disk_usage('/').free // (1024**3),
            'disk_percent': psutil.disk_usage('/').percent,
            'network_interfaces': len(psutil.net_if_addrs()),
            'network_connections': len(psutil.net_connections()),
            'processes_total': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return system_info
        
    except ImportError:
        return {'error': 'psutil no disponible'}
    except Exception as e:
        return {'error': str(e)}


def export_to_csv(data, filename, headers=None):
    """Exporta datos a un archivo CSV"""
    try:
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if headers:
                writer.writerow(headers)
            
            for row in data:
                writer.writerow(row)
        
        return True
        
    except Exception as e:
        log_file(f"❌ Error exportando a CSV: {e}")
        return False


def open_file(filename):
    """Abre un archivo con el programa predeterminado del sistema"""
    try:
        import platform
        
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}")
        else:  # Linux
            os.system(f"xdg-open {filename}")
        
        return True
        
    except Exception as e:
        log_file(f"❌ Error abriendo archivo: {e}")
        return False


def get_dependency_status():
    """Verifica y reporta el estado de las dependencias del sistema"""
    missing = []
    dependencies_status = {}
    
    # Verificar MySQL
    mysql_mod, mysql_err = _import_mysql()
    if mysql_mod:
        dependencies_status["MySQL"] = "✅ Disponible"
        log_file("✅ MySQL Connector: Disponible y operativo")
    else:
        missing.append("mysql-connector-python")
        dependencies_status["MySQL"] = "❌ No disponible"
        log_file(f"❌ MySQL Connector: No disponible - {mysql_err}")
    
    # Verificar PyFingerprint
    fp_mod, fp_err = _import_pyfingerprint()
    if fp_mod:
        dependencies_status["PyFingerprint"] = "✅ Disponible"
        log_file("✅ PyFingerprint: Disponible y operativo")
    else:
        missing.append("pyfingerprint")
        dependencies_status["PyFingerprint"] = "❌ No disponible"
        log_file(f"❌ PyFingerprint: No disponible - {fp_err}")
    
    # Verificar PySerial
    serial_mod, serial_err = _import_serial()
    if serial_mod:
        dependencies_status["PySerial"] = "✅ Disponible"
        log_file("✅ PySerial: Disponible y operativo")
    else:
        missing.append("pyserial")
        dependencies_status["PySerial"] = "❌ No disponible"
        log_file(f"❌ PySerial: No disponible - {serial_err}")
    
    return missing, dependencies_status
