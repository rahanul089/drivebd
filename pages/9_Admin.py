import streamlit as st
import pandas as pd
from utils.db import get_session, User, Vehicle, Violation, Payment, Appeal, ActivityLog, Setting
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Admin - DriveBD", page_icon="🛡️", layout="wide")
auth.require_role("admin")
user = auth.current_user()

st.title("🛡️ Admin Dashboard")
db = get_session()

tab_users, tab_appeals, tab_logs, tab_settings = st.tabs(
    ["User Management", "Review Appeals", "Activity Logs", "System Settings"]
)

with tab_users:
    st.subheader("All Users")
    users = db.query(User).all()
    df = pd.DataFrame([{
        "ID": u.id, "Name": u.name, "Email": u.email, "Role": u.role, "Phone": u.phone,
        "Vehicles": len(u.vehicles), "Joined": u.created_at.date() if u.created_at else None
    } for u in users])
    role_filter = st.multiselect("Filter by role", ["driver", "owner", "admin"], default=["driver", "owner", "admin"])
    st.dataframe(df[df["Role"].isin(role_filter)], use_container_width=True, hide_index=True)

    st.subheader("Change a User's Role")
    user_choice = st.selectbox("Select user", [f"{u.id} - {u.name} ({u.email})" for u in users])
    uid = int(user_choice.split(" - ")[0])
    new_role = st.selectbox("New Role", ["driver", "owner", "admin"])
    if st.button("Update Role"):
        target = db.query(User).get(uid)
        target.role = new_role
        db.commit()
        log_activity(user["user_id"], f"Changed role of user {uid} to {new_role}")
        st.success("Role updated.")
        st.rerun()

with tab_appeals:
    st.subheader("Pending Appeals")
    pending = db.query(Appeal).filter(Appeal.status == "pending").all()
    if not pending:
        st.info("No pending appeals.")
    else:
        for a in pending:
            with st.container(border=True):
                st.write(f"**Appeal #{a.id}** — Violation #{a.violation_id} ({a.violation.violation_type}, "
                         f"BDT {a.violation.fine_amount:,.0f}) by {a.user.name}")
                st.write(f"Reason: {a.reason}")
                comment = st.text_input("Admin comment", key=f"comment_{a.id}")
                c1, c2 = st.columns(2)
                if c1.button("Approve (waive fine)", key=f"approve_{a.id}"):
                    a.status = "approved"
                    a.admin_comment = comment or "Approved."
                    a.violation.status = "waived"
                    db.commit()
                    log_activity(user["user_id"], f"Approved appeal #{a.id}")
                    st.rerun()
                if c2.button("Reject", key=f"reject_{a.id}"):
                    a.status = "rejected"
                    a.admin_comment = comment or "Rejected."
                    a.violation.status = "unpaid"
                    db.commit()
                    log_activity(user["user_id"], f"Rejected appeal #{a.id}")
                    st.rerun()

with tab_logs:
    st.subheader("Recent System Activity")
    logs = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(200).all()
    df_logs = pd.DataFrame([{
        "Time": l.timestamp, "User ID": l.user_id, "Action": l.action
    } for l in logs])
    st.dataframe(df_logs, use_container_width=True, hide_index=True)

with tab_settings:
    st.subheader("System Settings")
    settings = db.query(Setting).all()
    for s in settings:
        new_val = st.text_input(s.key, value=s.value, key=f"setting_{s.key}")
        if new_val != s.value:
            if st.button(f"Save {s.key}", key=f"save_{s.key}"):
                s.value = new_val
                db.commit()
                st.success(f"Updated {s.key}")
                st.rerun()

db.close()
