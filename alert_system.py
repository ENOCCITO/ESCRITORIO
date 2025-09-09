#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alert_system.py
- Sistema de alertas elegantes para el sistema biométrico
- Integración con SweetAlert2 para notificaciones profesionales
"""

import tkinter as tk
from tkinter import messagebox
import webbrowser
import json
import os
from typing import Optional, Dict, Any

class AlertSystem:
    """Sistema de alertas elegantes para el sistema biométrico"""
    
    def __init__(self):
        self.alert_html = self._create_alert_html()
        self.temp_file = "temp_alert.html"
    
    def _create_alert_html(self) -> str:
        """Crea el HTML base para las alertas con SweetAlert2"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Biométrico - Alerta</title>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        .cyber-grid {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: grid-move 20s linear infinite;
        }
        
        @keyframes grid-move {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        
        .cyber-particles {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #00ffff;
            border-radius: 50%;
            animation: float 6s infinite linear;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(100px);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="cyber-grid"></div>
    <div class="cyber-particles" id="particles"></div>
    <div class="container">
        <div id="alert-container"></div>
    </div>

    <script>
        // Crear partículas flotantes
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        createParticles();
        
        // Función para mostrar alerta de acceso denegado
        function showAccessDeniedAlert(role, userName = null) {
            const roleNames = {
                'admin': 'ADMINISTRADOR',
                'instructor': 'INSTRUCTOR', 
                'security': 'SEGURIDAD',
                'cleaning': 'ASEO',
                'administrative': 'ADMINISTRATIVO'
            };
            
            const roleName = roleNames[role] || role.toUpperCase();
            const userText = userName ? `\\n\\nUsuario identificado: ${userName}` : '';
            
            Swal.fire({
                title: '🚫 ACCESO DENEGADO',
                html: `
                    <div style="color: #ff6b6b; font-size: 18px; margin-bottom: 20px;">
                        <i class="fas fa-shield-alt" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                        <strong>Esta huella no corresponde a un ${roleName}</strong>
                    </div>
                    <div style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                        <p>🔐 <strong>Verificación de identidad fallida</strong></p>
                        <p>La huella digital escaneada no tiene permisos para acceder al módulo de ${roleName}.</p>
                        <p style="color: #ffd93d; margin-top: 15px;">
                            <strong>Por favor, contacte al administrador del sistema para obtener los permisos necesarios.</strong>
                        </p>
                        ${userText}
                    </div>
                `,
                width: '500px',
                padding: '30px',
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
                backdrop: `
                    rgba(0, 0, 0, 0.8)
                    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2300ffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")
                `,
                customClass: {
                    popup: 'swal2-popup-custom',
                    title: 'swal2-title-custom',
                    htmlContainer: 'swal2-html-container-custom'
                },
                showConfirmButton: true,
                confirmButtonText: 'ENTENDIDO',
                confirmButtonColor: '#ff6b6b',
                confirmButtonAriaLabel: 'Entendido',
                buttonsStyling: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                showCloseButton: false,
                timer: null,
                didOpen: () => {
                    // Agregar efectos visuales adicionales
                    const popup = document.querySelector('.swal2-popup');
                    if (popup) {
                        popup.style.border = '2px solid #00ffff';
                        popup.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.5), inset 0 0 30px rgba(0, 255, 255, 0.1)';
                        popup.style.animation = 'pulse 2s infinite';
                    }
                    
                    // Agregar animación de pulso
                    const style = document.createElement('style');
                    style.textContent = `
                        @keyframes pulse {
                            0% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), inset 0 0 30px rgba(0, 255, 255, 0.1); }
                            50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.8), inset 0 0 40px rgba(0, 255, 255, 0.2); }
                            100% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), inset 0 0 30px rgba(0, 255, 255, 0.1); }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }).then((result) => {
                // Cerrar la ventana después de que el usuario haga clic en "Entendido"
                window.close();
            });
        }
        
        // Función para mostrar alerta de huella no reconocida
        function showFingerprintNotFoundAlert() {
            Swal.fire({
                title: '🔍 HUELLA NO RECONOCIDA',
                html: `
                    <div style="color: #ffa726; font-size: 18px; margin-bottom: 20px;">
                        <i class="fas fa-fingerprint" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                        <strong>Huella digital no encontrada en el sistema</strong>
                    </div>
                    <div style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                        <p>🔐 <strong>Verificación de identidad fallida</strong></p>
                        <p>La huella digital escaneada no se encuentra registrada en la base de datos del sistema.</p>
                        <p style="color: #ffd93d; margin-top: 15px;">
                            <strong>Por favor, asegúrese de que su huella esté registrada en el sistema o contacte al administrador.</strong>
                        </p>
                    </div>
                `,
                width: '500px',
                padding: '30px',
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
                backdrop: `
                    rgba(0, 0, 0, 0.8)
                    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffa726' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")
                `,
                customClass: {
                    popup: 'swal2-popup-custom',
                    title: 'swal2-title-custom',
                    htmlContainer: 'swal2-html-container-custom'
                },
                showConfirmButton: true,
                confirmButtonText: 'ENTENDIDO',
                confirmButtonColor: '#ffa726',
                confirmButtonAriaLabel: 'Entendido',
                buttonsStyling: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                showCloseButton: false,
                timer: null,
                didOpen: () => {
                    const popup = document.querySelector('.swal2-popup');
                    if (popup) {
                        popup.style.border = '2px solid #ffa726';
                        popup.style.boxShadow = '0 0 30px rgba(255, 167, 38, 0.5), inset 0 0 30px rgba(255, 167, 38, 0.1)';
                        popup.style.animation = 'pulse 2s infinite';
                    }
                }
            }).then((result) => {
                window.close();
            });
        }
        
        // Función para mostrar alerta de acceso exitoso
        function showAccessGrantedAlert(role, userName) {
            const roleNames = {
                'admin': 'ADMINISTRADOR',
                'instructor': 'INSTRUCTOR', 
                'security': 'SEGURIDAD',
                'cleaning': 'ASEO',
                'administrative': 'ADMINISTRATIVO'
            };
            
            const roleName = roleNames[role] || role.toUpperCase();
            
            Swal.fire({
                title: '✅ ACCESO CONCEDIDO',
                html: `
                    <div style="color: #4caf50; font-size: 18px; margin-bottom: 20px;">
                        <i class="fas fa-check-circle" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                        <strong>Bienvenido, ${userName}</strong>
                    </div>
                    <div style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                        <p>🔐 <strong>Verificación de identidad exitosa</strong></p>
                        <p>Acceso concedido al módulo de <strong>${roleName}</strong>.</p>
                        <p style="color: #81c784; margin-top: 15px;">
                            <strong>Iniciando interfaz del sistema...</strong>
                        </p>
                    </div>
                `,
                width: '500px',
                padding: '30px',
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
                backdrop: `
                    rgba(0, 0, 0, 0.8)
                    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%234caf50' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")
                `,
                customClass: {
                    popup: 'swal2-popup-custom',
                    title: 'swal2-title-custom',
                    htmlContainer: 'swal2-html-container-custom'
                },
                showConfirmButton: true,
                confirmButtonText: 'CONTINUAR',
                confirmButtonColor: '#4caf50',
                confirmButtonAriaLabel: 'Continuar',
                buttonsStyling: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                showCloseButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: () => {
                    const popup = document.querySelector('.swal2-popup');
                    if (popup) {
                        popup.style.border = '2px solid #4caf50';
                        popup.style.boxShadow = '0 0 30px rgba(76, 175, 80, 0.5), inset 0 0 30px rgba(76, 175, 80, 0.1)';
                    }
                }
            }).then((result) => {
                window.close();
            });
        }
        
        // Cargar Font Awesome para los iconos
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
        document.head.appendChild(link);
        
        // Estilos personalizados para SweetAlert2
        const customStyles = document.createElement('style');
        customStyles.textContent = `
            .swal2-popup-custom {
                border-radius: 15px !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }
            
            .swal2-title-custom {
                color: #ffffff !important;
                font-size: 24px !important;
                font-weight: bold !important;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
            }
            
            .swal2-html-container-custom {
                color: #ffffff !important;
            }
            
            .swal2-confirm {
                border-radius: 25px !important;
                font-weight: bold !important;
                font-size: 16px !important;
                padding: 12px 30px !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s ease !important;
            }
            
            .swal2-confirm:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
            }
        `;
        document.head.appendChild(customStyles);
    </script>
</body>
</html>
        """
    
    def show_access_denied_alert(self, role: str, user_name: Optional[str] = None):
        """Muestra una alerta de acceso denegado para un rol específico"""
        try:
            # Crear archivo HTML temporal
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(self.alert_html)
            
            # Agregar script para mostrar la alerta específica
            script_addition = f"""
            <script>
                // Mostrar alerta cuando la página se carga
                window.addEventListener('load', function() {{
                    showAccessDeniedAlert('{role}', {f"'{user_name}'" if user_name else 'null'});
                }});
            </script>
            """
            
            # Insertar el script antes del cierre del body
            with open(self.temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace('</body>', script_addition + '</body>')
            
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Abrir en el navegador
            file_path = os.path.abspath(self.temp_file)
            webbrowser.open(f'file://{file_path}')
            
        except Exception as e:
            print(f"❌ Error mostrando alerta de acceso denegado: {e}")
            # Fallback a messagebox si hay error
            self._fallback_access_denied_alert(role, user_name)
    
    def show_fingerprint_not_found_alert(self):
        """Muestra una alerta cuando no se encuentra la huella"""
        try:
            # Crear archivo HTML temporal
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(self.alert_html)
            
            # Agregar script para mostrar la alerta específica
            script_addition = """
            <script>
                // Mostrar alerta cuando la página se carga
                window.addEventListener('load', function() {
                    showFingerprintNotFoundAlert();
                });
            </script>
            """
            
            # Insertar el script antes del cierre del body
            with open(self.temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace('</body>', script_addition + '</body>')
            
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Abrir en el navegador
            file_path = os.path.abspath(self.temp_file)
            webbrowser.open(f'file://{file_path}')
            
        except Exception as e:
            print(f"❌ Error mostrando alerta de huella no encontrada: {e}")
            # Fallback a messagebox si hay error
            self._fallback_fingerprint_not_found_alert()
    
    def show_access_granted_alert(self, role: str, user_name: str):
        """Muestra una alerta de acceso concedido"""
        try:
            # Crear archivo HTML temporal
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(self.alert_html)
            
            # Agregar script para mostrar la alerta específica
            script_addition = f"""
            <script>
                // Mostrar alerta cuando la página se carga
                window.addEventListener('load', function() {{
                    showAccessGrantedAlert('{role}', '{user_name}');
                }});
            </script>
            """
            
            # Insertar el script antes del cierre del body
            with open(self.temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace('</body>', script_addition + '</body>')
            
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Abrir en el navegador
            file_path = os.path.abspath(self.temp_file)
            webbrowser.open(f'file://{file_path}')
            
        except Exception as e:
            print(f"❌ Error mostrando alerta de acceso concedido: {e}")
            # Fallback a messagebox si hay error
            self._fallback_access_granted_alert(role, user_name)
    
    def _fallback_access_denied_alert(self, role: str, user_name: Optional[str] = None):
        """Fallback usando messagebox si hay error con SweetAlert2"""
        role_names = {
            'admin': 'ADMINISTRADOR',
            'instructor': 'INSTRUCTOR', 
            'security': 'SEGURIDAD',
            'cleaning': 'ASEO',
            'administrative': 'ADMINISTRATIVO'
        }
        
        role_name = role_names.get(role, role.upper())
        user_text = f"\n\nUsuario identificado: {user_name}" if user_name else ""
        
        messagebox.showerror(
            "🚫 ACCESO DENEGADO",
            f"Esta huella no corresponde a un {role_name}\n\n"
            f"La huella digital escaneada no tiene permisos para acceder al módulo de {role_name}.\n"
            f"Por favor, contacte al administrador del sistema para obtener los permisos necesarios.{user_text}"
        )
    
    def _fallback_fingerprint_not_found_alert(self):
        """Fallback usando messagebox si hay error con SweetAlert2"""
        messagebox.showwarning(
            "🔍 HUELLA NO RECONOCIDA",
            "Huella digital no encontrada en el sistema\n\n"
            "La huella digital escaneada no se encuentra registrada en la base de datos del sistema.\n"
            "Por favor, asegúrese de que su huella esté registrada en el sistema o contacte al administrador."
        )
    
    def _fallback_access_granted_alert(self, role: str, user_name: str):
        """Fallback usando messagebox si hay error con SweetAlert2"""
        role_names = {
            'admin': 'ADMINISTRADOR',
            'instructor': 'INSTRUCTOR', 
            'security': 'SEGURIDAD',
            'cleaning': 'ASEO',
            'administrative': 'ADMINISTRATIVO'
        }
        
        role_name = role_names.get(role, role.upper())
        
        messagebox.showinfo(
            "✅ ACCESO CONCEDIDO",
            f"Bienvenido, {user_name}\n\n"
            f"Verificación de identidad exitosa\n"
            f"Acceso concedido al módulo de {role_name}.\n"
            f"Iniciando interfaz del sistema..."
        )
    
    def cleanup(self):
        """Limpia archivos temporales"""
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except Exception as e:
            print(f"⚠️ Error limpiando archivos temporales: {e}")

# Instancia global del sistema de alertas
alert_system = AlertSystem()
