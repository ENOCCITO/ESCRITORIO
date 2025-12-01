#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biometric_interface.py
- Interface unificada para el sistema biométrico
- Permite cambiar entre escáner real y simulador
"""

import os
from typing import Optional, Tuple, Any, Dict, List
from datetime import datetime

# Importar ambos sistemas
from src.core.biometric_scanner import BiometricScanner
from src.core.fingerprint_simulator import FingerprintSimulator

class BiometricInterface:
    """Interface unificada para el sistema biométrico"""
    
    def __init__(self, use_simulator: bool = False):
        """
        Inicializa la interfaz biométrica
        
        Args:
            use_simulator: Si True, usa el simulador; si False, usa el escáner real
        """
        self.use_simulator = use_simulator or not self._is_hardware_available()
        
        if self.use_simulator:
            print("🎭 Usando SIMULADOR de huellas digitales")
            self.scanner = FingerprintSimulator()
        else:
            print("🔬 Usando ESCÁNER BIOMÉTRICO REAL")
            self.scanner = BiometricScanner()
    
    def _is_hardware_available(self) -> bool:
        """
        Verifica si el hardware biométrico está disponible
        Por ahora, simplemente verifica si estamos en modo desarrollo
        """
        # Verificar variable de entorno para forzar el uso del simulador
        if os.getenv('USE_FINGERPRINT_SIMULATOR', '').lower() in ('true', '1', 'yes'):
            return False
        
        # Por defecto, asumir que no tenemos hardware hasta que se demuestre lo contrario
        return False
    
    def connect(self) -> bool:
        """Conecta al dispositivo biométrico"""
        try:
            return self.scanner.connect()
        except Exception as e:
            print(f"❌ Error conectando al dispositivo: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del dispositivo biométrico"""
        try:
            self.scanner.disconnect()
        except Exception as e:
            print(f"⚠️ Error desconectando dispositivo: {e}")
    
    @property
    def connected(self) -> bool:
        """Verifica si el dispositivo está conectado"""
        return getattr(self.scanner, 'connected', False)
    
    def test_com3_connection(self) -> bool:
        """
        Prueba específicamente la conexión en COM3
        Solo disponible en el escáner real
        """
        if self.use_simulator:
            # El simulador siempre está "conectado"
            return True
        
        if hasattr(self.scanner, 'test_com3_connection'):
            return self.scanner.test_com3_connection()
        return False
    
    def scan_fingerprint(self, timeout: int = 30) -> Optional[bytes]:
        """
        Escanea una huella digital
        
        Args:
            timeout: Tiempo máximo de espera en segundos
            
        Returns:
            bytes: Datos de la huella escaneada o None si hay error
        """
        try:
            return self.scanner.scan_fingerprint(timeout)
        except Exception as e:
            print(f"❌ Error escaneando huella: {e}")
            return None
    
    def save_fingerprint_to_db(self, person_id: int, fingerprint_data: bytes) -> bool:
        """
        Guarda la huella digital en la base de datos
        
        Args:
            person_id: ID de la persona
            fingerprint_data: Datos binarios de la huella
            
        Returns:
            bool: True si se guardó correctamente
        """
        if hasattr(self.scanner, 'save_fingerprint_to_db'):
            return self.scanner.save_fingerprint_to_db(person_id, fingerprint_data)
        
        # Para el simulador, solo simulamos el guardado
        print(f"🎭 Simulando guardado de huella para persona ID {person_id}")
        return True
    
    def verify_fingerprint_exists(self, person_id: int) -> bool:
        """
        Verifica si una persona ya tiene huella registrada
        
        Args:
            person_id: ID de la persona
            
        Returns:
            bool: True si ya tiene huella registrada
        """
        if hasattr(self.scanner, 'verify_fingerprint_exists'):
            return self.scanner.verify_fingerprint_exists(person_id)
        
        # Para el simulador, devolvemos False para permitir el registro
        return False
    
    def register_fingerprint_for_person(self, person_id: int, person_name: str) -> Tuple[bool, str]:
        """
        Registra una huella para una persona específica
        
        Args:
            person_id: ID de la persona
            person_name: Nombre de la persona
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if hasattr(self.scanner, 'register_fingerprint_for_person'):
            return self.scanner.register_fingerprint_for_person(person_id, person_name)
        
        # Para el simulador
        try:
            # Simular escaneo
            fingerprint_data = self.scan_fingerprint()
            if not fingerprint_data:
                return False, "No se pudo escanear la huella (simulación)"
            
            # Simular guardado
            if self.save_fingerprint_to_db(person_id, fingerprint_data):
                return True, f"Huella registrada exitosamente para {person_name} (simulación)"
            else:
                return False, "Error guardando la huella en la base de datos (simulación)"
                
        except Exception as e:
            return False, f"Error registrando huella: {e}"
    
    def update_fingerprint_for_person(self, person_id: int, person_name: str) -> Tuple[bool, str]:
        """
        Actualiza una huella para una persona específica
        
        Args:
            person_id: ID de la persona
            person_name: Nombre de la persona
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if hasattr(self.scanner, 'update_fingerprint_for_person'):
            return self.scanner.update_fingerprint_for_person(person_id, person_name)
        
        # Para el simulador, usar la misma lógica que registro
        return self.register_fingerprint_for_person(person_id, person_name)
    
    def validate_fingerprint_against_database(self, scanned_characteristics: bytes) -> Optional[Dict[str, Any]]:
        """
        Valida la huella escaneada contra la base de datos
        
        Args:
            scanned_characteristics: Datos de la huella escaneada
            
        Returns:
            Optional[Dict[str, Any]]: Información del usuario si coincide, None si no
        """
        if hasattr(self.scanner, 'validate_fingerprint_against_database'):
            return self.scanner.validate_fingerprint_against_database(scanned_characteristics)
        
        # Para el simulador
        print("🎭 Simulando validación de huella contra base de datos")
        return None

# Instancia global de la interfaz biométrica (por defecto usa simulador)
biometric_interface = BiometricInterface(use_simulator=True)