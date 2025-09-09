#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_database_save.py
- Prueba específica para guardar huellas en la base de datos
- Verifica la conexión y el guardado en la tabla personal
"""

import tkinter as tk
from biometric_scanner import BiometricScanner
from utils import db_connect

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🗄️ PRUEBA DE CONEXIÓN A LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        # Probar conexión a la base de datos
        with db_connect() as cnx:
            cur = cnx.cursor()
            
            # Verificar que la tabla personal existe
            cur.execute("SHOW TABLES LIKE 'personal'")
            if not cur.fetchone():
                print("❌ La tabla 'personal' no existe")
                return False
            
            print("✅ Tabla 'personal' encontrada")
            
            # Verificar estructura de la tabla
            cur.execute("DESCRIBE personal")
            columns = cur.fetchall()
            
            print("📋 Estructura de la tabla 'personal':")
            for col in columns:
                print(f"   - {col[0]}: {col[1]}")
                if col[0] == 'huella_digital':
                    print(f"     ✅ Campo huella_digital encontrado: {col[1]}")
            
            # Verificar que hay personas en la tabla
            cur.execute("SELECT COUNT(*) FROM personal WHERE activo = 1")
            count = cur.fetchone()[0]
            print(f"👥 Personas activas en la tabla: {count}")
            
            if count == 0:
                print("⚠️ No hay personas activas en la tabla")
                return False
            
            # Mostrar algunas personas
            cur.execute("SELECT id, nombres, apellidos FROM personal WHERE activo = 1 LIMIT 5")
            people = cur.fetchall()
            
            print("👤 Algunas personas en la tabla:")
            for person in people:
                print(f"   - ID {person[0]}: {person[1]} {person[2]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def test_fingerprint_save():
    """Prueba el guardado de huella en la base de datos"""
    print("\n💾 PRUEBA DE GUARDADO DE HUELLA")
    print("=" * 60)
    
    try:
        # Crear instancia del lector
        scanner = BiometricScanner()
        
        # Conectar al lector
        if not scanner.test_com3_connection():
            print("❌ No se pudo conectar al lector biométrico")
            return False
        
        print("✅ Lector biométrico conectado")
        
        # Obtener una persona de la base de datos para probar
        with db_connect() as cnx:
            cur = cnx.cursor()
            cur.execute("SELECT id, nombres, apellidos FROM personal WHERE activo = 1 LIMIT 1")
            person = cur.fetchone()
            
            if not person:
                print("❌ No hay personas en la base de datos")
                return False
            
            person_id, nombres, apellidos = person
            person_name = f"{nombres} {apellidos}"
            
            print(f"👤 Probando con persona: {person_name} (ID: {person_id})")
            
            # Crear datos de prueba (simulando huella)
            test_fingerprint_data = b"TEST_FINGERPRINT_DATA_" + str(person_id).encode()
            
            print(f"💾 Guardando datos de prueba...")
            print(f"💾 Tamaño de datos: {len(test_fingerprint_data)} bytes")
            
            # Probar guardado
            if scanner.save_fingerprint_to_db(person_id, test_fingerprint_data):
                print("✅ ¡Huella guardada exitosamente!")
                
                # Verificar que se guardó
                cur.execute("SELECT huella_digital FROM personal WHERE id = %s", (person_id,))
                result = cur.fetchone()
                
                if result and result[0]:
                    print("✅ Huella verificada en la base de datos")
                    print(f"💾 Tamaño guardado: {len(result[0])} bytes")
                    
                    # Limpiar datos de prueba
                    cur.execute("UPDATE personal SET huella_digital = NULL WHERE id = %s", (person_id,))
                    cnx.commit()
                    print("🧹 Datos de prueba limpiados")
                    
                    return True
                else:
                    print("❌ La huella no se guardó correctamente")
                    return False
            else:
                print("❌ Error guardando la huella")
                return False
                
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'scanner' in locals():
            scanner.disconnect()

def test_with_gui():
    """Prueba con interfaz gráfica"""
    print("\n🖥️ INICIANDO PRUEBA CON INTERFAZ GRÁFICA")
    print("=" * 60)
    
    try:
        # Crear ventana de prueba
        root = tk.Tk()
        root.title("Prueba - Guardado en Base de Datos")
        root.geometry("500x400")
        root.configure(bg="#1a1a2e")
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="💾 PRUEBA DE BASE DE DATOS",
            font=("Segoe UI", 18, "bold"),
            fg="#00ffff",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_text = """
Esta prueba verifica el guardado de huellas:

✅ Conexión a la base de datos
✅ Estructura de la tabla personal
✅ Guardado de datos LONGBLOB
✅ Verificación del guardado
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
        
        # Botón para probar conexión
        test_db_btn = tk.Button(
            main_frame,
            text="🗄️ PROBAR BASE DE DATOS",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#4caf50",
            activeforeground="#ffffff",
            activebackground="#45a049",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: test_database_connection()
        )
        test_db_btn.pack(pady=10)
        
        # Botón para probar guardado
        test_save_btn = tk.Button(
            main_frame,
            text="💾 PROBAR GUARDADO",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#00ffff",
            activeforeground="#ffffff",
            activebackground="#00cccc",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: test_fingerprint_save()
        )
        test_save_btn.pack(pady=10)
        
        # Botón de salir
        exit_btn = tk.Button(
            main_frame,
            text="❌ SALIR",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#ff6b6b",
            activeforeground="#ffffff",
            activebackground="#ff5252",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=root.destroy
        )
        exit_btn.pack(side="bottom", pady=(20, 0))
        
        print("✅ Ventana de prueba creada")
        print("   - Haz clic en 'PROBAR BASE DE DATOS' primero")
        print("   - Luego haz clic en 'PROBAR GUARDADO'")
        print("   - Revisa la consola para ver los resultados")
        
        # Ejecutar
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error en la prueba GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE GUARDADO EN BASE DE DATOS")
    print("=" * 70)
    
    try:
        # Prueba de conexión a base de datos
        if test_database_connection():
            print("\n✅ Conexión a base de datos exitosa")
            
            # Preguntar si quiere probar guardado
            print("\n" + "="*60)
            response = input("¿Desea probar el guardado de huella? (s/n): ")
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                test_fingerprint_save()
        else:
            print("\n❌ Error en la conexión a la base de datos")
        
        # Preguntar si quiere prueba con GUI
        print("\n" + "="*60)
        response = input("¿Desea ejecutar la prueba con interfaz gráfica? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            test_with_gui()
        
        print("\n✅ PRUEBA COMPLETADA")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
