import streamlit as st
from utils.db import init_db
from utils import auth
import os
from utils.db import DB_PATH

st.set_page_config(page_title="DriveBD - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

# --- AUTO-SEED BLOCK ---
if not os.path.exists(DB_PATH):
    print("⚠️ Database not found. Generating fresh mock data...")
    from utils.seed import generate
    generate()
    print("✅ Database seeding complete.")
# --------------------------------------------

init_db()

# ---------------------------------------------------------------------------
# MODERN COOL THEME (Matching Deshi Discovery)
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0a0a0f;
    --bg-card: rgba(20, 20, 30, 0.85);
    --primary: #00d4ff;
    --primary-dark: #0099cc;
    --gradient: linear-gradient(135deg, #00d4ff, #7b2ffc);
    --text: #ffffff;
    --text-secondary: #8899aa;
    --border: rgba(0, 212, 255, 0.15);
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.03) 0%, transparent 70%),
                radial-gradient(ellipse at 80% 20%, rgba(123, 47, 252, 0.03) 0%, transparent 70%);
    z-index: 0;
    pointer-events: none;
}

.stApp > div {
    position: relative;
    z-index: 1;
}

/* Sidebar styles */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.98) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* Sidebar toggle button */
button[kind="header"] {
    color: var(--primary) !important;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 4px !important;
}
button[kind="header"]:hover {
    border-color: var(--primary) !important;
    background: rgba(0, 212, 255, 0.05) !important;
}

.main-header {
    font-size: 2.8rem;
    font-weight: 700;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.sub-header {
    color: var(--text-secondary);
    font-size: 1.1rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-top: 0;
}

.divider {
    border: none;
    height: 1px;
    background: var(--gradient);
    margin: 1.5rem 0;
    opacity: 0.3;
}

/* Buttons */
div.stButton > button {
    background: var(--gradient) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2) !important;
}

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 212, 255, 0.05);
}
.metric-label {
    font-size: 0.7rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-value {
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text);
}

/* Form inputs */
.stTextInput > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.stTextInput label {
    color: var(--text-secondary) !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
.stSelectbox label {
    color: var(--text-secondary) !important;
}

/* Alerts and messages */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.stSuccess {
    background: rgba(0, 212, 255, 0.05) !important;
    border-color: var(--primary) !important;
}
.stError {
    background: rgba(255, 50, 50, 0.05) !important;
    border-color: #ff3333 !important;
}
.stInfo {
    background: rgba(123, 47, 252, 0.05) !important;
    border-color: #7b2ffc !important;
}

/* Info text */
.info-text {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.8;
    margin: 1rem 0;
}

/* Footer */
footer {
    opacity: 0.3 !important;
    font-size: 0.7rem !important;
}

#MainMenu {
    visibility: hidden;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-secondary);
    padding: 8px 16px;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--gradient);
    color: white;
    border-color: transparent;
}

/* Badge */
.badge {
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 12px;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.1);
    color: var(--primary);
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MAIN APP LOGIC
# ---------------------------------------------------------------------------
if auth.is_logged_in():
    user = auth.current_user()
    
    # --- SIDEBAR (Visible when logged in) ---
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        st.markdown(f'<p style="color: var(--text-secondary); font-size: 0.8rem;">Welcome back, {user["name"]}</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Actions")
        st.markdown('<p style="color: var(--text-secondary); font-size: 0.8rem;">Navigate to different modules</p>', unsafe_allow_html=True)
        
        # Navigation options (you can expand these with actual page routing)
        st.markdown("**📊 Dashboard**")
        st.markdown("**🚗 Vehicles**")
        st.markdown("**⚠️ Violations**")
        st.markdown("**💳 Payments**")
        st.markdown("**📄 Documents**")
        
        st.markdown("---")
        st.markdown("### 📊 Your Stats")
        st.markdown(f'<div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
        st.markdown(f'<p style="color: var(--text-secondary); font-size: 0.8rem;">Role</p><p style="font-weight: 600; font-size: 1.1rem;">{user["role"].title()}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: var(--text-secondary); font-size: 0.8rem;">Email</p><p style="font-weight: 600; font-size: 1.1rem;">{user["email"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🚪 Log out", use_container_width=True):
            auth.logout()
            st.rerun()
    
    # --- MAIN CONTENT (Logged In) ---
    st.markdown('<div class="main-header">🚗 DriveBD</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    st.success(f"✅ Logged in as **{user['name']}**")
    
    st.markdown("""
    <div class="info-text">
        Welcome to your DriveBD dashboard. From here, you can manage your vehicles,
        track traffic violations, handle payments, and keep your documents up to date.
        Use the sidebar to navigate between different modules.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # --- METRIC CARDS ---
    st.markdown('<div style="font-weight: 600; font-size: 1.2rem; color: var(--text); margin-bottom: 1rem;">📊 At a Glance</div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text" style="margin-top: 0; font-size: 0.85rem;">Your key account information</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Account Type</div>
            <div class="metric-value">{user["role"].title()} <span class="badge">Active</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Email Address</div>
            <div class="metric-value">{user["email"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Member Since</div>
            <div class="metric-value">2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # --- QUICK ACCESS ---
    st.markdown('<div style="font-weight: 600; font-size: 1.2rem; color: var(--text); margin-bottom: 1rem;">🚀 Quick Access</div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text" style="margin-top: 0; font-size: 0.85rem;">Common tasks you might want to perform</p>', unsafe_allow_html=True)
    
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("📋 Register Vehicle", use_container_width=True):
            st.info("Vehicle registration module coming soon!")
    with q2:
        if st.button("📄 Renew License", use_container_width=True):
            st.info("License renewal module coming soon!")
    with q3:
        if st.button("💳 Pay Fines", use_container_width=True):
            st.info("Payment module coming soon!")
    with q4:
        if st.button("📊 View Reports", use_container_width=True):
            st.info("Reports module coming soon!")

else:
    # --- LOGIN / REGISTER PAGE ---
    left, right = st.columns([1, 1])
    
    with left:
        st.markdown('<div class="main-header">🚗 DriveBD</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</div>', unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-text">
            <strong>DriveBD</strong> is a unified portal for vehicle owners and drivers to manage:
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ Vehicle registrations</p>
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ Traffic violations & fines</p>
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ Document management</p>
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ Service history tracking</p>
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ Mock BRTA integration</p>
            <p style="color: var(--text-secondary); margin: 0.3rem 0;">✅ AI-powered violation detection</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-text">
            <strong>🔑 Demo accounts:</strong><br>
            👤 Owner: <code>demo@drivebd.gov.bd</code> / <code>Demo@123</code><br>
            🛡️ Admin: <code>admin@drivebd.gov.bd</code> / <code>Admin@123</code>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem;">', unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔐 Log In", "📝 Create Account"])

        with tab_login:
            st.markdown('<p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">Enter your credentials to access your dashboard</p>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("🔐 Log In", use_container_width=True)
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Please try again.")

        with tab_register:
            st.markdown('<p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;">Create a new account to get started</p>', unsafe_allow_html=True)
            
            with st.form("register_form"):
                name = st.text_input("Full Name")
                email_r = st.text_input("Email Address", key="reg_email")
                phone = st.text_input("Phone Number")
                nid = st.text_input("NID Number")
                role = st.selectbox("Account Type", ["driver", "owner"])
                password_r = st.text_input("Password", type="password", key="reg_pw")
                submitted_r = st.form_submit_button("✨ Create Account", use_container_width=True)
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("❌ Name, email and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); font-size: 0.75rem; opacity: 0.5; padding: 1rem 0;">
    DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data
</div>
""", unsafe_allow_html=True)
