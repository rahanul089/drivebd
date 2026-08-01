"""
DriveBD - Authentication & Role-Based Access Control
Simple bcrypt-based auth using Streamlit session_state (no external auth service needed).
"""
import bcrypt
import streamlit as st
from utils.db import get_session, User, ActivityLog


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def log_activity(user_id, action):
    db = get_session()
    try:
        db.add(ActivityLog(user_id=user_id, action=action))
        db.commit()
    finally:
        db.close()


def login(email: str, password: str) -> bool:
    db = get_session()
    try:
        user = db.query(User).filter(User.email == email.strip().lower()).first()
        if user and verify_password(password, user.password_hash):
            st.session_state["auth"] = {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
            log_activity(user.id, "Logged in")
            return True
        return False
    finally:
        db.close()


def logout():
    if "auth" in st.session_state:
        log_activity(st.session_state["auth"]["user_id"], "Logged out")
    st.session_state.pop("auth", None)


def is_logged_in() -> bool:
    return "auth" in st.session_state


def current_user():
    return st.session_state.get("auth")


def require_login():
    """Call at the top of every protected page. Stops rendering if not logged in."""
    if not is_logged_in():
        st.warning("Please log in from the Home page to access this section.")
        st.stop()


def require_role(*allowed_roles):
    """Call at the top of a page to restrict it to specific roles."""
    require_login()
    role = current_user()["role"]
    if role not in allowed_roles:
        st.error(f"Access denied. This page is restricted to: {', '.join(allowed_roles)}.")
        st.stop()


def register_user(name, email, password, role, nid="", phone="", license_no=""):
    db = get_session()
    try:
        existing = db.query(User).filter(User.email == email.strip().lower()).first()
        if existing:
            return False, "An account with this email already exists."
        user = User(
            name=name,
            email=email.strip().lower(),
            password_hash=hash_password(password),
            role=role,
            nid=nid,
            phone=phone,
            license_no=license_no,
        )
        db.add(user)
        db.commit()
        return True, "Account created successfully. Please log in."
    finally:
        db.close()
