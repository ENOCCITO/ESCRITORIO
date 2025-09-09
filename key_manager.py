#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
key_manager.py
- Gestor de llaves para el sistema de dispensación
- Integra con la base de datos sistema_llaves_v2
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_utils import *
from config import *

class KeyManager:
    """Gestor de llaves para el sistema"""
    
    def __init__(self):
        self.current_user = None
        
    def authenticate_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Autentica un usuario por ID"""
        try:
            user = get_personal_by_id(user_id)
            if user and user['activo']:
                self.current_user = user
                print(f"✅ Usuario autenticado: {user['nombres']} {user['apellidos']}")
                return user
            else:
                print("❌ Usuario no encontrado o inactivo")
                return None
        except Exception as e:
            print(f"❌ Error autenticando usuario: {e}")
            return None
    
    def show_available_keys(self, environment_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Muestra las llaves disponibles"""
        try:
            available_keys = get_available_keys()
            
            if environment_id:
                available_keys = [k for k in available_keys if k['ambiente_id'] == environment_id]
            
            if not available_keys:
                print("ℹ️ No hay llaves disponibles")
                return []
            
            print(f"\n🔑 LLAVES DISPONIBLES ({len(available_keys)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'CÓDIGO':<15} {'DESCRIPCIÓN':<40} {'AMBIENTE':<15} {'ÁNGULO':<10}")
            print("-" * 80)
            
            for key in available_keys:
                ambiente = "N/A"
                if key['ambiente_id']:
                    environments = get_environments()
                    for env in environments:
                        if env['id'] == key['ambiente_id']:
                            ambiente = env['nombre'][:14]
                            break
                
                print(f"{key['id']:<5} {key['codigo_llave']:<15} {key['descripcion'][:39]:<40} {ambiente:<15} {key['angulo_grados']:<10}")
            
            return available_keys
            
        except Exception as e:
            print(f"❌ Error mostrando llaves disponibles: {e}")
            return []
    
    def show_user_keys(self, user_id: int) -> List[Dict[str, Any]]:
        """Muestra las llaves asignadas a un usuario"""
        try:
            active_assignments = get_active_key_assignments()
            user_keys = [a for a in active_assignments if a['personal_id'] == user_id]
            
            if not user_keys:
                print("ℹ️ El usuario no tiene llaves asignadas")
                return []
            
            print(f"\n🔑 LLAVES ASIGNADAS AL USUARIO:")
            print("-" * 80)
            print(f"{'ID':<5} {'CÓDIGO':<15} {'DESCRIPCIÓN':<40} {'AMBIENTE':<15} {'FECHA':<20}")
            print("-" * 80)
            
            for assignment in user_keys:
                print(f"{assignment['id']:<5} {assignment['llave_codigo']:<15} {assignment['llave_descripcion'][:39]:<40} {assignment['ambiente_nombre'][:14]:<15} {assignment['fecha_asignacion'].strftime('%Y-%m-%d %H:%M')}")
            
            return user_keys
            
        except Exception as e:
            print(f"❌ Error mostrando llaves del usuario: {e}")
            return []
    
    def assign_key_to_user(self, user_id: int, key_id: int, observations: str = "") -> bool:
        """Asigna una llave a un usuario"""
        try:
            if not self.current_user or self.current_user['id'] != user_id:
                print("❌ Error: Usuario no autenticado o no coincide")
                return False
            
            # Verificar permisos del usuario
            user_permissions = self._get_user_permissions(self.current_user)
            if not user_permissions['can_access_keys']:
                print("❌ Error: El usuario no tiene permisos para recibir llaves")
                return False
            
            # Verificar límite diario
            can_receive, current, remaining = self._check_daily_key_limit(user_id)
            if not can_receive:
                print(f"❌ Error: Usuario ha alcanzado su límite diario ({current}/{user_permissions['max_keys_per_day']})")
                return False
            
            # Verificar que la llave esté disponible
            available_keys = get_available_keys()
            key_available = any(k['id'] == key_id for k in available_keys)
            if not key_available:
                print("❌ Error: La llave no está disponible")
                return False
            
            # Asignar la llave
            if assign_key_to_person(user_id, key_id, observations):
                print(f"✅ Llave asignada exitosamente")
                
                # Registrar en logs
                log_access(user_id, 'ENTREGA_LLAVE', f"Llave {key_id} asignada - {observations}")
                
                return True
            else:
                print("❌ Error asignando la llave")
                return False
                
        except Exception as e:
            print(f"❌ Error en asignación: {e}")
            return False
    
    def return_key_from_user(self, assignment_id: int, observations: str = "") -> bool:
        """Devuelve una llave de un usuario"""
        try:
            if not self.current_user:
                print("❌ Error: Usuario no autenticado")
                return False
            
            # Verificar que la asignación pertenezca al usuario actual
            user_keys = self.show_user_keys(self.current_user['id'])
            assignment_exists = any(a['id'] == assignment_id for a in user_keys)
            
            if not assignment_exists:
                print("❌ Error: La asignación no pertenece al usuario actual")
                return False
            
            # Devolver la llave
            if return_key_from_person(assignment_id, observations):
                print(f"✅ Llave devuelta exitosamente")
                
                # Registrar en logs
                log_access(self.current_user['id'], 'DEVOLUCION_LLAVE', f"Llave devuelta - {observations}")
                
                return True
            else:
                print("❌ Error devolviendo la llave")
                return False
                
        except Exception as e:
            print(f"❌ Error en devolución: {e}")
            return False
    
    def show_environments(self) -> List[Dict[str, Any]]:
        """Muestra los ambientes disponibles"""
        try:
            environments = get_environments()
            
            if not environments:
                print("ℹ️ No hay ambientes disponibles")
                return []
            
            print(f"\n🏢 AMBIENTES DISPONIBLES ({len(environments)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'NOMBRE':<25} {'DESCRIPCIÓN':<30} {'CAPACIDAD':<12} {'ESTADO':<15}")
            print("-" * 80)
            
            for env in environments:
                print(f"{env['id']:<5} {env['nombre'][:24]:<25} {env['descripcion'][:29]:<30} {str(env['capacidad'] or 'N/A'):<12} {env['estado']:<15}")
            
            return environments
            
        except Exception as e:
            print(f"❌ Error mostrando ambientes: {e}")
            return []
    
    def _get_user_permissions(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene los permisos del usuario"""
        try:
            permissions = {
                'can_access_keys': False,
                'max_keys_per_day': 0,
                'special_permissions': False,
                'user_type': user.get('tipo_personal_nombre', 'DESCONOCIDO')
            }
            
            personal_types = get_personal_types()
            for pt in personal_types:
                if pt['id'] == user['tipo_personal_id']:
                    permissions['max_keys_per_day'] = pt['max_llaves_por_dia']
                    permissions['special_permissions'] = bool(pt['permisos_especiales'])
                    permissions['can_access_keys'] = pt['max_llaves_por_dia'] > 0
                    break
            
            return permissions
            
        except Exception as e:
            print(f"❌ Error obteniendo permisos: {e}")
            return {
                'can_access_keys': False,
                'max_keys_per_day': 0,
                'special_permissions': False,
                'user_type': 'ERROR'
            }
    
    def _check_daily_key_limit(self, user_id: int) -> Tuple[bool, int, int]:
        """Verifica el límite diario de llaves del usuario"""
        try:
            today = datetime.now().date()
            
            with db_connect() as cnx:
                cur = cnx.cursor()
                
                query = """
                    SELECT COUNT(*) as count
                    FROM asignaciones_llaves
                    WHERE personal_id = %s 
                      AND DATE(fecha_asignacion) = %s
                      AND estado = 'ACTIVA'
                """
                cur.execute(query, (user_id, today))
                result = cur.fetchone()
                current_keys = result[0] if result else 0
                
                user = get_personal_by_id(user_id)
                if user:
                    user_permissions = self._get_user_permissions(user)
                    max_keys = user_permissions['max_keys_per_day']
                    
                    can_receive = current_keys < max_keys
                    remaining = max_keys - current_keys
                    
                    return can_receive, current_keys, remaining
                
                return False, current_keys, 0
                
        except Exception as e:
            print(f"❌ Error verificando límite diario: {e}")
            return False, 0, 0

def main():
    """Función principal de demostración"""
    print("🔑 GESTOR DE LLAVES - sistema_llaves_v2")
    print("=" * 60)
    
    # Crear gestor
    manager = KeyManager()
    
    try:
        # Mostrar información general
        print("\n📊 INFORMACIÓN GENERAL DEL SISTEMA")
        print("-" * 40)
        db_info = get_database_info()
        if db_info:
            print(f"   • Total personal: {db_info['total_personal']}")
            print(f"   • Personal con huellas: {db_info['personal_con_huellas']}")
            print(f"   • Total llaves: {db_info['total_llaves']}")
            print(f"   • Llaves disponibles: {db_info['llaves_disponibles']}")
            print(f"   • Ambientes: {db_info['total_ambientes']}")
            print(f"   • Asignaciones activas: {db_info['asignaciones_activas']}")
        
        # Mostrar ambientes
        print("\n🏢 AMBIENTES DISPONIBLES")
        print("-" * 40)
        manager.show_environments()
        
        # Mostrar llaves disponibles
        print("\n🔑 LLAVES DISPONIBLES")
        print("-" * 40)
        manager.show_available_keys()
        
        # Mostrar tipos de personal
        print("\n👥 TIPOS DE PERSONAL")
        print("-" * 40)
        personal_types = get_personal_types()
        for pt in personal_types:
            print(f"   • {pt['nombre']}: {pt['descripcion']} (Max llaves: {pt['max_llaves_por_dia']})")
        
        # Mostrar personal con huellas
        print("\n👤 PERSONAL CON HUELLAS")
        print("-" * 40)
        personal_with_fingerprints = get_personal_with_fingerprints()
        for person in personal_with_fingerprints:
            print(f"   • {person['nombres']} {person['apellidos']} ({person['tipo_personal_nombre']})")
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA")
        print("\n💡 Para usar el sistema completo:")
        print("   1. Ejecuta fingerprint_validator.py para autenticación biométrica")
        print("   2. Usa key_manager.py para gestionar llaves")
        print("   3. Integra con la interfaz principal del sistema")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
