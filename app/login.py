import streamlit as st
from db.database import get_connection

def login():
    st.title("Login")

    documento = st.text_input("Documento")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        conn = get_connection()
        cursor = conn.cursor()

        # 🔍 Buscar usuario solo por documento
        cursor.execute(
            "SELECT * FROM usuarios WHERE documento=?",
            (documento,)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            # 🔒 VALIDAR ESTADO (columna 9)
            estado = user[9]

            if estado == 0:
                st.error("Usuario desactivado. Contacte al administrador.")
                return

            # 🔑 VALIDAR PASSWORD
            if user[6] == password:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        else:
            st.error("Usuario no encontrado")