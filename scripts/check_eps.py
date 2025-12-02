#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from src.utils.db_utils import db_connect

cnx = db_connect()
cur = cnx.cursor()

# Ver todas las tablas que mencionen eps
cur.execute("SHOW TABLES")
tables = cur.fetchall()
print("Tablas en la BD:")
for table in tables:
    print(f"  - {table[0]}")

# Chequear referencias en people
cur.execute("SHOW CREATE TABLE people")
result = cur.fetchone()
print(f"\nTabla people:")
print(result[1][:500])

cnx.close()
