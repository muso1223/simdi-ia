from db.database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        documento TEXT UNIQUE,
        id_profesional TEXT,
        especialidad TEXT,
        email TEXT,
        password TEXT,
        rol TEXT,
        imagen TEXT,
        estado INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()

    print("Base de datos creada")