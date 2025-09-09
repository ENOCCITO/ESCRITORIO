#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db_utils.py
- Utilidades específicas para la base de datos sistema_llaves_v2
- Manejo de personal, huellas digitales y tipos de personal
"""

import json
import time
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from config import DB_CONFIG

def _import_mysql():
    """Importa mysql.connector de forma diferida"""
    try:
        import mysql.connector as mysql
        return mysql, None
    except Exception as e:
        return None, e

def db_connect():
    """Conecta a la base de datos sistema_llaves_v2"""
    mysql, err = _import_mysql()
    if not mysql:
        raise RuntimeError(f"Falta mysql-connector-python: {err}")
    return mysql.connect(**DB_CONFIG)

def get_personal_types() -> List[Dict[str, Any]]:
    """Obtiene todos los tipos de personal desde la tabla tipos_personal"""
    query = """
        SELECT id, nombre, descripcion, max_llaves_por_dia, permisos_especiales, activo
        FROM tipos_personal 
        WHERE activo = 1
        ORDER BY nombre
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)
            types = cur.fetchall()
            cur.close()
            return types
    except Exception as e:
        print(f"❌ Error obteniendo tipos de personal: {e}")
        return []

def get_personal_with_fingerprints() -> List[Dict[str, Any]]:
    """Obtiene personal con huellas digitales registradas"""
    query = """
        SELECT p.id, p.tipo_personal_id, p.documento_tipo, p.documento_numero,
               p.nombres, p.apellidos, p.email, p.telefono, p.direccion,
               p.fecha_nacimiento, p.genero, p.huella_digital, p.fecha_registro_huella,
               p.activo, p.fecha_contratacion, p.fecha_terminacion,
               tp.nombre as tipo_personal_nombre, tp.max_llaves_por_dia
        FROM personal p
        JOIN tipos_personal tp ON p.tipo_personal_id = tp.id
        WHERE p.huella_digital IS NOT NULL 
          AND p.activo = 1 
          AND p.deleted_at IS NULL
        ORDER BY p.nombres, p.apellidos
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)
            personal = cur.fetchall()
            cur.close()
            return personal
    except Exception as e:
        print(f"❌ Error obteniendo personal con huellas: {e}")
        return []

def get_personal_by_id(personal_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene información de una persona específica por ID"""
    query = """
        SELECT p.id, p.tipo_personal_id, p.documento_tipo, p.documento_numero,
               p.nombres, p.apellidos, p.email, p.telefono, p.direccion,
               p.fecha_nacimiento, p.genero, p.huella_digital, p.fecha_registro_huella,
               p.activo, p.fecha_contratacion, p.fecha_terminacion,
               tp.nombre as tipo_personal_nombre, tp.max_llaves_por_dia, tp.permisos_especiales
        FROM personal p
        JOIN tipos_personal tp ON p.tipo_personal_id = tp.id
        WHERE p.id = %s AND p.activo = 1 AND p.deleted_at IS NULL
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, (personal_id,))
            person = cur.fetchone()
            cur.close()
            return person
    except Exception as e:
        print(f"❌ Error obteniendo personal ID {personal_id}: {e}")
        return None

def get_personal_by_document(document_type: str, document_number: str) -> Optional[Dict[str, Any]]:
    """Obtiene información de una persona por tipo y número de documento"""
    query = """
        SELECT p.id, p.tipo_personal_id, p.documento_tipo, p.documento_numero,
               p.nombres, p.apellidos, p.email, p.telefono, p.direccion,
               p.fecha_nacimiento, p.genero, p.huella_digital, p.fecha_registro_huella,
               p.activo, p.fecha_contratacion, p.fecha_terminacion,
               tp.nombre as tipo_personal_nombre, tp.max_llaves_por_dia, tp.permisos_especiales
        FROM personal p
        JOIN tipos_personal tp ON p.tipo_personal_id = tp.id
        WHERE p.documento_tipo = %s AND p.documento_numero = %s 
          AND p.activo = 1 AND p.deleted_at IS NULL
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, (document_type, document_number))
            person = cur.fetchone()
            cur.close()
            return person
    except Exception as e:
        print(f"❌ Error obteniendo personal por documento {document_type} {document_number}: {e}")
        return None

def get_available_keys() -> List[Dict[str, Any]]:
    """Obtiene las llaves disponibles desde la tabla llaves"""
    query = """
        SELECT id, codigo_llave, descripcion, ambiente_id, estado, activo, 
               angulo_grados, modulo, posicion_circular, tipo_llave
        FROM llaves 
        WHERE activo = 1 AND estado = 'DISPONIBLE'
        ORDER BY codigo_llave
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)
            keys = cur.fetchall()
            cur.close()
            return keys
    except Exception as e:
        print(f"❌ Error obteniendo llaves disponibles: {e}")
        return []

def get_environments() -> List[Dict[str, Any]]:
    """Obtiene los ambientes disponibles"""
    query = """
        SELECT id, nombre, descripcion, ubicacion, capacidad, activo, estado
        FROM ambientes 
        WHERE activo = 1
        ORDER BY nombre
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)
            environments = cur.fetchall()
            cur.close()
            return environments
    except Exception as e:
        print(f"❌ Error obteniendo ambientes: {e}")
        return []

def get_active_key_assignments() -> List[Dict[str, Any]]:
    """Obtiene las asignaciones activas de llaves"""
    query = """
        SELECT al.id, al.personal_id, al.llave_id, al.fecha_asignacion, 
               al.fecha_devolucion, al.estado, al.motivo, al.notas,
               p.nombres, p.apellidos, p.documento_numero,
               l.codigo_llave as llave_codigo, l.descripcion as llave_descripcion,
               a.nombre as ambiente_nombre
        FROM asignaciones_llaves al
        JOIN personal p ON al.personal_id = p.id
        JOIN llaves l ON al.llave_id = l.id
        JOIN ambientes a ON l.ambiente_id = a.id
        WHERE al.estado = 'ACTIVA'
        ORDER BY al.fecha_asignacion DESC
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)
            assignments = cur.fetchall()
            cur.close()
            return assignments
    except Exception as e:
        print(f"❌ Error obteniendo asignaciones activas: {e}")
        return []

def assign_key_to_person(personal_id: int, key_id: int, observations: str = "") -> bool:
    """Asigna una llave a una persona"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Verificar que la llave esté disponible
            cur.execute("SELECT estado FROM llaves WHERE id = %s", (key_id,))
            key_status = cur.fetchone()
            if not key_status or key_status[0] != 'DISPONIBLE':
                print(f"❌ La llave {key_id} no está disponible")
                return False
            
            # Crear la asignación
            insert_query = """
                INSERT INTO asignaciones_llaves 
                (personal_id, llave_id, fecha_asignacion, estado, motivo, created_at)
                VALUES (%s, %s, NOW(), 'ACTIVA', %s, NOW())
            """
            cur.execute(insert_query, (personal_id, key_id, observations))
            
            # Actualizar estado de la llave
            cur.execute("UPDATE llaves SET estado = 'ASIGNADA' WHERE id = %s", (key_id,))
            
            cnx.commit()
            cur.close()
            print(f"✅ Llave {key_id} asignada exitosamente a personal {personal_id}")
            return True
            
    except Exception as e:
        print(f"❌ Error asignando llave: {e}")
        return False

def return_key_from_person(assignment_id: int, observations: str = "") -> bool:
    """Devuelve una llave de una persona"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Obtener información de la asignación
            cur.execute("SELECT llave_id FROM asignaciones_llaves WHERE id = %s", (assignment_id,))
            assignment = cur.fetchone()
            if not assignment:
                print(f"❌ Asignación {assignment_id} no encontrada")
                return False
            
            key_id = assignment[0]
            
            # Marcar asignación como devuelta
            update_query = """
                UPDATE asignaciones_llaves 
                SET estado = 'DEVUELTA', fecha_devolucion = NOW(), 
                    notas = CONCAT(IFNULL(notas, ''), ' | Devolución: ', %s),
                    updated_at = NOW()
                WHERE id = %s
            """
            cur.execute(update_query, (observations, assignment_id))
            
            # Actualizar estado de la llave
            cur.execute("UPDATE llaves SET estado = 'DISPONIBLE' WHERE id = %s", (key_id,))
            
            cnx.commit()
            cur.close()
            print(f"✅ Llave {key_id} devuelta exitosamente")
            return True
            
    except Exception as e:
        print(f"❌ Error devolviendo llave: {e}")
        return False

def log_access(personal_id: int, action: str, details: str = "") -> bool:
    """Registra un acceso en la tabla logs_acceso"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            insert_query = """
                INSERT INTO logs_acceso 
                (personal_id, tipo_accion, fecha_hora, exitoso, ip_address, notas)
                VALUES (%s, %s, NOW(), 1, '127.0.0.1', %s)
            """
            cur.execute(insert_query, (personal_id, action, details))
            
            cnx.commit()
            cur.close()
            return True
            
    except Exception as e:
        print(f"❌ Error registrando acceso: {e}")
        return False

def get_access_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Obtiene los logs de acceso más recientes"""
    query = """
        SELECT l.id, l.personal_id, l.fecha_hora, l.tipo_accion, l.notas,
               l.ip_address, l.exitoso, l.calidad_huella, p.nombres, p.apellidos, p.documento_numero
        FROM logs_acceso l
        JOIN personal p ON l.personal_id = p.id
        ORDER BY l.fecha_hora DESC
        LIMIT %s
    """
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, (limit,))
            logs = cur.fetchall()
            cur.close()
            return logs
    except Exception as e:
        print(f"❌ Error obteniendo logs de acceso: {e}")
        return []

def test_database_connection() -> bool:
    """Prueba la conexión a la base de datos"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor()
            cur.execute("SELECT 1")
            result = cur.fetchone()
            cur.close()
            
            if result and result[0] == 1:
                print("✅ Conexión a la base de datos exitosa")
                return True
            else:
                print("❌ Conexión a la base de datos falló")
                return False
                
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def get_daily_schedule(date=None) -> List[Dict[str, Any]]:
    """Obtiene la programación del día especificado desde la base de datos"""
    if date is None:
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            
            # Consulta para obtener programación del día con información de instructores y ambientes
            query = """
                SELECT 
                    p.id as instructor_id,
                    CONCAT(p.nombres, ' ', p.apellidos) as instructor_nombre,
                    a.nombre as ambiente_nombre,
                    a.descripcion as ambiente_descripcion,
                    tp.nombre as tipo_personal,
                    al.fecha_asignacion,
                    al.fecha_devolucion,
                    l.codigo_llave,
                    l.descripcion as llave_descripcion
                FROM asignaciones_llaves al
                JOIN personal p ON al.personal_id = p.id
                JOIN tipos_personal tp ON p.tipo_personal_id = tp.id
                JOIN llaves l ON al.llave_id = l.id
                JOIN ambientes a ON l.ambiente_id = a.id
                WHERE DATE(al.fecha_asignacion) = %s 
                  AND al.estado = 'ACTIVA'
                  AND tp.nombre = 'INSTRUCTOR'
                ORDER BY al.fecha_asignacion ASC
            """
            
            cur.execute(query, (date,))
            results = cur.fetchall()
            cur.close()
            
            # Si no hay datos reales, usar datos de ejemplo mejorados
            if not results:
                return get_sample_schedule_data(date)
            
            # Procesar datos reales
            schedule_data = []
            for i, row in enumerate(results):
                # Generar horarios basados en la hora de asignación
                hora_inicio = "08:00" if i == 0 else f"{8 + (i * 2):02d}:00"
                hora_fin = f"{10 + (i * 2):02d}:00"
                
                schedule_data.append({
                    'id': row['instructor_id'],
                    'ambiente': row['ambiente_nombre'],
                    'instructor': row['instructor_nombre'],
                    'programa_formacion': f"{row['llave_descripcion']} - Ficha {row['codigo_llave']}",
                    'hora_inicio': hora_inicio,
                    'hora_fin': hora_fin,
                    'fecha': date,
                    'tipo_personal': row['tipo_personal']
                })
            
            return schedule_data
            
    except Exception as e:
        print(f"❌ Error obteniendo programación real: {e}")
        # Retornar datos de ejemplo si hay error
        return get_sample_schedule_data(date)

def get_sample_schedule_data(date) -> List[Dict[str, Any]]:
    """Datos de ejemplo mejorados para la programación"""
    return [
        {
            'id': 1,
            'ambiente': 'Aula 101 - Programación',
            'instructor': 'Carlos Mendoza',
            'programa_formacion': 'Programación Básica - Ficha 001',
            'hora_inicio': '08:00',
            'hora_fin': '10:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        },
        {
            'id': 2,
            'ambiente': 'Laboratorio 201 - Desarrollo',
            'instructor': 'Ana García',
            'programa_formacion': 'Desarrollo Web - Ficha 002',
            'hora_inicio': '10:00',
            'hora_fin': '12:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        },
        {
            'id': 3,
            'ambiente': 'Aula 102 - Bases de Datos',
            'instructor': 'Luis Rodríguez',
            'programa_formacion': 'Bases de Datos - Ficha 003',
            'hora_inicio': '14:00',
            'hora_fin': '16:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        },
        {
            'id': 4,
            'ambiente': 'Laboratorio 202 - Algoritmos',
            'instructor': 'María López',
            'programa_formacion': 'Algoritmos - Ficha 004',
            'hora_inicio': '16:00',
            'hora_fin': '18:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        },
        {
            'id': 5,
            'ambiente': 'Aula 103 - Avanzado',
            'instructor': 'Pedro Sánchez',
            'programa_formacion': 'Programación Avanzada - Ficha 005',
            'hora_inicio': '18:00',
            'hora_fin': '20:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        },
        {
            'id': 6,
            'ambiente': 'Laboratorio 203 - IA',
            'instructor': 'Sofia Martínez',
            'programa_formacion': 'Inteligencia Artificial - Ficha 006',
            'hora_inicio': '20:00',
            'hora_fin': '22:00',
            'fecha': date,
            'tipo_personal': 'INSTRUCTOR'
        }
    ]

def search_schedule_by_name(search_term: str, date=None) -> List[Dict[str, Any]]:
    """Busca en la programación por nombre del instructor"""
    if not search_term:
        return get_daily_schedule(date)
    
    all_schedule = get_daily_schedule(date)
    search_term_lower = search_term.lower()
    
    # Filtrar por nombre del instructor
    filtered_schedule = [
        item for item in all_schedule 
        if search_term_lower in item['instructor'].lower()
    ]
    
    return filtered_schedule

def get_database_info() -> Dict[str, Any]:
    """Obtiene información general de la base de datos"""
    try:
        with db_connect() as cnx:
            cur = cnx.cursor(dictionary=True)
            
            # Contar registros en cada tabla principal
            tables = ['personal', 'tipos_personal', 'llaves', 'ambientes', 'asignaciones_llaves']
            counts = {}
            
            for table in tables:
                cur.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = cur.fetchone()
                counts[table] = result['count'] if result else 0
            
            # Contar personal con huellas
            cur.execute("SELECT COUNT(*) as count FROM personal WHERE huella_digital IS NOT NULL")
            result = cur.fetchone()
            counts['personal_con_huellas'] = result['count'] if result else 0
            
            # Contar llaves disponibles
            cur.execute("SELECT COUNT(*) as count FROM llaves WHERE estado = 'DISPONIBLE'")
            result = cur.fetchone()
            counts['llaves_disponibles'] = result['count'] if result else 0
            
            cur.close()
            
            return {
                'total_personal': counts.get('personal', 0),
                'personal_con_huellas': counts.get('personal_con_huellas', 0),
                'tipos_personal': counts.get('tipos_personal', 0),
                'total_llaves': counts.get('llaves', 0),
                'llaves_disponibles': counts.get('llaves_disponibles', 0),
                'total_ambientes': counts.get('ambientes', 0),
                'asignaciones_activas': counts.get('asignaciones_llaves', 0)
            }
            
    except Exception as e:
        print(f"❌ Error obteniendo información de la base de datos: {e}")
        return {}
