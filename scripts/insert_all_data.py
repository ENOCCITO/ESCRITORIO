import mysql.connector

cnx = mysql.connector.connect(host='localhost', user='root', password='', database='sicefa')
cur = cnx.cursor()

print("="*60)
print("📝 INSERTAR DATOS DE EJEMPLO EN SICEFA")
print("="*60)

try:
    # Primero insertar EPS
    print("\n1️⃣ Insertando EPS...")
    cur.execute("INSERT IGNORE INTO e_p_s (name) VALUES ('EPS PRINCIPAL')")
    cnx.commit()
    
    # Insertar Population Groups
    print("2️⃣ Insertando Grupos de población...")
    cur.execute("INSERT IGNORE INTO population_groups (name) VALUES ('GENERAL')")
    cnx.commit()
    
    # Insertar Pension Entities
    print("3️⃣ Insertando Entidades de pensión...")
    cur.execute("INSERT IGNORE INTO pension_entities (name) VALUES ('AFP PRINCIPAL')")
    cnx.commit()
    
    # Ahora insertar personas
    print("4️⃣ Insertando personas...")
    insert_people = """
    INSERT IGNORE INTO people (first_name, first_last_name, document_type, document_number, personal_email, eps_id, population_group_id, pension_entity_id)
    VALUES
    ('Juan', 'Pérez', '1', '1234567890', 'juan@example.com', 1, 1, 1),
    ('María', 'García', '1', '0987654321', 'maria@example.com', 1, 1, 1),
    ('Carlos', 'López', '1', '1122334455', 'carlos@example.com', 1, 1, 1),
    ('Ana', 'Martínez', '1', '5544332211', 'ana@example.com', 1, 1, 1),
    ('Pedro', 'Rodríguez', '1', '9876543210', 'pedro@example.com', 1, 1, 1),
    ('Laura', 'Gómez', '1', '1111111111', 'laura@example.com', 1, 1, 1),
    ('Miguel', 'Sánchez', '1', '2222222222', 'miguel@example.com', 1, 1, 1),
    ('Sofía', 'Torres', '1', '3333333333', 'sofia@example.com', 1, 1, 1),
    ('Diego', 'Rivera', '1', '4444444444', 'diego@example.com', 1, 1, 1),
    ('Valentina', 'Herrera', '1', '5555555555', 'valentina@example.com', 1, 1, 1);
    """
    cur.execute(insert_people)
    cnx.commit()
    
    # Contar resultados
    cur.execute("SELECT COUNT(*) FROM people")
    count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM ambientes WHERE activo = 1")
    ambientes = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM courses WHERE deleted_at IS NULL")
    courses = cur.fetchone()[0]
    
    print(f"\n✅ DATOS INSERTADOS CORRECTAMENTE")
    print(f"\n📊 RESUMEN:")
    print(f"   👥 Personas: {count}")
    print(f"   🏢 Ambientes: {ambientes}")
    print(f"   📚 Cursos: {courses}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

cur.close()
cnx.close()

print("\n" + "="*60)
print("Ahora puedes visualizar los datos en MySQL Workbench")
print("="*60)
