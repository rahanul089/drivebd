import streamlit as st
from utils.db import init_db
from utils import auth

st.set_page_config(page_title="DriveBD - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

init_db()

# ---- Simple CSS theme ----
st.markdown("""
<style>
.main-header {font-size: 2.4rem; font-weight: 700; color: #0B5FFF; margin-bottom:0;}
.sub-header {color: #555; font-size:1.05rem; margin-top:0;}
div.stButton > button {background-color: #0B5FFF; color: white; border-radius: 8px; border:none;}
div.stButton > button:hover {background-color: #0847C4; color: white;}
.metric-card {background:#F0F5FF; padding:16px; border-radius:10px; border:1px solid #D6E4FF;}
</style>
""", unsafe_allow_html=True)

if auth.is_logged_in():
    user = auth.current_user()
    st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal</p>', unsafe_allow_html=True)
    st.success(f"Logged in as **{user['name']}** ({user['role'].title()})")
    st.info("Use the sidebar to navigate to Dashboard, Vehicles, Violations, Payments and other modules.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><b>Role</b><br>' + user["role"].title() + '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><b>Email</b><br>' + user["email"] + '</div>', unsafe_allow_html=True)
    with col3:
        if st.button("Log out"):
            auth.logout()
            st.rerun()
else:
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</p>', unsafe_allow_html=True)
        st.write("""
        DriveBD is a unified portal for vehicle owners and drivers to manage registrations,
        traffic violations, fines, documents, service history and more — with a mock BRTA
        integration and a demo AI violation detector.
        """)
        st.markdown("""
        **Demo accounts (pre-seeded):**
        - 👤 Owner demo: `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ Admin demo: `admin@drivebd.gov.bd` / `Admin@123`
        """)

    with right:
        tab_login, tab_register = st.tabs(["Log In", "Create Account"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In")
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        with tab_register:
            with st.form("register_form"):
                name = st.text_input("Full name")
                email_r = st.text_input("Email", key="reg_email")
                phone = st.text_input("Phone number")
                nid = st.text_input("NID number")
                role = st.selectbox("Account type", ["driver", "owner"])
                password_r = st.text_input("Password", type="password", key="reg_pw")
                submitted_r = st.form_submit_button("Create Account")
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("Name, email and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
