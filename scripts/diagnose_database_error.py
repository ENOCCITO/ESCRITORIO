#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnose_database_error.py
- Diagnóstico específico del error de guardado en base de datos
- Identifica exactamente qué está fallando
"""

import tkinter as tk
from src.core.biometric_scanner import BiometricScanner
from src.utils.utils import db_connect
import traceback

def diagnose_database_error():
    """Diagnostica el error específico de guardado en base de datos"""
    print("🔍 DIAGNÓSTICO DE ERROR DE BASE DE DATOS")
    print("=" * 60)
    
    try:
        # 1. Probar conexión a base de datos
        print("1️⃣ Probando conexión a base de datos...")
        try:
            with db_connect() as cnx:
                cur = cnx.cursor()
                print("✅ Conexión a base de datos exitosa")
                
                # Verificar tabla personal
                cur.execute("SHOW TABLES LIKE 'personal'")
                if not cur.fetchone():
                    print("❌ La tabla 'personal' no existe")
                    return False
                print("✅ Tabla 'personal' encontrada")
                
                # Verificar estructura
                cur.execute("DESCRIBE personal")
                columns = cur.fetchall()
                huella_column = None
                for col in columns:
                    if col[0] == 'huella_digital':
                        huella_column = col
                        break
                
                if not huella_column:
                    print("❌ Campo 'huella_digital' no encontrado")
                    return False
                
                print(f"✅ Campo 'huella_digital' encontrado: {huella_column[1]}")
                
                # Verificar personas activas
                cur.execute("SELECT COUNT(*) FROM personal WHERE activo = 1")
                count = cur.fetchone()[0]
                print(f"✅ Personas activas: {count}")
                
                if count == 0:
                    print("❌ No hay personas activas")
                    return False
                
                # Obtener una persona para probar
                cur.execute("SELECT id, nombres, apellidos FROM personal WHERE activo = 1 LIMIT 1")
                person = cur.fetchone()
                if not person:
                    print("❌ No se pudo obtener una persona")
                    return False
                
                person_id, nombres, apellidos = person
                print(f"✅ Persona de prueba: {nombres} {apellidos} (ID: {person_id})")
                
        except Exception as e:
            print(f"❌ Error en conexión a BD: {e}")
            print(f"❌ Tipo: {type(e).__name__}")
            traceback.print_exc()
            return False
        
        # 2. Probar guardado directo
        print("\n2️⃣ Probando guardado directo...")
        try:
            # Crear datos de prueba
            test_data = b"TEST_FINGERPRINT_DATA_" + str(person_id).encode()
            print(f"🧪 Datos de prueba: {len(test_data)} bytes")
            
            # Probar UPDATE directo
            update_query = """
                UPDATE personal 
                SET huella_digital = %s, 
                    fecha_registro_huella = NOW(),
                    updated_at = NOW()
                WHERE id = %s AND activo = 1
            """
            
            with db_connect() as cnx:
                cur = cnx.cursor()
                cur.execute(update_query, (test_data, person_id))
                cnx.commit()
                
                if cur.rowcount > 0:
                    print("✅ UPDATE directo exitoso")
                    
                    # Verificar que se guardó
                    cur.execute("SELECT huella_digital FROM personal WHERE id = %s", (person_id,))
                    result = cur.fetchone()
                    
                    if result and result[0]:
                        print(f"✅ Datos verificados en BD: {len(result[0])} bytes")
                        
                        # Limpiar datos de prueba
                        cur.execute("UPDATE personal SET huella_digital = NULL WHERE id = %s", (person_id,))
                        cnx.commit()
                        print("🧹 Datos de prueba limpiados")
                        
                        return True
                    else:
                        print("❌ Los datos no se guardaron correctamente")
                        return False
                else:
                    print("❌ No se pudo actualizar la persona")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en guardado directo: {e}")
            print(f"❌ Tipo: {type(e).__name__}")
            traceback.print_exc()
            return False
        
        # 3. Probar con el método del scanner
        print("\n3️⃣ Probando con método del scanner...")
        try:
            scanner = BiometricScanner()
            
            # Probar guardado con datos de prueba
            success, message = scanner.test_database_save(person_id)
            
            if success:
                print("✅ Método del scanner exitoso")
                return True
            else:
                print(f"❌ Método del scanner falló: {message}")
                return False
                
        except Exception as e:
            print(f"❌ Error en método del scanner: {e}")
            print(f"❌ Tipo: {type(e).__name__}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error general en diagnóstico: {e}")
        traceback.print_exc()
        return False

def test_with_gui():
    """Prueba con interfaz gráfica"""
    print("\n🖥️ INICIANDO DIAGNÓSTICO CON INTERFAZ GRÁFICA")
    print("=" * 60)
    
    try:
        # Crear ventana de diagnóstico
        root = tk.Tk()
        root.title("Diagnóstico - Error de Base de Datos")
        root.geometry("600x500")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🔍 DIAGNÓSTICO DE ERROR",
            font=("Segoe UI", 18, "bold"),
            fg="#ff6b6b",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Este diagnóstico identifica exactamente qué está fallando:

1️⃣ Conexión a base de datos
2️⃣ Estructura de la tabla personal
3️⃣ Guardado directo con UPDATE
4️⃣ Método del scanner biométrico
5️⃣ Verificación de datos guardados
        """
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=("Segoe UI", 11),
            fg="#cccccc",
            bg="#1a1a2e",
            justify="left"
        )
        info_label.pack(pady=(0, 20))
        
        # Botón para ejecutar diagnóstico
        test_btn = tk.Button(
            main_frame,
            text="🔍 EJECUTAR DIAGNÓSTICO",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            activeforeground="#ffffff",
            activebackground="#ff5252",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: diagnose_database_error()
        )
        test_btn.pack(pady=20)
        
        # Botón de salir
        exit_btn = tk.Button(
            main_frame,
            text="❌ SALIR",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#666666",
            activeforeground="#ffffff",
            activebackground="#555555",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=root.destroy
        )
        exit_btn.pack(side="bottom", pady=(20, 0))
        
        print("✅ Ventana de diagnóstico creada")
        print("   - Haz clic en 'EJECUTAR DIAGNÓSTICO'")
        print("   - Revisa la consola para ver los resultados detallados")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la interfaz: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DE ERROR DE BASE DE DATOS")
    print("=" * 70)
    
    try:
        # Ejecutar diagnóstico
        if diagnose_database_error():
            print("\n✅ DIAGNÓSTICO COMPLETADO - TODO FUNCIONA")
        else:
            print("\n❌ DIAGNÓSTICO COMPLETADO - SE ENCONTRARON ERRORES")
        
        # Preguntar si quiere interfaz gráfica
        print("\n" + "="*60)
        response = input("¿Desea ejecutar el diagnóstico con interfaz gráfica? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            test_with_gui()
        
        print("\n✅ DIAGNÓSTICO FINALIZADO")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Diagnóstico interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el diagnóstico: {e}")
        traceback.print_exc()
