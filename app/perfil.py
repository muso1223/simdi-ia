import streamlit as st
import os
from db.database import get_connection

def perfil_usuario(user):
    st.title("Mi perfil")

    if "perfil_feedback" not in st.session_state:
        st.session_state.perfil_feedback = ""

    if st.session_state.perfil_feedback:
        st.success(st.session_state.perfil_feedback)

    # Campos de solo lectura
    st.write(f"**Nombre:** {user[1]}")
    st.write(f"**Documento:** {user[2]}")
    st.write(f"**ID Profesional:** {user[3]}")
    st.write(f"**Especialidad:** {user[4]}")
    st.write(f"**Rol:** {user[7]}")

    if user[8]:
        st.image(user[8], caption="Imagen actual", width=200)
    else:
        st.info("No tienes imagen de perfil configurada")

    st.divider()

    # Campos editables
    email = st.text_input("Email", value=user[5])

    st.subheader("Cambiar contraseña")
    current_password = st.text_input("Contraseña actual", type="password")
    new_password = st.text_input("Nueva contraseña", type="password")
    confirm_password = st.text_input("Confirmar nueva contraseña", type="password")

    st.subheader("Imagen de perfil")
    uploaded_image = st.file_uploader("Seleccionar imagen", type=["png", "jpg", "jpeg", "gif"])

    if st.button("Actualizar"):
        updates = []
        params = []

        # Email
        if email != user[5]:
            updates.append("email = ?")
            params.append(email)

        # Password
        if new_password:
            if current_password != user[6]:
                st.error("La contraseña actual es incorrecta")
                return
            if new_password != confirm_password:
                st.error("Las nuevas contraseñas no coinciden")
                return
            updates.append("password = ?")
            params.append(new_password)

        # Image
        image_path = user[8] if user[8] else None
        if uploaded_image:
            # Crear carpeta si no existe
            upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            # Nombre único
            ext = os.path.splitext(uploaded_image.name)[1]
            image_filename = f"user_{user[0]}{ext}"
            image_path = os.path.join(upload_dir, image_filename)

            # Guardar archivo
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            updates.append("imagen = ?")
            params.append(image_path)

        if not updates:
            st.warning("No hay cambios para actualizar")
            return

        # Actualizar DB
        conn = get_connection()
        cursor = conn.cursor()

        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
        params.append(user[0])

        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user[0],))
        updated_user = cursor.fetchone()
        conn.close()

        st.session_state.user = updated_user
        st.session_state.perfil_feedback = "Perfil actualizado correctamente"
        st.rerun()  # Para refrescar los valores mostrados