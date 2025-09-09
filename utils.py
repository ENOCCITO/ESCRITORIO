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
from typing import List, Tuple, Optional
from config import *

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
    (person_id, full_name, template_list[int]) de personas con huella digital
    y activas en el sistema. Las huellas están en formato binario del sensor.
    """
    q = """
        SELECT DISTINCT p.id,
               CONCAT_WS(' ', p.nombres, p.apellidos) AS full_name,
               p.huella_digital
        FROM personal AS p
        WHERE p.huella_digital IS NOT NULL
          AND p.activo = 1
    """
    out: List[Tuple[int, str, List[int]]] = []
    with db_connect() as cnx:
        cur = cnx.cursor()
        cur.execute(q)
        for pid, full_name, bio in cur.fetchall():
            try:
                if isinstance(bio, (bytes, bytearray)):
                    # Las huellas están en formato binario del sensor
                    # Convertir bytes a lista de enteros para compatibilidad
                    template = list(bio)
                    if template:  # Verificar que no esté vacía
                        out.append((int(pid), str(full_name or ""), template))
                        log_file(f"Huella cargada para p.id={pid}: {len(template)} bytes")
                    else:
                        log_file(f"Huella vacía para p.id={pid}")
                else:
                    log_file(f"Formato de huella inesperado para p.id={pid}: {type(bio)}")
            except Exception as ex:
                log_file(f"Error procesando huella p.id={pid}: {ex}")
                continue
        cur.close()
    return out


def query_latest_environment(person_id: int) -> Optional[Tuple[int, str, int]]:
    """
    Retorna (ambiente_id, ambiente_nombre, angulo_grados) para la persona.
    Consulta la tabla ambientes para obtener información real del sistema.
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Verificar si la persona existe y tiene acceso
            cur.execute("SELECT id FROM personal WHERE id = %s AND activo = 1", (person_id,))
            if not cur.fetchone():
                log_file(f"Persona {person_id} no encontrada o inactiva")
                return None
            
            # Consultar ambientes disponibles y activos
            cur.execute("""
                SELECT id, nombre, capacidad, ubicacion, piso, edificio, estado
                FROM ambientes 
                WHERE activo = 1 
                ORDER BY nombre
                LIMIT 1
            """)
            
            ambiente = cur.fetchone()
            if ambiente:
                ambiente_id, nombre, capacidad, ubicacion, piso, edificio, estado = ambiente
                
                # Construir nombre descriptivo del ambiente
                nombre_completo = nombre
                if ubicacion:
                    nombre_completo += f" - {ubicacion}"
                if piso:
                    nombre_completo += f" (Piso {piso})"
                if edificio:
                    nombre_completo += f" - {edificio}"
                
                # Por ahora usamos un ángulo por defecto (90 grados)
                # En el futuro se puede implementar lógica más compleja con asignaciones
                angulo = 90
                
                log_file(f"Ambiente asignado para persona {person_id}: {nombre_completo} (ID: {ambiente_id})")
                cur.close()
                return (ambiente_id, nombre_completo, angulo)
            else:
                log_file(f"No hay ambientes disponibles para persona {person_id}")
                cur.close()
                return None
            
    except Exception as e:
        log_file(f"Error consultando ambiente para persona {person_id}: {e}")
        return None


def get_available_environments() -> List[Tuple[int, str, str, str, str, str, str]]:
    """
    Retorna lista de ambientes disponibles en el sistema.
    Retorna: [(id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio)]
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            cur.execute("""
                SELECT id, nombre, descripcion, tipo_ambiente, ubicacion, piso, edificio
                FROM ambientes 
                WHERE activo = 1 
                ORDER BY nombre
            """)
            
            ambientes = cur.fetchall()
            cur.close()
            
            log_file(f"Obtenidos {len(ambientes)} ambientes disponibles")
            return ambientes
            
    except Exception as e:
        log_file(f"Error obteniendo ambientes disponibles: {e}")
        return []


def get_environment_by_id(ambiente_id: int) -> Optional[Tuple[int, str, str, str, str, str, str, str]]:
    """
    Obtiene información detallada de un ambiente específico por ID.
    Retorna: (id, nombre, descripcion, tipo_ambiente, capacidad, ubicacion, piso, edificio)
    """
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            cur.execute("""
                SELECT id, nombre, descripcion, tipo_ambiente, capacidad, ubicacion, piso, edificio
                FROM ambientes 
                WHERE id = %s AND activo = 1
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
def send_home(arduino_port: str, baud: int, timeout: float = 10.0) -> str:
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    with serial.Serial(arduino_port, baud, timeout=timeout) as ser:
        time.sleep(1.2)
        ser.reset_input_buffer(); ser.reset_output_buffer()
        ser.write(b"HOME\n"); ser.flush()
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        return line or ""


def open_key_angle(angle_deg: int, dwell_seconds: int, arduino_port: str, baud: int, timeout: float = 10.0) -> str:
    serial, err = _import_serial()
    if not serial:
        raise RuntimeError(f"Falta pyserial: {err}")
    cmd = f"OPEN {angle_deg} {dwell_seconds}\n".encode("utf-8")
    with serial.Serial(arduino_port, baud, timeout=timeout) as ser:
        time.sleep(1.2)
        ser.reset_input_buffer(); ser.reset_output_buffer()
        ser.write(cmd); ser.flush()
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        return line or ""


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
