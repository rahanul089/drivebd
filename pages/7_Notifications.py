import streamlit as st
from utils.db import get_session, Notification
from utils import auth

st.set_page_config(page_title="Notifications - DriveBD", page_icon="🔔", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("🔔 Notifications")
db = get_session()

notifications = db.query(Notification).filter(
    Notification.user_id == user["user_id"]
).order_by(Notification.date.desc()).all()

if not notifications:
    st.info("You have no notifications.")
else:
    unread_count = sum(1 for n in notifications if not n.is_read)
    st.write(f"You have **{unread_count}** unread notification(s).")

    if st.button("Mark all as read"):
        for n in notifications:
            n.is_read = True
        db.commit()
        st.rerun()

    icon_map = {"info": "ℹ️", "warning": "⚠️", "alert": "🚨"}
    for n in notifications:
        icon = icon_map.get(n.category, "ℹ️")
        read_tag = "" if n.is_read else " **(new)**"
        with st.container(border=True):
            st.write(f"{icon} {n.message}{read_tag}")
            st.caption(str(n.date))

db.close()
