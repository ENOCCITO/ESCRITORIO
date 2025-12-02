import mysql.connector

cnx = mysql.connector.connect(host='localhost', user='root', password='', database='sicefa')
cur = cnx.cursor()

# Insertar personas simples con todos los campos requeridos
insert_people = """
INSERT INTO people (first_name, first_last_name, document_type, document_number, personal_email, eps_id, population_group_id, pension_entity_id)
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

try:
    cur.execute(insert_people)
    cnx.commit()
    print("✅ 10 personas insertadas correctamente")
except Exception as e:
    print(f"❌ Error: {e}")

# Ver datos
cur.execute("SELECT COUNT(*) FROM people WHERE document_type = '1'")
count = cur.fetchone()[0]
print(f"Total de personas: {count}")

cur.close()
cnx.close()
