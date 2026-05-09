import sys
import base64
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db.init_db import init_db
from db.crear_admin import crear_admin

init_db()
crear_admin()   

import streamlit as st

from app.login import login
from app.dashboard_admin import admin_panel
from app.dashboard_medico import medico_panel
from app.admin_reportes import admin_reportes
from app.medico_reportes import medico_reportes
from app.perfil import perfil_usuario

st.set_page_config(
    page_title="SIMDI",
    page_icon="🩺",
    layout="wide"
)

# =========================
# PALETA DE COLORES
# =========================

COLOR_FONDO = "#D9D4EB"
COLOR_HEADER = "#FFFFFF"
COLOR_FOOTER = "#CCCCCC"

COLOR_TEXTO = "#2B2B2B"
COLOR_SUBTEXTO = "#666666"

COLOR_BORDE = "#C5BEDB"

COLOR_BOTON = "#9A91B7"
COLOR_BOTON_HOVER = "#7A68B2"

COLOR_CARD = "#FFFFFF"

# =========================
# HEADER
# =========================

def mostrar_header(user=None):

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    logo_path = os.path.join(BASE_DIR, "ALOGOSIMDI.png")

    logo_base64 = ""

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img:
            logo_base64 = base64.b64encode(img.read()).decode()

    # =========================
    # FOTO PERFIL
    # =========================

    foto_html = ""

    if user and len(user) > 8 and user[8] and os.path.exists(user[8]):

        with open(user[8], "rb") as img:
            user_img = base64.b64encode(img.read()).decode()

        foto_html = f"""
        <img src="data:image/png;base64,{user_img}"
        style="
            width:90px;
            height:90px;
            border-radius:50%;
            object-fit:cover;
            border:3px solid #4CAF50;
        ">
        """

    else:

        foto_html = """
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        style="
            width:90px;
            height:90px;
            border-radius:50%;
            object-fit:cover;
            border:3px solid #4CAF50;
        ">
        """

    # =========================
    # CSS
    # =========================

    st.html(f"""
    <style>

    /* ===== FONDO GENERAL ===== */

    .stApp {{
        background-color:{COLOR_FONDO};
    }}

    /* ===== HEADER ===== */

    .header-container{{
        background:{COLOR_HEADER};
        border:1px solid {COLOR_BORDE};
        border-radius:20px;
        padding:20px 35px;
        margin-bottom:25px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
    }}

    .header-flex{{
        display:flex;
        justify-content:space-between;
        align-items:center;
    }}

    .logo-section{{
        display:flex;
        align-items:center;
        gap:30px;
    }}

    .logo-img{{
        width:170px;
    }}

    .title-section h1{{
        margin:0;
        color:{COLOR_TEXTO};
        font-size:56px;
        font-weight:700;
    }}

    .title-section p{{
        margin-top:5px;
        color:{COLOR_SUBTEXTO};
        font-size:20px;
    }}

    .user-section{{
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        text-align:center;
    }}

    .user-name{{
        margin-top:10px;
        color:{COLOR_TEXTO};
        font-weight:600;
        font-size:18px;
    }}

    /* ===== BOTONES ===== */

    .stButton > button{{
        background:{COLOR_BOTON};
        color:white;
        border:none;
        border-radius:12px;
        padding:10px 18px;
        font-weight:600;
        transition:0.3s;
    }}

    .stButton > button:hover{{
        background:{COLOR_BOTON_HOVER};
        transform:translateY(-2px);
    }}

    /* ===== CARDS / CONTAINERS ===== */

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background:{COLOR_CARD};
        border:1px solid {COLOR_BORDE};
        border-radius:18px;
        padding:10px;
        box-shadow:0 2px 10px rgba(0,0,0,0.05);
    }}

    /* ===== FOOTER ===== */

    .footer{{
        background:{COLOR_FOOTER};
        margin-top:60px;
        padding:25px;
        border-radius:18px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        color:{COLOR_TEXTO};
        font-size:14px;
    }}

    .footer-left{{
        text-align:left;
        line-height:1.8;
    }}

    .footer-right{{
        text-align:right;
        line-height:1.8;
    }}

    /* ===== TITULOS STREAMLIT ===== */

    h1, h2, h3, h4 {{
        color:{COLOR_TEXTO} !important;
    }}

    p, span, label, div {{
        color:{COLOR_TEXTO};
    }}

    </style>
    """)

    

    # =========================
    # HEADER HTML
    # =========================

    st.html(f"""
    <div class="header-container">

        <div class="header-flex">

            <div class="logo-section">

                <img src="data:image/png;base64,{logo_base64}" class="logo-img">

                <div class="title-section">
                    <h1>SIMDI-IA</h1>
                    <p>Sistema Inteligente de Diagnóstico Médico</p>
                </div>

            </div>

            <div class="user-section">

                {foto_html}

                <div class="user-name">
                    {user[1]}
                </div>



            </div>

        </div>

    </div>
    """)

    # =========================
    # MENÚ SUPERIOR
    # =========================

    rol = user[7]

    if rol == "admin":

        c1, c2, c3, c4, c5, c6 = st.columns([2,2,2,2,1,2])

        with c2:
            if st.button("👥 Usuarios", use_container_width=True):
                st.session_state.view = "usuarios"
                st.rerun()

        with c3:
            if st.button("📄 Reportes", use_container_width=True):
                st.session_state.view = "reportes_admin"
                st.rerun()

        with c4:
            if st.button("⏻", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    else:

        c1, c2, c3, c4, c5, c6, c7 = st.columns([1,2,2,2,1,1,1])

        with c2:
            if st.button("🩺 Nueva consulta", use_container_width=True):
                st.session_state.view = "consulta"
                st.rerun()

        with c3:
            if st.button("📄 Mis reportes", use_container_width=True):
                st.session_state.view = "reportes_medico"
                st.rerun()

        with c4:
            if st.button("⚙️ Mi perfil", use_container_width=True):
                st.session_state.view = "perfil"
                st.rerun()

        with c5:
            if st.button("⏻", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    st.divider()


# =========================
# ESTADO GLOBAL
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "view" not in st.session_state:
    st.session_state.view = "home"

# =========================
# LOGIN
# =========================

if not st.session_state.logged_in:

    login()

else:

    user = st.session_state.user
    rol = user[7]

    if "ir_a_consulta" in st.session_state and st.session_state.ir_a_consulta:
        st.session_state.view = "consulta"
        st.session_state.ir_a_consulta = False
        st.rerun()

    # HEADER
    mostrar_header(user)

    # =========================
    # HOME
    # =========================

    if st.session_state.view == "home":

        st.title("Panel principal")

        if rol == "admin":

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):

                    st.markdown("## 👥 Gestión de Usuarios")
                    st.write("Crear, editar, activar y desactivar usuarios.")

                    if st.button("Ir a usuarios"):
                        st.session_state.view = "usuarios"
                        st.rerun()

            with col2:
                with st.container(border=True):

                    st.markdown("## 📄 Reportes")
                    st.write("Visualización y descarga de reportes clínicos.")

                    if st.button("Ir a reportes"):
                        st.session_state.view = "reportes_admin"
                        st.rerun()

        else:

            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):

                    st.markdown("## 🩺 Nueva Consulta")
                    st.write("Registrar síntomas y generar diagnósticos.")

                    if st.button("Ir a consulta"):
                        st.session_state.view = "consulta"
                        st.rerun()

            with col2:
                with st.container(border=True):

                    st.markdown("## 📄 Mis Reportes")
                    st.write("Consultar historial clínico.")

                    if st.button("Ver reportes"):
                        st.session_state.view = "reportes_medico"
                        st.rerun()

            with col3:
                with st.container(border=True):

                    st.markdown("## ⚙️ Mi Perfil")
                    st.write("Configuración e información del usuario.")

                    if st.button("Abrir perfil"):
                        st.session_state.view = "perfil"
                        st.rerun()

    # =========================
    # VISTAS
    # =========================

    else:

        if st.button("⬅️ Volver al inicio"):
            st.session_state.view = "home"
            st.rerun()

        if rol == "admin":

            if st.session_state.view == "usuarios":
                admin_panel(user)

            elif st.session_state.view == "reportes_admin":
                admin_reportes()

        else:

            if st.session_state.view == "consulta":
                medico_panel(user)

            elif st.session_state.view == "reportes_medico":
                medico_reportes(user)

            elif st.session_state.view == "perfil":
                perfil_usuario(user)

    # =========================
    # FOOTER
    # =========================

    st.html("""
    <div class="footer">

        <div class="footer-left">
            📞 3105679305 - 3118871786<br>
            ✉️ byulianmaldonado@uts.edu.co<br>
            ✉️ kmacareo@uts.edu.co
        </div>

        <div class="footer-right">
            <strong>SIMDI-IA</strong><br>
            Sistema Inteligente de Diagnóstico Médico creado<br>
            para el apoyo en la toma de decisiones clínicas.
        </div>

    </div>
    """)