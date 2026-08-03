import streamlit as st
from utils.db import init_db
from utils import auth
import pandas as pd
import datetime
import time
import random

# --- Page Config ---
st.set_page_config(page_title="DriveBD - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

# --- DB Setup ---
init_db()

# --- Auto-Seed Block (Fixed) ---
import os
from utils.db import DB_PATH, get_session, User

db = get_session()
admin_exists = db.query(User).filter(User.email == "admin@drivebd.gov.bd").first()
db.close()

if not admin_exists:
    print("⚠️ Admin user not found. Generating mock data...")
    from utils.seed import generate
    generate()
    print("✅ Database seeding complete.")
else:
    print("✅ Database already seeded.")

# ---------------------------------------------------------------------------
# CUSTOM CSS (Kept your original blue theme + minor cleanups)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.main-header {font-size: 2.6rem; font-weight: 800; color: #0B5FFF; margin-bottom: 0; letter-spacing: -0.5px;}
.sub-header {color: #666; font-size: 1.1rem; margin-top: 0; font-weight: 400;}
div.stButton > button {background-color: #0B5FFF; color: white; border-radius: 8px; border: none; font-weight: 600; transition: 0.2s;}
div.stButton > button:hover {background-color: #0847C4; color: white; transform: scale(1.02);}
.metric-card {background: #F0F5FF; padding: 18px; border-radius: 12px; border: 1px solid #D6E4FF; text-align: center;}
.section-header {font-size: 1.5rem; font-weight: 600; color: #1A2B4C; margin-top: 1.5rem; margin-bottom: 0.5rem;}
.info-paragraph {background: #F8FAFC; padding: 15px; border-radius: 10px; border-left: 5px solid #0B5FFF; color: #333; margin-bottom: 15px;}
.notification-badge {background: #FF4B4B; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; margin-left: 5px;}
.action-card {background: white; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); text-align: center; transition: 0.2s;}
.action-card:hover {border-color: #0B5FFF; box-shadow: 0 4px 12px rgba(11, 95, 255, 0.1);}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MOCK DATA GENERATORS (For new functionalities)
# ---------------------------------------------------------------------------
def get_mock_notifications(user_id):
    return [
        {"id": 1, "msg": "Your vehicle renewal (ABC-123) is due in 7 days.", "date": "2026-08-10", "read": False},
        {"id": 2, "msg": "New traffic violation detected on XYZ-789.", "date": "2026-08-05", "read": False},
        {"id": 3, "msg": "Insurance policy for your SUV has been updated.", "date": "2026-08-03", "read": True},
    ]

def get_quick_actions():
    return ["📄 Renew License", "🚗 Add New Vehicle", "💳 Pay Fines", "📅 Schedule Inspection", "📞 Contact Support"]

# ---------------------------------------------------------------------------
# AUTHENTICATION LOGIC
# ---------------------------------------------------------------------------
if auth.is_logged_in():
    user = auth.current_user()
    
    # --- HERO SECTION ---
    st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</p>', unsafe_allow_html=True)
    
    # --- WELCOME BANNER WITH NOTIFICATIONS ---
    cols_top = st.columns([2.5, 1])
    with cols_top[0]:
        notifications = get_mock_notifications(user['id'])
        unread_count = sum(1 for n in notifications if not n['read'])
        badge_html = f'<span class="notification-badge">{unread_count}</span>' if unread_count > 0 else ""
        st.success(f"✅ Welcome back, **{user['name']}** ({user['role'].title()}) {badge_html}")
        st.caption(f"Last login: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
    with cols_top[1]:
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()

    st.markdown("---")

    # --- INTRODUCTORY PARAGRAPH ---
    st.markdown("""
    <div class="info-paragraph">
        <b>📋 Your Digital Hub</b><br>
        Welcome to your personalized dashboard. Here, you can manage all your vehicle-related tasks in one place. 
        From tracking traffic violations and paying fines to renewing documents and scheduling inspections, 
        DriveBD streamlines your experience. Use the sidebar to dive deep into specific modules.
    </div>
    """, unsafe_allow_html=True)

    # --- QUICK STATISTICS ---
    st.markdown('<div class="section-header">📊 At a Glance</div>', unsafe_allow_html=True)
    
    # Mock stats for demonstration
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><b style="font-size:1.8rem; color:#0B5FFF;">2</b><br>Registered Vehicles</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><b style="font-size:1.8rem; color:#FF4B4B;">1</b><br>Pending Violations</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><b style="font-size:1.8rem; color:#28A745;">4</b><br>Active Documents</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><b style="font-size:1.8rem; color:#FFC107;">2</b><br>Upcoming Renewals</div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- QUICK ACTIONS (New Functionality) ---
    st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#666; margin-top:-5px;">Perform common tasks instantly without navigating away.</p>', unsafe_allow_html=True)

    qa_cols = st.columns(5)
    actions = get_quick_actions()
    for i, action in enumerate(actions):
        with qa_cols[i]:
            st.markdown(f'<div class="action-card">{action}</div>', unsafe_allow_html=True)
            if st.button(f"Go", key=f"qa_{i}"):
                st.toast(f"🚀 Navigating to: {action}", icon="ℹ️")

    st.markdown("---")

    # --- NOTIFICATION CENTER (New Functionality) ---
    st.markdown('<div class="section-header">🔔 Notification Center</div>', unsafe_allow_html=True)
    
    for n in notifications:
        col_n1, col_n2 = st.columns([4, 1])
        with col_n1:
            if n['read']:
                st.markdown(f"<span style='color:#888;'>✔️ {n['msg']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='font-weight:600;'>🔴 {n['msg']}</span>", unsafe_allow_html=True)
            st.caption(f"📅 {n['date']}")
        with col_n2:
            if not n['read']:
                if st.button("Mark Read", key=f"read_{n['id']}"):
                    st.success("Marked as read!")
                    st.rerun()
    st.markdown("---")

    # --- AI VIOLATION DETECTOR DEMO (New Functionality) ---
    st.markdown('<div class="section-header">🤖 AI Violation Detector (Demo)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-paragraph" style="border-left-color: #FFC107;">
        <b>Simulated AI Intelligence</b><br>
        Our integrated AI agent scans real-time traffic feeds to detect potential violations. 
        Click the button below to simulate an AI scan for your registered vehicles.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛰️ Run AI Scan", type="primary"):
        with st.spinner("AI Agent is analyzing traffic feeds..."):
            time.sleep(2)  # Simulate processing
            violation_types = ["Speeding", "Running Red Light", "Illegal Parking", "No Seatbelt", "Expired Registration"]
            detected = random.choice(violation_types)
            vehicle = random.choice(["ABC-123", "XYZ-789"])
            fine = random.randint(500, 5000)
            
            st.success(f"🚨 **Violation Detected!**")
            st.warning(f"Vehicle **{vehicle}** violated: **{detected}**")
            st.info(f"Estimated Fine: **{fine} BDT**")
            
            if st.button("💸 Pay Fine Now"):
                st.balloons()
                st.success("Fine paid successfully! Receipt sent to your email.")

    st.markdown("---")

    # --- DOCUMENT MANAGER (New Functionality) ---
    st.markdown('<div class="section-header">📁 Document Manager</div>', unsafe_allow_html=True)
    st.markdown("Keep track of your essential driving documents.")
    
    docs = [
        {"Document": "Driving License", "Status": "✅ Active", "Expiry": "2028-05-12"},
        {"Document": "Vehicle Registration (ABC-123)", "Status": "✅ Active", "Expiry": "2027-01-20"},
        {"Document": "Insurance Policy", "Status": "⚠️ Expiring Soon", "Expiry": "2026-09-15"},
        {"Document": "Fitness Certificate", "Status": "✅ Active", "Expiry": "2026-12-01"},
    ]
    
    df_docs = pd.DataFrame(docs)
    st.dataframe(df_docs, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- DASHBOARD FOOTER INFO ---
    st.caption("💡 Tip: Use the sidebar on the left to access detailed modules like Vehicles, Violations, Payments, and Settings.")

else:
    # ---------------------------------------------------------------------------
    # LANDING PAGE (ENHANCED)
    # ---------------------------------------------------------------------------
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #F8FAFC; padding: 20px; border-radius: 12px; margin-top: 10px;">
            <b>🌟 Welcome to the Future of Vehicle Management</b><br><br>
            DriveBD is a unified, digital-first portal designed to simplify life for vehicle owners, 
            drivers, and transport authorities in Bangladesh. Whether you are managing a single car 
            or a fleet, our platform provides everything you need.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### 🚀 Key Features:
        - **📝 Digital Registration:** Manage all vehicle papers in one cloud-based hub.
        - **🚦 AI Violation Tracker:** Simulated AI detection to keep you updated on traffic rules.
        - **💳 Smart Fine Payments:** Instant fine processing with digital receipts.
        - **📅 Service Reminders:** Automated alerts for renewals, insurance, and inspections.
        - **📊 Real-time Dashboard:** Get a bird's-eye view of your driving history.
        """)

        st.markdown("""
        ### 🔑 Demo Accounts:
        - 👤 **Owner Demo:** `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ **Admin Demo:** `admin@drivebd.gov.bd` / `Admin@123`
        """)

    with right:
        st.markdown('<div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔐 Log In", "📝 Create Account"])

        with tab_login:
            st.markdown("Welcome back! Please login to your dashboard.")
            with st.form("login_form"):
                email = st.text_input("📧 Email")
                password = st.text_input("🔑 Password", type="password")
                submitted = st.form_submit_button("Log In", use_container_width=True)
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Please try again.")

        with tab_register:
            st.markdown("Join DriveBD today. It's free and takes 2 minutes.")
            with st.form("register_form"):
                name = st.text_input("👤 Full name")
                email_r = st.text_input("📧 Email", key="reg_email")
                phone = st.text_input("📞 Phone number")
                nid = st.text_input("🆔 NID number")
                role = st.selectbox("👮 Account type", ["driver", "owner"])
                password_r = st.text_input("🔑 Password", type="password", key="reg_pw")
                submitted_r = st.form_submit_button("Create Account", use_container_width=True)
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("❌ Name, email, and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(msg)
                            st.balloons()
                        else:
                            st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("📌 DriveBD Capstone Project · Built with Streamlit · Mock Data for Demonstration · Not affiliated with BRTA")
