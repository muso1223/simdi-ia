from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO usuarios 
(nombre, documento, id_profesional, especialidad, email, password, rol, imagen, estado)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Admin Principal",
    "123456",
    "ADMIN001",
    "",
    "admin@demo.com",
    "1234",
    "admin",
    None,
    1
))

conn.commit()
conn.close()

print("Admin creado")