#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instructor_interface.py
- Interfaz de instructor (PySide6)
"""

import styles
from config import *
from utils import *
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox, QPushButton, QApplication, QDialog
from PySide6.QtCore import Qt
from key_manager import KeyManager
from fingerprint_validator import FingerprintValidator
from db_utils import get_instructor_week_schedule, get_personal_by_id, db_connect
from typing import List, Dict, Any

class InstructorInterface:
    def __init__(self, parent, user: dict | None = None):
        self.parent = parent
        self._km = KeyManager()
        # Si viene el usuario autenticado, establecerlo para no pedir huella otra vez
        try:
            if user and 'id' in user:
                full = get_personal_by_id(int(user['id']))
                if full:
                    self._km.current_user = full
        except Exception:
            pass
        self._schedule_data = None
        self._status_by_day = {}
        
    def show_instructor_interface(self):
        instructor_win = styles.create_modal_window(self.parent, "👨‍🏫 INTERFAZ DE INSTRUCTOR - SISTEMA CEFA", "1000x700")
        main_layout = QVBoxLayout(instructor_win)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        self._create_futuristic_header(instructor_win, main_layout)

        # Scroll central para contenido responsive
        scroll = styles.create_scroll_area(instructor_win)
        content = styles.create_main_frame(scroll)
        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)

        info_layout = QVBoxLayout(content)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(12)

        self._show_assigned_environment_futuristic(content, info_layout)
        self._show_instructor_calendar(content, info_layout)

        self._create_futuristic_footer(instructor_win, instructor_win, main_layout)
        styles.center_window(instructor_win)
        instructor_win.show()

    def _create_futuristic_header(self, parent, layout):
        header = styles.create_main_frame(parent)
        header_layout = QVBoxLayout(header)
        icon = styles.create_title_label(header, "👨‍🏫")
        # Obtener nombre desde KeyManager si está autenticado
        welcome_name = "INSTRUCTOR"
        try:
            if self._km.current_user:
                welcome_name = f"{self._km.current_user.get('nombres','').strip()} {self._km.current_user.get('apellidos','').strip()}".strip() or "INSTRUCTOR"
        except Exception:
            pass
        title = styles.create_title_label(header, f"¡BIENVENIDO {welcome_name}!")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        layout.addWidget(header)

    def _show_assigned_environment_futuristic(self, parent, layout):
        block = styles.create_main_frame(parent)
        block_layout = QVBoxLayout(block)
        block_layout.addWidget(styles.create_subtitle_label(block, "AMBIENTE ASIGNADO"))
        details = [
            ("📍", "AULA PRINCIPAL", "Aula 101 - Laboratorio de Programación"),
            ("🔧", "EQUIPOS", "25 computadoras, Proyector 4K, Pizarra digital"),
            ("👥", "CAPACIDAD", "30 estudiantes"),
            ("🌐", "CONECTIVIDAD", "WiFi de alta velocidad, Red cableada"),
            ("📚", "RECURSOS", "Software de desarrollo, Bibliotecas digitales"),
        ]
        for icon, label, value in details:
            row = styles.create_main_frame(block)
            row_layout = QHBoxLayout(row)
            row_layout.addWidget(QLabel(icon))
            row_layout.addWidget(styles.create_info_label(block, f"{label}:"))
            row_layout.addWidget(styles.create_info_label(block, value))
            row_layout.addStretch(1)
            block_layout.addWidget(row)
        layout.addWidget(block)

    def _show_instructor_calendar(self, parent, layout):
        # Encabezado mejorado
        card = styles.create_card(parent)
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(20, 16, 20, 16)
        card_l.setSpacing(12)
        
        # Título con icono
        title_frame = QHBoxLayout()
        title_frame.addWidget(QLabel("📅"))
        title_frame.addWidget(styles.create_subtitle_label(card, "HORARIO DE CLASES"))
        title_frame.addStretch(1)
        card_l.addLayout(title_frame)

        # Cargar programación real por instructor
        personal_id = None
        try:
            if self._km.current_user:
                personal_id = self._km.current_user.get('id')
        except Exception:
            pass
        
        schedule = []
        day_order = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
        if personal_id:
            week = get_instructor_week_schedule(personal_id)
            for d in day_order:
                items = week.get(d, [])
                if items:
                    pretty = d.capitalize() if d != "MIERCOLES" else "Miércoles"
                    mapped = []
                    for it in items:
                        t = f"{it['inicio']} - {it['fin']}" if it.get('inicio') and it.get('fin') else (it.get('inicio') or '')
                        mapped.append((t, it.get('tipo') or 'Clase', it.get('ambiente') or '', it.get('ambiente_id')))
                    schedule.append((pretty, mapped))
        
        # Si no hay datos reales, mostrar mensaje informativo
        if not schedule:
            no_data_frame = styles.create_main_frame(card)
            no_data_l = QVBoxLayout(no_data_frame)
            no_data_l.setContentsMargins(20, 20, 20, 20)
            no_data_l.addWidget(QLabel("📭"))
            no_data_l.addWidget(styles.create_info_label(no_data_frame, "No hay programación disponible"))
            no_data_l.addWidget(styles.create_info_label(no_data_frame, "Contacte al administrador para configurar su horario"))
            card_l.addWidget(no_data_frame)
            layout.addWidget(card)
            return
            
        self._schedule_data = schedule

        # Selector de días mejorado - solo mostrar días con programación
        days_bar = QWidget(card)
        hb = QHBoxLayout(days_bar)
        hb.setContentsMargins(0, 0, 0, 0)
        hb.setSpacing(12)
        card_l.addWidget(days_bar)

        # Crear botones de días solo para días con programación
        self._day_buttons = {}
        for i, (day, _) in enumerate(schedule):
            btn = QPushButton(f"📅 {day}", days_bar)
            btn.setProperty("class", "warning")
            btn.setObjectName("warning")
            btn.setCursor(Qt.PointingHandCursor)
            # Usar una función auxiliar para evitar problemas con lambda
            def make_click_handler(day_name):
                def handler():
                    self._populate_day(day_name)
                return handler
            btn.clicked.connect(make_click_handler(day))
            hb.addWidget(btn)
            self._day_buttons[day] = btn
        hb.addStretch(1)

        # Contenedor principal para las clases
        self._day_container = QWidget(card)
        self._day_layout = QVBoxLayout(self._day_container)
        self._day_layout.setContentsMargins(0, 8, 0, 0)
        self._day_layout.setSpacing(8)
        card_l.addWidget(self._day_container)

        # Mostrar el primer día por defecto
        if schedule:
            self._populate_day(schedule[0][0])
        layout.addWidget(card)

    def _populate_day(self, day: str):
        # Limpiar contenido anterior
        while self._day_layout.count():
            item = self._day_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
        
        # Marcar botón activo visualmente
        for name, btn in self._day_buttons.items():
            try:
                if name == day:
                    btn.setStyleSheet(btn.styleSheet() + "font-weight: 800; background-color: #00d4ff; color: #0a0e1a;")
                else:
                    btn.setStyleSheet(btn.styleSheet().replace("font-weight: 800; background-color: #00d4ff; color: #0a0e1a;", ""))
            except Exception:
                pass
        
        # Cargar items del día
        items = []
        found = False
        
        for d, lst in (self._schedule_data or []):
            if d == day:
                items = lst
                found = True
                break
                
        if not found:
            # Si no hay registros para ese día, mostrar un mensaje elegante
            empty = styles.create_card(self._day_container)
            e_l = QVBoxLayout(empty)
            e_l.setContentsMargins(20, 20, 20, 20)
            e_l.addWidget(QLabel("📭"))
            e_l.addWidget(styles.create_info_label(empty, f"No hay clases programadas para {day}"))
            self._day_layout.addWidget(empty)
            return
            
        # Verificar estado actual de llaves
        current_taken = False
        try:
            if self._km and self._km.current_user:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
                current_taken = len(assignments) > 0
        except Exception:
            pass
        self._status_by_day[day] = current_taken

        # Verificar si es el día actual
        import datetime
        now = datetime.datetime.now()
        weekday_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        today_name = weekday_map.get(now.weekday())
        today_is_selected = (day == today_name)

        # Mostrar información del día actual
        if today_is_selected:
            info_frame = styles.create_main_frame(self._day_container)
            info_l = QHBoxLayout(info_frame)
            info_l.setContentsMargins(12, 8, 12, 8)
            info_l.addWidget(QLabel("📅"))
            info_l.addWidget(styles.create_info_label(info_frame, f"Hoy es {day} - Puede gestionar llaves"))
            info_l.addStretch(1)
            self._day_layout.addWidget(info_frame)

        # Mostrar cada clase del día
        for t, title, room, ambiente_id in items:
            # Crear tarjeta para cada clase
            class_card = styles.create_card(self._day_container)
            class_l = QVBoxLayout(class_card)
            class_l.setContentsMargins(16, 12, 16, 12)
            class_l.setSpacing(8)
            
            # Información de la clase
            time_label = styles.create_subtitle_label(class_card, f"🕐 {t}")
            class_l.addWidget(time_label)
            
            class_info = QHBoxLayout()
            class_info.addWidget(QLabel("📚"))
            class_info.addWidget(styles.create_info_label(class_card, f"{title}"))
            class_info.addStretch(1)
            class_l.addLayout(class_info)
            
            room_info = QHBoxLayout()
            room_info.addWidget(QLabel("🏫"))
            room_info.addWidget(styles.create_info_label(class_card, f"{room}"))
            room_info.addStretch(1)
            class_l.addLayout(room_info)
            
            # Acciones de llave
            actions = QHBoxLayout()
            actions.setContentsMargins(0, 8, 0, 0)
            actions.setSpacing(12)
            
            # Estado actual
            if current_taken:
                status_chip = styles.create_status_chip(class_card, "🔑 Llave Tomada", "success")
            else:
                status_chip = styles.create_status_chip(class_card, "⏳ Pendiente", "warning")
            actions.addWidget(status_chip)
            
            # Botones de acción - usar funciones auxiliares para evitar problemas con lambda
            def make_take_handler(day_name, time_range, class_title, room_name, env_id):
                def handler():
                    self._take_key_flow(day_name, time_range, class_title, room_name, env_id)
                return handler
            
            def make_return_handler(day_name, time_range, class_title, room_name, env_id):
                def handler():
                    self._return_key_flow(day_name, time_range, class_title, room_name, env_id)
                return handler
            
            take_btn = QPushButton("🔑 Tomar Llave", class_card)
            take_btn.setProperty("class", "accent")
            take_btn.setObjectName("accent")
            take_btn.setCursor(Qt.PointingHandCursor)
            take_btn.clicked.connect(make_take_handler(day, t, title, room, ambiente_id))
            
            return_btn = QPushButton("↩️ Devolver", class_card)
            return_btn.setProperty("class", "danger")
            return_btn.setObjectName("danger")
            return_btn.setCursor(Qt.PointingHandCursor)
            return_btn.clicked.connect(make_return_handler(day, t, title, room, ambiente_id))
            
            # Validar si puede operar (solo en el día actual)
            can_operate = today_is_selected
            # Por ahora, permitir operar en el día actual sin validación estricta de horario
            # Esto permite mayor flexibilidad al instructor

            # Configurar botones según el estado
            take_btn.setEnabled(not current_taken and can_operate)
            return_btn.setEnabled(current_taken and can_operate)
            
            # Agregar tooltips informativos
            if not today_is_selected:
                take_btn.setToolTip("Solo puede gestionar llaves en el día actual")
                return_btn.setToolTip("Solo puede gestionar llaves en el día actual")
            else:
                take_btn.setToolTip("Hacer clic para tomar la llave del ambiente")
                return_btn.setToolTip("Hacer clic para devolver la llave del ambiente")
            
            actions.addWidget(take_btn)
            actions.addWidget(return_btn)
            actions.addStretch(1)
            
            class_l.addLayout(actions)
            self._day_layout.addWidget(class_card)

    def _create_futuristic_footer(self, parent, window, layout):
        footer = styles.create_main_frame(parent)
        footer_layout = QHBoxLayout(footer)
        logout_btn = styles.create_danger_button(footer, "🚪 CERRAR SESIÓN", window.close)
        footer_layout.addStretch(1)
        footer_layout.addWidget(logout_btn)
        layout.addWidget(footer)

    def _get_keys_for_environment(self, environment_id: int, room_name: str) -> List[Dict[str, Any]]:
        """Busca llaves para un ambiente de manera más flexible"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor(dictionary=True)
                
                # Primero buscar llaves disponibles
                query_available = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, activo, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE activo = 1 AND estado = 'DISPONIBLE' AND ambiente_id = %s
                    ORDER BY codigo_llave
                """
                cur.execute(query_available, (environment_id,))
                available_keys = cur.fetchall()
                
                if available_keys:
                    cur.close()
                    return available_keys
                
                # Si no hay disponibles, buscar cualquier llave del ambiente que no esté perdida
                query_any = """
                    SELECT id, codigo_llave, descripcion, ambiente_id, estado, activo, 
                           angulo_grados, modulo, posicion_circular, tipo_llave
                    FROM llaves 
                    WHERE activo = 1 AND ambiente_id = %s AND estado != 'PERDIDA'
                    ORDER BY codigo_llave
                """
                cur.execute(query_any, (environment_id,))
                any_keys = cur.fetchall()
                
                cur.close()
                return any_keys
                
        except Exception as e:
            print(f"❌ Error buscando llaves para ambiente {environment_id}: {e}")
            return []

    def _assign_key_directly(self, user_id: int, key_id: int, observations: str = "") -> bool:
        """Asigna una llave directamente sin validaciones estrictas de estado"""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor()
                
                # Verificar que la llave existe y está activa
                cur.execute("SELECT id, estado FROM llaves WHERE id = %s AND activo = 1", (key_id,))
                key_info = cur.fetchone()
                if not key_info:
                    print(f"❌ La llave {key_id} no existe o no está activa")
                    return False
                
                # Crear la asignación sin verificar el estado de la llave
                insert_query = """
                    INSERT INTO asignaciones_llaves 
                    (personal_id, llave_id, fecha_asignacion, estado, motivo, created_at)
                    VALUES (%s, %s, NOW(), 'ACTIVA', %s, NOW())
                """
                cur.execute(insert_query, (user_id, key_id, observations))
                
                # Actualizar estado de la llave a ASIGNADA
                cur.execute("UPDATE llaves SET estado = 'ASIGNADA' WHERE id = %s", (key_id,))
                
                cnx.commit()
                cur.close()
                
                print(f"✅ Llave {key_id} asignada exitosamente a usuario {user_id}")
                
                # Registrar en logs
                from db_utils import log_access
                log_access(user_id, 'ENTREGA_LLAVE', f"Llave {key_id} asignada - {observations}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error en asignación directa: {e}")
            return False

    def _show_progress(self, text: str) -> QDialog:
        dlg = styles.create_modal_window(self.parent, "Procesando...", "420x160")
        try:
            dlg.setObjectName("progressDialog")
        except Exception:
            pass
        lay = QVBoxLayout(dlg)
        lay.addWidget(styles.create_subtitle_label(dlg, text))
        dlg.show()
        QApplication.processEvents()
        return dlg

    def _take_key_flow(self, day: str, time_range: str, title: str, room: str, ambiente_id: int = None):
        # Si ya hay usuario autenticado, no pedir huella
        if self._km and self._km.current_user:
            try:
                # Usar el ambiente_id de la programación si está disponible
                env_id = ambiente_id
                if not env_id:
                    from utils import query_latest_environment
                    env_info = query_latest_environment(self._km.current_user['id'])
                    env_id = env_info[0] if env_info else None
                
                # Buscar llaves de manera más flexible
                keys = self._get_keys_for_environment(env_id, room)
                if not keys:
                    QMessageBox.information(self.parent, "Sin llaves", f"No hay llaves disponibles para el ambiente {room}")
                    return
                
                key_id = keys[0]['id']
                # Usar la función directa de db_utils en lugar de KeyManager para evitar validaciones estrictas
                ok = self._assign_key_directly(self._km.current_user['id'], key_id, f"{day} {time_range} - {title} ({room})")
                if ok:
                    # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                    self._send_arduino_command(key_id, "TOMAR")
                    
                    try:
                        from desktop_alerts import desktop_alert_system
                        desktop_alert_system.show_key_assigned_alert(keys[0]['codigo_llave'], f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    except Exception:
                        QMessageBox.information(self.parent, "✅ Llave entregada", f"Se asignó la llave {keys[0]['codigo_llave']} a {self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    # Actualizar estado visual: tomada
                    self._status_by_day[day] = True
                    self._populate_day(day)
                else:
                    QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")
                return
            except Exception as e:
                QMessageBox.warning(self.parent, "⚠️", f"No fue posible completar la operación: {e}")
                return

        progress = self._show_progress("👆 Iniciando escaneo para tomar llave...")
        try:
            validator = FingerprintValidator()
            if not validator.connect():
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo conectar al lector biométrico")
                return
            scanned = validator.scan_fingerprint()
            if not scanned:
                QMessageBox.warning(self.parent, "⚠️ Escaneo", "No se obtuvo huella válida")
                return
            user = validator.validate_fingerprint_against_database(scanned)
            validator.disconnect()
            if not user:
                QMessageBox.critical(self.parent, "Acceso denegado", "Huella no coincide con ningún usuario")
                return
            # Autenticar en KeyManager y obtener ambiente
            self._km.authenticate_user(user['id'])
            env_id = ambiente_id
            if not env_id:
                from utils import query_latest_environment
                env_info = query_latest_environment(user['id'])
                env_id = env_info[0] if env_info else None
            
            # Buscar llaves de manera más flexible
            keys = self._get_keys_for_environment(env_id, room)
            if not keys:
                QMessageBox.information(self.parent, "Sin llaves", f"No hay llaves disponibles para el ambiente {room}")
                return
            key_id = keys[0]['id']
            # Usar la función directa de db_utils en lugar de KeyManager para evitar validaciones estrictas
            ok = self._assign_key_directly(user['id'], key_id, f"{day} {time_range} - {title} ({room})")
            if ok:
                # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                self._send_arduino_command(key_id, "TOMAR")
                
                QMessageBox.information(self.parent, "✅ Llave entregada", f"Se asignó la llave {keys[0]['codigo_llave']} a {user['nombres']} {user['apellidos']}")
            else:
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo asignar la llave")
        finally:
            progress.close()

    def _return_key_directly(self, assignment_id: int, observations: str = "") -> bool:
        """Marca una asignación como devuelta y libera la llave directamente."""
        try:
            with db_connect() as cnx:
                cur = cnx.cursor()
                cur.execute("SELECT llave_id, personal_id FROM asignaciones_llaves WHERE id = %s AND estado = 'ACTIVA'", (assignment_id,))
                row = cur.fetchone()
                if not row:
                    print(f"❌ Asignación {assignment_id} no encontrada o no activa")
                    return False
                key_id = row[0]
                personal_id = row[1] if len(row) > 1 else None
                cur.execute("""
                    UPDATE asignaciones_llaves 
                    SET estado = 'DEVUELTA', fecha_devolucion = NOW(), 
                        notas = CONCAT(IFNULL(notas, ''), ' | Devolución: ', %s),
                        updated_at = NOW()
                    WHERE id = %s
                """, (observations, assignment_id))
                cur.execute("UPDATE llaves SET estado = 'DISPONIBLE' WHERE id = %s", (key_id,))
                cnx.commit()
                cur.close()
                try:
                    from db_utils import log_access
                    if personal_id:
                        log_access(personal_id, 'DEVOLUCION_LLAVE', f"Llave {key_id} devuelta - {observations}")
                except Exception:
                    pass
                print(f"✅ Llave {key_id} devuelta (asignación {assignment_id})")
                return True
        except Exception as e:
            print(f"❌ Error en devolución directa: {e}")
            return False
    def _return_key_flow(self, day: str, time_range: str, title: str, room: str, ambiente_id: int = None):
        # Si ya hay usuario autenticado, no pedir huella
        if self._km and self._km.current_user:
            try:
                assignments = self._km.show_user_keys(self._km.current_user['id'])
                if not assignments:
                    QMessageBox.information(self.parent, "Sin asignaciones", "No hay llaves activas para devolver")
                    return
                
                # Buscar la asignación correcta por ambiente si está disponible
                assignment_id = assignments[-1]['id']  # Por defecto la última
                if ambiente_id:
                    for assignment in assignments:
                        # Verificar si la llave pertenece al ambiente correcto
                        try:
                            from utils import get_key_environment
                            key_env = get_key_environment(assignment.get('llave_id'))
                            if key_env and key_env.get('id') == ambiente_id:
                                assignment_id = assignment['id']
                                break
                        except Exception:
                            pass
                
                # obtener código de llave para mostrar en alertas
                key_code = None
                try:
                    assignment_obj = next(a for a in assignments if a['id'] == assignment_id)
                    key_code = assignment_obj.get('llave_codigo')
                except Exception:
                    pass
                ok = self._return_key_directly(assignment_id, f"Devolución: {day} {time_range} - {title} ({room})")
                if ok:
                    # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                    self._send_arduino_command(assignment_id, "DEVOLVER")
                    
                    try:
                        from desktop_alerts import desktop_alert_system
                        desktop_alert_system.show_key_returned_alert(key_code, f"{self._km.current_user['nombres']} {self._km.current_user['apellidos']}")
                    except Exception:
                        if key_code:
                            QMessageBox.information(self.parent, "✅ Llave devuelta", f"Se devolvió la llave {key_code} correctamente")
                        else:
                            QMessageBox.information(self.parent, "✅ Llave devuelta", "Devolución registrada correctamente")
                    # Actualizar estado visual: pendiente
                    self._status_by_day[day] = False
                    self._populate_day(day)
                else:
                    QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")
                return
            except Exception as e:
                QMessageBox.warning(self.parent, "⚠️", f"No fue posible completar la operación: {e}")
                return

        progress = self._show_progress("👆 Escanee su huella para devolver la llave...")
        try:
            validator = FingerprintValidator()
            if not validator.connect():
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo conectar al lector biométrico")
                return
            scanned = validator.scan_fingerprint()
            if not scanned:
                QMessageBox.warning(self.parent, "⚠️ Escaneo", "No se obtuvo huella válida")
                return
            user = validator.validate_fingerprint_against_database(scanned)
            validator.disconnect()
            if not user:
                QMessageBox.critical(self.parent, "Acceso denegado", "Huella no coincide con ningún usuario")
                return
            self._km.authenticate_user(user['id'])
            # Buscar la asignación correcta del usuario
            assignments = self._km.show_user_keys(user['id'])
            if not assignments:
                QMessageBox.information(self.parent, "Sin asignaciones", "No hay llaves activas para devolver")
                return
            
            # Buscar la asignación correcta por ambiente si está disponible
            assignment_id = assignments[-1]['id']  # Por defecto la última
            if ambiente_id:
                for assignment in assignments:
                    # Verificar si la llave pertenece al ambiente correcto
                    try:
                        from utils import get_key_environment
                        key_env = get_key_environment(assignment.get('llave_id'))
                        if key_env and key_env.get('id') == ambiente_id:
                            assignment_id = assignment['id']
                            break
                    except Exception:
                        pass
            
            # obtener código de llave para mostrar en mensajes
            key_code = None
            try:
                assignment_obj = next(a for a in assignments if a['id'] == assignment_id)
                key_code = assignment_obj.get('llave_codigo')
            except Exception:
                pass
            ok = self._return_key_directly(assignment_id, f"Devolución: {day} {time_range} - {title} ({room})")
            if ok:
                # 🤖 ENVIAR COMANDO AL ARDUINO PARA MOVER MOTOR
                self._send_arduino_command(assignment_id, "DEVOLVER")
                
                if key_code:
                    QMessageBox.information(self.parent, "✅ Llave devuelta", f"Se devolvió la llave {key_code} correctamente")
                else:
                    QMessageBox.information(self.parent, "✅ Llave devuelta", "Devolución registrada correctamente")
            else:
                QMessageBox.critical(self.parent, "❌ Error", "No se pudo registrar la devolución")
        finally:
            progress.close()

    def _send_arduino_command(self, key_id_or_assignment_id: int, action: str):
        """
        Envía comando al Arduino para mover el motor NEMA17 a la posición de la llave
        
        Args:
            key_id_or_assignment_id: ID de la llave o asignación
            action: "TOMAR" o "DEVOLVER"
        """
        try:
            from utils import open_key_by_id_steps as open_key_by_id, open_environment_key, log_file
            from config import ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT
            
            print(f"🤖 Enviando comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            log_file(f"🤖 Comando Arduino: {action} - ID: {key_id_or_assignment_id}")
            
            if action == "TOMAR":
                # Para tomar llave, mover a la posición de la llave
                success = open_key_by_id(key_id_or_assignment_id, dwell_seconds=5)
                if success:
                    print(f"✅ Motor movido a posición de llave {key_id_or_assignment_id}")
                    log_file(f"✅ Motor movido a posición de llave {key_id_or_assignment_id}")
                else:
                    print(f"❌ Error moviendo motor a llave {key_id_or_assignment_id}")
                    log_file(f"❌ Error moviendo motor a llave {key_id_or_assignment_id}")
                    
            elif action == "DEVOLVER":
                # Para devolver llave, mover a posición HOME (0 grados)
                from utils import send_home
                try:
                    response = send_home(ARDUINO_PORT_DEFAULT, ARDUINO_BAUD_DEFAULT)
                    if "HOME completado" in response or "Posición" in response:
                        print("✅ Motor movido a posición HOME")
                        log_file("✅ Motor movido a posición HOME")
                    else:
                        print(f"⚠️ Respuesta inesperada del Arduino: {response}")
                        log_file(f"⚠️ Respuesta Arduino: {response}")
                except Exception as e:
                    print(f"❌ Error enviando HOME al Arduino: {e}")
                    log_file(f"❌ Error enviando HOME al Arduino: {e}")
            
        except Exception as e:
            print(f"❌ Error en comando Arduino {action}: {e}")
            log_file(f"❌ Error en comando Arduino {action}: {e}")
            # No mostrar error al usuario para no interrumpir el flujo principal
            # El sistema seguirá funcionando sin el Arduino

