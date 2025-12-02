#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from src.utils.db_utils import db_connect

cnx = db_connect()
cur = cnx.cursor()

# Ver estructura de e_p_s
cur.execute("DESCRIBE e_p_s")
print("Estructura de e_p_s:")
for row in cur.fetchall():
    print(f"  {row}")

# Ver algunos registros existentes
cur.execute("SELECT * FROM e_p_s LIMIT 3")
print("\nPrimeros 3 registros de e_p_s:")
for row in cur.fetchall():
    print(f"  {row}")

cnx.close()
