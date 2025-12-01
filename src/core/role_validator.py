#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
role_validator.py
- Validador de roles específicos para el sistema biométrico
- Verificación de permisos por tipo de personal en la base de datos
"""

from typing import Optional, Dict, Any, Tuple
from src.utils.db_utils import get_personal_by_id, get_personal_types

class RoleValidator:
    """Validador de roles específicos para el sistema biométrico"""
    
    def __init__(self):
        self.role_mapping = {
            'admin': 'ADMINISTRADOR',
            'instructor': 'INSTRUCTOR',
            'security': 'SEGURIDAD', 
            'cleaning': 'LIMPIEZA',
            'administrative': 'ADMINISTRATIVO'
        }
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Obtiene el rol del usuario desde la base de datos"""
        try:
            user = get_personal_by_id(user_id)
            if not user:
                return None
            
            return user.get('tipo_personal_nombre', 'DESCONOCIDO')
            
        except Exception as e:
            print(f"❌ Error obteniendo rol del usuario {user_id}: {e}")
            return None
    
    def validate_role_access(self, user_id: int, requested_role: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Valida si un usuario tiene acceso a un rol específico
        
        Args:
            user_id: ID del usuario
            requested_role: Rol solicitado (admin, instructor, security, cleaning, administrative)
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
                - (tiene_acceso, nombre_usuario, rol_real)
        """
        try:
            # Obtener información del usuario
            user = get_personal_by_id(user_id)
            if not user:
                return False, None, None
            
            user_name = f"{user.get('nombres', '')} {user.get('apellidos', '')}".strip()
            user_role = user.get('tipo_personal_nombre', 'DESCONOCIDO')
            
            # Mapear el rol solicitado al nombre en la base de datos
            requested_role_name = self.role_mapping.get(requested_role, requested_role.upper())
            
            # Verificar si el usuario tiene el rol correcto
            has_access = user_role.upper() == requested_role_name.upper()
            
            return has_access, user_name, user_role
            
        except Exception as e:
            print(f"❌ Error validando acceso del usuario {user_id} al rol {requested_role}: {e}")
            return False, None, None
    
    def get_role_display_name(self, role_key: str) -> str:
        """Obtiene el nombre de visualización para un rol"""
        return self.role_mapping.get(role_key, role_key.upper())
    
    def get_all_roles(self) -> Dict[str, str]:
        """Obtiene todos los roles disponibles"""
        return self.role_mapping.copy()
    
    def is_valid_role(self, role_key: str) -> bool:
        """Verifica si un rol es válido"""
        return role_key in self.role_mapping

# Instancia global del validador de roles
role_validator = RoleValidator()
