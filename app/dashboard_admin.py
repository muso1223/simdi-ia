import streamlit as st
import os
import pandas as pd
from db.database import get_connection
from email_validator import validate_email, EmailNotValidError


def admin_panel(user):

    st.title("Panel de Administración")

    # =========================
    # ESTADOS
    # =========================
    if "admin_view" not in st.session_state:
        st.session_state.admin_view = "list"

    if "usuario_editar" not in st.session_state:
        st.session_state.usuario_editar = None

    if "mostrar_inactivos" not in st.session_state:
        st.session_state.mostrar_inactivos = False

    # =========================
    # CAMBIAR VISTA
    # =========================
    if st.session_state.admin_view == "crear":
        formulario_usuario()
        return

    if st.session_state.admin_view == "editar":
        formulario_usuario(editar=True)
        return

    # =========================
    # HEADER ACCIONES
    # =========================
    colA, colB, colC = st.columns([2, 2, 3])

    with colA:
        if st.button("➕ Crear usuario"):
            st.session_state.admin_view = "crear"
            st.rerun()

    with colB:
        if st.button("👁️ Mostrar/Ocultar inactivos"):
            st.session_state.mostrar_inactivos = not st.session_state.mostrar_inactivos
            st.rerun()

    with colC:
        busqueda = st.text_input("🔍 Buscar por nombre o documento")

    st.divider()

    # =========================
    # CONSULTA
    # =========================
    conn = get_connection()

    if st.session_state.mostrar_inactivos:
        query = "SELECT * FROM usuarios"
    else:
        query = "SELECT * FROM usuarios WHERE estado = 1"

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        st.info("No hay usuarios registrados")
        return

    # =========================
    # FILTRO DE BÚSQUEDA
    # =========================
    if busqueda:
        busqueda = busqueda.lower()
        df = df[
            df["nombre"].str.lower().str.contains(busqueda) |
            df["documento"].astype(str).str.contains(busqueda)
        ]

    if df.empty:
        st.warning("No se encontraron resultados")
        return

    # =========================
    # LISTADO
    # =========================
    for idx, row in df.iterrows():

        estado = "🟢 Activo" if row["estado"] == 1 else "🔴 Inactivo"

        col1, col2, col3 = st.columns([4, 2, 2])

        with col1:
            st.markdown(f"**{row['nombre']}**")
            st.write(f"Documento: {row['documento']}")
            st.write(f"Rol: {row['rol']}")
            st.write(f"Estado: {estado}")

        # =========================
        # EDITAR
        # =========================
        with col2:
            if st.button("✏️ Editar", key=f"edit_{row['id']}"):
                st.session_state.usuario_editar = row.to_dict()
                st.session_state.admin_view = "editar"
                st.rerun()

        # =========================
        # ACTIVAR / DESACTIVAR
        # =========================
        with col3:
            conn = get_connection()
            cursor = conn.cursor()

            if row["estado"] == 1:
                if st.button("❌ Desactivar", key=f"del_{row['id']}"):
                    cursor.execute(
                        "UPDATE usuarios SET estado = 0 WHERE id = ?",
                        (row["id"],)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Usuario desactivado")
                    st.rerun()
            else:
                if st.button("✅ Reactivar", key=f"act_{row['id']}"):
                    cursor.execute(
                        "UPDATE usuarios SET estado = 1 WHERE id = ?",
                        (row["id"],)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Usuario reactivado")
                    st.rerun()

        st.divider()


# =========================
# FORMULARIO (CREAR / EDITAR)
# =========================
def formulario_usuario(editar=False):

    if editar:
        st.subheader("Editar usuario")
        data = st.session_state.usuario_editar
    else:
        st.subheader("Crear usuario")
        data = {}

    nombre = st.text_input("Nombre", value=data.get("nombre", ""))
    documento = st.text_input("Documento", value=data.get("documento", ""))
    id_prof = st.text_input("ID Profesional", value=data.get("id_profesional", ""))
    especialidad = st.text_input("Especialidad", value=data.get("especialidad", ""))
    email = st.text_input("Email", value=data.get("email", ""))
    imagen_actual = data.get("imagen", None)

    if pd.isna(imagen_actual):
        imagen_actual = None

    if editar and imagen_actual and os.path.exists(imagen_actual):

        st.image(imagen_actual, width=120)

        eliminar_imagen = st.checkbox("Eliminar imagen actual")

    else:
        eliminar_imagen = False

    nueva_imagen = st.file_uploader(
        "Subir nueva imagen",
        type=["png", "jpg", "jpeg"]
    )

    password = st.text_input("Password (dejar vacío para no cambiar)", type="password")

    rol = st.selectbox(
        "Rol",
        ["admin", "medico"],
        index=0 if data.get("rol", "admin") == "admin" else 1
    )

    col1, col2 = st.columns(2)

    # =========================
    # GUARDAR
    # =========================
    with col1:
        if st.button("Guardar"):

            # =========================
            # VALIDACIONES
            # =========================

            if not nombre.strip():
                st.warning("El nombre es obligatorio")
                return

            if len(nombre.strip()) < 3:
                st.warning("El nombre es demasiado corto")
                return

            if not documento.strip():
                st.warning("El documento es obligatorio")
                return

            if not documento.isdigit():
                st.warning("El documento solo debe contener números")
                return

            if len(documento) < 5:
                st.warning("Documento inválido")
                return

            if email:

                try:
                    validate_email(email)

                except EmailNotValidError:
                    st.warning("Correo electrónico inválido")
                    return

            # password obligatoria solo en creación
            if not editar:

                if not password:
                    st.warning("La contraseña es obligatoria")
                    return

                if len(password) < 4:
                    st.warning("La contraseña debe tener mínimo 4 caracteres")
                    return

            # password opcional en edición
            if editar and password:

                if len(password) < 4:
                    st.warning("La contraseña debe tener mínimo 4 caracteres")
                    return

            conn = get_connection()
            cursor = conn.cursor()

            ruta_imagen = imagen_actual

            try:

                # =========================
                # GUARDAR NUEVA IMAGEN
                # =========================

                if nueva_imagen:

                    carpeta = "uploads"

                    os.makedirs(carpeta, exist_ok=True)

                    ruta_imagen = os.path.join(
                        carpeta,
                        f"{documento}_{nueva_imagen.name}"
                    )

                    with open(ruta_imagen, "wb") as f:
                        f.write(nueva_imagen.getbuffer())

                # =========================
                # ELIMINAR IMAGEN
                # =========================

                if eliminar_imagen:

                    if imagen_actual and os.path.exists(imagen_actual):
                        os.remove(imagen_actual)

                    ruta_imagen = None

                if editar:
                    if password:
                        cursor.execute("""
                            UPDATE usuarios
                            SET nombre=?, documento=?, id_profesional=?, especialidad=?, email=?, password=?, rol=?, imagen=?
                            WHERE id=?
                        """, (
                            nombre, documento, id_prof, especialidad, email, password, rol, ruta_imagen,
                            data["id"]
                        ))
                    else:
                        cursor.execute("""
                            UPDATE usuarios
                            SET nombre=?, documento=?, id_profesional=?, especialidad=?, email=?, rol=?, imagen=?
                            WHERE id=?
                        """, (
                            nombre, documento, id_prof, especialidad, email, rol, ruta_imagen,
                            data["id"]
                        ))
                else:
                    cursor.execute("""
                        INSERT INTO usuarios 
                        (nombre, documento, id_profesional, especialidad, email, password, rol, imagen, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        nombre, documento, id_prof, especialidad, email, password, rol, ruta_imagen, 1
                    ))

                conn.commit()
                if editar:

                    # si el usuario editado es el mismo logueado
                    if str(data["documento"]) == str(st.session_state.user[2]):

                        cursor.execute(
                            "SELECT * FROM usuarios WHERE id=?",
                            (data["id"],)
                        )

                        usuario_actualizado = cursor.fetchone()

                        st.session_state.user = usuario_actualizado

                conn.close()

                st.success("Usuario guardado correctamente")

                st.session_state.admin_view = "list"
                st.session_state.usuario_editar = None
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

    # =========================
    # CANCELAR
    # =========================
    with col2:
        if st.button("Cancelar"):
            st.session_state.admin_view = "list"
            st.session_state.usuario_editar = None
            st.rerun()