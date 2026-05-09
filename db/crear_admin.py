from db.database import get_connection

def crear_admin():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE documento=?",
        ("1001",)
    )

    admin = cursor.fetchone()

    if not admin:
        cursor.execute("""
        INSERT INTO usuarios 
        (nombre, documento, id_profesional, especialidad, email, password, rol, imagen, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Admin Principal",
            "1001",
            "ADMIN001",
            "",
            "admin@demo.com",
            "12345",
            "admin",
            None,
            1
        ))

        conn.commit()
        print("Admin creado")

    conn.close()