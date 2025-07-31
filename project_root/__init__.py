import sqlite3
import os

nombre_db = 'database.db'

if not os.path.exists(nombre_db):
    print(f"❌ La base de datos '{nombre_db}' no se encuentra en la carpeta actual.")
else:
    try:
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()
        alter_sql = """
        ALTER TABLE tarjetas ADD COLUMN archivo_html VARCHAR(200) NOT NULL DEFAULT 'index.html';
        """
        cursor.execute(alter_sql)
        conn.commit()
        print("✅ Columna 'archivo_html' agregada correctamente a la tabla 'tarjetas'.")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Error al ejecutar ALTER TABLE: {e}")
    finally:
        conn.close()
