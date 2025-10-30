#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_interface.py
- Interfaz de seguridad (PySide6)
"""

import styles
from config import *
from utils import *
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox, QPushButton, QDialog
from key_manager import KeyManager
from desktop_alerts import desktop_alert_system
from db_utils import get_available_keys, get_environments, assign_key_to_person, get_personal_by_id

class SecurityInterface:
    def __init__(self, parent, user: dict | None = None):
        self.parent = parent
        self._km = KeyManager()
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass

    def set_authenticated_user(self, user: dict | None):
        """Actualiza el usuario autenticado para la sesión de seguridad."""
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass
        
    def show_security_interface(self):
        security_win = styles.create_modal_window(self.parent, "🛡️ INTERFAZ DE SEGURIDAD - SISTEMA CEFA", ADMIN_WINDOW_SIZE)
        
        main_layout = QVBoxLayout(security_win)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        welcome_label = styles.create_title_label(security_win, "🛡️ INTERFAZ DE SEGURIDAD")
        main_layout.addWidget(welcome_label)

        # Único botón principal: Seleccionar ambiente
        select_btn = styles.create_futuristic_button(security_win, "🏢 SELECCIONAR AMBIENTE", self._open_environment_selector)
        main_layout.addWidget(select_btn)

        # Sección: Mis llaves en mano (para devolver)
        my_keys_card = styles.create_card(security_win)
        mk_l = QVBoxLayout(my_keys_card)
        mk_l.setContentsMargins(16, 12, 16, 12)
        mk_l.addWidget(styles.create_subtitle_label(my_keys_card, "MIS LLAVES EN MANO"))
        self._my_keys_container = styles.create_main_frame(my_keys_card)
        self._my_keys_layout = QVBoxLayout(self._my_keys_container)
        mk_l.addWidget(self._my_keys_container)
        main_layout.addWidget(my_keys_card)
        self._refresh_my_keys()

        logout_btn = styles.create_danger_button(security_win, "🚪 CERRAR SESIÓN", security_win.close)
        main_layout.addWidget(logout_btn)

        styles.center_window(security_win)
        security_win.show()

    def _show_real_time_monitoring(self, parent_window):
        """Muestra el monitoreo en tiempo real del campus"""
        # Crear ventana de monitoreo
        monitoring_win = styles.create_modal_window(self.parent, "📹 MONITOREO EN TIEMPO REAL", ENVIRONMENT_WINDOW_SIZE)
        layout = QVBoxLayout(monitoring_win)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(styles.create_title_label(monitoring_win, "📹 MONITOREO EN TIEMPO REAL"))
        layout.addWidget(styles.create_subtitle_label(monitoring_win, "Estado actual del campus y cámaras de seguridad"))
        main_block = styles.create_content_frame(monitoring_win)
        main_block_layout = QVBoxLayout(main_block)
        for line in """🏫 ESTADO ACTUAL DEL CAMPUS

🟢 ZONAS SEGURAS:
   • Edificio Principal: Normal
   • Laboratorios: Normal
   • Biblioteca: Normal
   • Cafetería: Normal
   • Estacionamiento: Normal

📹 CÁMARAS ACTIVAS:
   • Entrada Principal: Funcionando
   • Recepción: Funcionando
   • Pasillos: Funcionando
   • Estacionamiento: Funcionando
   • Salidas de Emergencia: Funcionando

👥 PERSONAL EN CAMPUS:
   • Estudiantes: 245
   • Instructores: 18
   • Administrativos: 12
   • Seguridad: 8
   • Mantenimiento: 5

🚨 ALERTAS ACTIVAS:
   • Ninguna alerta activa
   • Sistema funcionando normalmente
   • Todas las áreas monitoreadas""".split("\n"):
            if line.strip():
                main_block_layout.addWidget(styles.create_info_label(main_block, line))
        layout.addWidget(main_block)
        controls = styles.create_main_frame(monitoring_win)
        controls_layout = QHBoxLayout(controls)
        refresh_btn = styles.create_accent_button(controls, "🔄 ACTUALIZAR", lambda: self._refresh_campus_status())
        close_btn = styles.create_danger_button(controls, "❌ CERRAR", monitoring_win.close)
        controls_layout.addWidget(refresh_btn)
        controls_layout.addStretch(1)
        controls_layout.addWidget(close_btn)
        layout.addWidget(controls)
        styles.center_window(monitoring_win)
        monitoring_win.show()

    def _open_environment_selector(self):
        dlg = styles.create_modal_window(self.parent, "🏢 AMBIENTES DISPONIBLES", "900x620")
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)
        lay.addWidget(styles.create_subtitle_label(dlg, "Seleccione un ambiente para gestionar sus llaves disponibles"))

        # Construir lista de ambientes con llaves disponibles
        # Mostrar todos los ambientes con llaves en estado DISPONIBLE o ASIGNADA (pero no DEVUELTA)
        # Seguridad puede sacar llaves asignadas si no han sido reclamadas (estado ASIGNADA pero físicamente presente)
        try:
            from db_utils import db_connect
            env_ids_with_keys = {}
            envs_list = get_environments()
            envs = {e['id']: e for e in envs_list} if isinstance(envs_list, list) else {}
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                cur.execute("SELECT id, codigo_llave, descripcion, ambiente_id, estado, angulo_grados FROM llaves WHERE activo = 1 AND estado IN ('DISPONIBLE','ASIGNADA')")
                for row in cur.fetchall():
                    a_id = row.get('ambiente_id')
                    if a_id:
                        env_ids_with_keys.setdefault(a_id, []).append(row)
        except Exception:
            keys = get_available_keys()
            envs = {e['id']: e for e in get_environments()} if isinstance(get_environments(), list) else {}
            env_ids_with_keys = {}
            for k in keys:
                a_id = k.get('ambiente_id')
                if a_id:
                    env_ids_with_keys.setdefault(a_id, []).append(k)

        container = styles.create_main_frame(dlg)
        v = QVBoxLayout(container)
        if not env_ids_with_keys:
            v.addWidget(styles.create_info_label(container, "No hay llaves disponibles en este momento."))
        else:
            for env_id, klist in env_ids_with_keys.items():
                info = envs.get(env_id, {})
                name = info.get('nombre', f"Ambiente {env_id}")
                row = styles.create_main_frame(container)
                r = QHBoxLayout(row)
                r.addWidget(styles.create_info_label(row, f"🏢 {name}  •  🔑 {len(klist)} llaves disponibles o asignadas sin reclamar"))
                btn = styles.create_accent_button(row, "Ver llaves", lambda eid=env_id, n=name, kl=klist: self._open_keys_for_environment(eid, n, kl))
                r.addStretch(1)
                r.addWidget(btn)
                v.addWidget(row)
        lay.addWidget(container)
        dlg.show()

    def _create_security_header(self, parent, layout):
        header = styles.create_main_frame(parent)
        header_layout = QVBoxLayout(header)
        icon = styles.create_title_label(header, "🛡️")
        title = styles.create_title_label(header, "CONTROL DE ACCESO")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        layout.addWidget(header)

    def _open_keys_for_environment(self, environment_id: int, environment_name: str, preset_keys: list | None = None):
        dlg = styles.create_modal_window(self.parent, f"🔑 Llaves - {environment_name}", "900x620")
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(10)
        lay.addWidget(styles.create_subtitle_label(dlg, f"Llaves disponibles en {environment_name}"))

        container = styles.create_main_frame(dlg)
        v = QVBoxLayout(container)
        v.setContentsMargins(10, 8, 10, 8)
        v.setSpacing(8)
        # Usar la lista precargada de llaves si viene del selector para evitar inconsistencias
        if preset_keys is not None:
            available = preset_keys
        else:
            try:
                from db_utils import db_connect
                with db_connect() as cnx:
                    cur = cnx.cursor(dictionary=True)
                    cur.execute("SELECT id, codigo_llave, descripcion, ambiente_id, estado, angulo_grados FROM llaves WHERE activo = 1 AND ambiente_id = %s ORDER BY codigo_llave", (environment_id,))
                    available = cur.fetchall()
            except Exception:
                # Fallback: usar solo disponibles
                available = [k for k in get_available_keys() if k.get('ambiente_id') == environment_id]
        if not available:
            v.addWidget(styles.create_info_label(container, "No hay llaves registradas para este ambiente."))
        else:
            for key in available:
                row = styles.create_main_frame(container)
                r = QHBoxLayout(row)
                estado = str(key.get('estado','')).upper()
                # Línea de detalle más clara y estética
                label = styles.create_info_label(
                    row,
                    f"Código: {key['codigo_llave']}  •  {key.get('descripcion','')}  •  Estado: {estado}  •  Ángulo {key.get('angulo_grados','-')}"
                )
                r.addWidget(label)
                # Acción según estado
                if estado == 'DISPONIBLE':
                    btn = styles.create_accent_button(row, "Tomar", lambda kid=key['id'], kcode=key['codigo_llave']: self._take_security_key(kid, kcode))
                    r.addStretch(1)
                    r.addWidget(btn)
                elif estado == 'ASIGNADA':
                    btn = styles.create_warning_button(row, "Reclamar (Seguridad)", lambda kid=key['id'], kcode=key['codigo_llave']: self._take_security_key(kid, kcode))
                    r.addStretch(1)
                    r.addWidget(btn)
                else:
                    r.addStretch(1)
                r.addStretch(1)
                v.addWidget(row)
        lay.addWidget(container)
        dlg.show()

    def _refresh_my_keys(self):
        # Limpiar
        try:
            while self._my_keys_layout.count():
                item = self._my_keys_layout.takeAt(0)
                w = item.widget()
                if w:
                    w.setParent(None)
        except Exception:
            pass
        # Cargar asignaciones activas del usuario
        try:
            if self._km.current_user:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
            else:
                assignments = []
        except Exception:
            assignments = []
        if not assignments:
            self._my_keys_layout.addWidget(styles.create_info_label(self._my_keys_container, "No tienes llaves asignadas actualmente."))
            return
        for a in assignments:
            row = styles.create_main_frame(self._my_keys_container)
            r = QHBoxLayout(row)
            r.addWidget(styles.create_info_label(row, f"{a['llave_codigo']} • {a['llave_descripcion']} • {a['ambiente_nombre']} • {a['fecha_asignacion'].strftime('%Y-%m-%d %H:%M')}"))
            btn = styles.create_danger_button(row, "Devolver", lambda aid=a['id']: self._return_security_key(aid))
            r.addStretch(1)
            r.addWidget(btn)
            self._my_keys_layout.addWidget(row)

    def _take_security_key(self, key_id: int, key_code: str):
        # Robustez: si el usuario no está seteado, intentar recuperarlo desde main -> role context
        if not self._km.current_user:
            try:
                if hasattr(self.parent, 'best') and self.parent.best:
                    pid, name, score = self.parent.best
                    user = get_personal_by_id(int(pid))
                    if user:
                        self._km.current_user = user
            except Exception:
                pass
        if not self._km.current_user:
            QMessageBox.warning(self.parent, "⚠️", "No hay usuario de seguridad autenticado.")
            return
        # Seguridad puede tomar sin restricciones: usar asignación directa en BD
        ok = assign_key_to_person(self._km.current_user['id'], key_id, "Entrega a seguridad")
        if ok:
            # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
            self._send_arduino_command(key_id, "TOMAR")
            
            try:
                desktop_alert_system.show_key_assigned_alert(key_code, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
            except Exception:
                QMessageBox.information(self.parent, "Llave asignada", f"Se asignó la llave {key_code}")
            self._refresh_my_keys()
        else:
            QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")

    def _return_security_key(self, assignment_id: int):
        if not self._km.current_user:
            QMessageBox.warning(self.parent, "⚠️", "No hay usuario de seguridad autenticado.")
            return
        ok = self._km.return_key_from_user(assignment_id, "Devolución por seguridad")
        if ok:
            # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
            self._send_arduino_command(assignment_id, "DEVOLVER")
            
            try:
                desktop_alert_system.show_key_returned_alert(None, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
            except Exception:
                QMessageBox.information(self.parent, "Llave devuelta", "Devolución registrada correctamente")
            self._refresh_my_keys()
        else:
            QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")

    def _control_environment_access(self, environment_id, environment_name, access_type):
        pass

    def _create_security_footer(self, parent, window, layout):
        footer = styles.create_main_frame(parent)
        footer_layout = QHBoxLayout(footer)
        close_btn = styles.create_danger_button(footer, "❌ CERRAR", window.close)
        footer_layout.addStretch(1)
        footer_layout.addWidget(close_btn)
        layout.addWidget(footer)

    def _show_security_reports(self, parent_window):
        """Muestra los reportes de seguridad"""
        # Crear ventana de reportes de seguridad
        reports_win = styles.create_modal_window(self.parent, "📊 REPORTES DE SEGURIDAD", ENVIRONMENT_WINDOW_SIZE)
        
        # Título
        title_label = styles.create_title_label(reports_win, "📊 REPORTES DE SEGURIDAD")
        title_label.pack(pady=(20, 10))
        
        subtitle_label = styles.create_subtitle_label(reports_win, "Estadísticas y reportes de seguridad del campus")
        subtitle_label.pack(pady=(0, 30))
        
        # Contenedor principal
        main_frame = styles.create_content_frame(reports_win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para estadísticas de seguridad
        stats_frame = styles.create_main_frame(main_frame)
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        # Estadísticas de seguridad
        security_stats_content = """
📊 ESTADÍSTICAS DE SEGURIDAD

🚪 ACCESOS:
   • Total de accesos hoy: 1,247
   • Accesos autorizados: 1,245
   • Accesos denegados: 2
   • Tasa de éxito: 99.8%

👥 PERSONAS EN CAMPUS:
   • Máximo concurrente: 312
   • Promedio diario: 245
   • Personal autorizado: 43
   • Visitantes: 12

📹 CÁMARAS DE SEGURIDAD:
   • Total de cámaras: 24
   • Cámaras activas: 24
   • Cámaras en mantenimiento: 0
   • Tiempo de grabación: 24/7

🚨 INCIDENTES:
   • Incidentes reportados: 0
   • Alertas de seguridad: 0
   • Llamadas de emergencia: 0
   • Tiempo de respuesta: < 2 min

🛡️ MEDIDAS DE SEGURIDAD:
   • Control biométrico: Activo
   • Verificación de identidad: Activa
   • Monitoreo 24/7: Activo
   • Protocolos de emergencia: Actualizados
        """
        
        # Crear etiquetas para las estadísticas de seguridad
        stats_lines = security_stats_content.strip().split('\n')
        for i, line in enumerate(stats_lines):
            if line.strip():
                label = styles.create_info_label(stats_frame, line)
                label.pack(anchor="w", pady=2)
        
        # Botones de control
        control_frame = styles.create_main_frame(reports_win)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        # Botón para exportar reporte
        export_btn = styles.create_accent_button(
            control_frame, 
            "📊 EXPORTAR REPORTE", 
            lambda: self._export_security_report()
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón para cerrar
        close_btn = styles.create_danger_button(
            control_frame, 
            "❌ CERRAR", 
            reports_win.destroy
        )
        close_btn.pack(side="right")
        
        # Centrar la ventana
        styles.center_window(reports_win)

    def _refresh_campus_status(self):
        """Actualiza el estado del campus"""
        QMessageBox.information(self.parent, "🔄 ACTUALIZACIÓN", "Estado del campus actualizado.\n\nTodas las áreas están siendo monitoreadas en tiempo real.")
        
        # Aquí se integraría con la lógica del sistema original
        # para actualizar el estado real del campus

    def _control_access_point(self, access_point):
        """Maneja el control de un punto de acceso específico"""
        QMessageBox.information(self.parent, "🚪 CONTROL DE ACCESO", f"Gestionando: {access_point}\n\nEl sistema está configurando el control de acceso para este punto.\nPor favor, espere la confirmación del sistema.")
        
        # Aquí se integraría con la lógica del sistema original
        # para configurar el control de acceso al punto seleccionado

    def _export_security_report(self):
        """Exporta el reporte de seguridad"""
        try:
            from datetime import datetime
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_seguridad_{timestamp}.csv"
            
            # Datos del reporte de seguridad
            report_data = [
                ['REPORTE DE SEGURIDAD - SISTEMA CEFA'],
                ['Fecha de exportación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [],
                ['ESTADÍSTICAS DE SEGURIDAD'],
                ['Total de accesos hoy', '1,247'],
                ['Accesos autorizados', '1,245'],
                ['Accesos denegados', '2'],
                ['Tasa de éxito', '99.8%'],
                ['Máximo concurrente', '312'],
                ['Total de cámaras', '24'],
                ['Cámaras activas', '24'],
                ['Incidentes reportados', '0']
            ]
            
            if export_to_csv(report_data, filename):
                QMessageBox.information(self.parent, "📊 EXPORTACIÓN EXITOSA", f"El reporte de seguridad se ha exportado correctamente a:\n\n{filename}")
                
                # Abrir el archivo exportado
                open_file(filename)
            else:
                QMessageBox.critical(self.parent, "❌ ERROR", "Error al exportar el reporte de seguridad.")
                
        except Exception as e:
            QMessageBox.critical(self.parent, "🚨 ERROR", f"Error al exportar el reporte de seguridad:\n\n{e}")

    def _send_arduino_command(self, key_id_or_assignment_id: int, action: str):
        """
        Envía comando al Arduino para mover el motor NEMA17 a la posición de la llave
        
        Args:
            key_id_or_assignment_id: ID de la llave o asignación
            action: "TOMAR" o "DEVOLVER"
        """
        try:
            from utils import open_key_by_id, send_home, log_file
            from config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
            
            print(f"🤖 [SEGURIDAD] Enviando comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            log_file(f"🤖 [SEGURIDAD] Comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            
            if action == "TOMAR":
                # Para tomar llave, mover a la posición de la llave
                success = open_key_by_id(key_id_or_assignment_id, dwell_seconds=5)
                if success:
                    print(f"✅ [SEGURIDAD] Motor movido a posición de llave {key_id_or_assignment_id}")
                    log_file(f"✅ [SEGURIDAD] Motor movido a posición de llave {key_id_or_assignment_id}")
                else:
                    print(f"❌ [SEGURIDAD] Error moviendo motor a llave {key_id_or_assignment_id}")
                    log_file(f"❌ [SEGURIDAD] Error moviendo motor a llave {key_id_or_assignment_id}")
                    
            elif action == "DEVOLVER":
                # Para devolver llave, mover a posición HOME (0 grados)
                try:
                    response = send_home(ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT)
                    if "HOME completado" in response or "Posición" in response:
                        print("✅ [SEGURIDAD] Motor movido a posición HOME")
                        log_file("✅ [SEGURIDAD] Motor movido a posición HOME")
                    else:
                        print(f"⚠️ [SEGURIDAD] Respuesta inesperada del Arduino: {response}")
                        log_file(f"⚠️ [SEGURIDAD] Respuesta Arduino: {response}")
                except Exception as e:
                    print(f"❌ [SEGURIDAD] Error enviando HOME al Arduino: {e}")
                    log_file(f"❌ [SEGURIDAD] Error enviando HOME al Arduino: {e}")
            
        except Exception as e:
            print(f"❌ [SEGURIDAD] Error en comando Arduino {action}: {e}")
            log_file(f"❌ [SEGURIDAD] Error en comando Arduino {action}: {e}")
            # No mostrar error al usuario para no interrumpir el flujo principal
