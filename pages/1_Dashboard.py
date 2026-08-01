import streamlit as st
import pandas as pd
from utils.db import get_session, Vehicle, Violation, Payment, Notification, Document
from utils import auth

st.set_page_config(page_title="Dashboard - DriveBD", page_icon="📊", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("📊 Dashboard")
st.caption(f"Welcome back, {user['name']}")

db = get_session()

if user["role"] == "admin":
    vehicles = db.query(Vehicle).all()
    violations = db.query(Violation).all()
    payments = db.query(Payment).all()
else:
    vehicles = db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()
    vehicle_ids = [v.id for v in vehicles]
    violations = db.query(Violation).filter(Violation.vehicle_id.in_(vehicle_ids)).all() if vehicle_ids else []
    payments = db.query(Payment).filter(Payment.user_id == user["user_id"]).all()

unpaid_fines = sum(v.fine_amount for v in violations if v.status == "unpaid")
total_paid = sum(p.amount for p in payments if p.status == "completed")
notifications = db.query(Notification).filter(
    Notification.user_id == user["user_id"], Notification.is_read == False
).count()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Vehicles" if user["role"] != "admin" else "Total Vehicles", len(vehicles))
c2.metric("Violations", len(violations))
c3.metric("Unpaid Fines (BDT)", f"{unpaid_fines:,.0f}")
c4.metric("Unread Notifications", notifications)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent Violations")
    if violations:
        df = pd.DataFrame([{
            "Date": v.date, "Type": v.violation_type, "Vehicle": v.vehicle.reg_number,
            "Fine (BDT)": v.fine_amount, "Status": v.status
        } for v in sorted(violations, key=lambda x: x.date, reverse=True)[:8]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No violations on record.")

with col2:
    st.subheader("Recent Payments")
    if payments:
        df = pd.DataFrame([{
            "Date": p.date, "Amount (BDT)": p.amount, "Method": p.method, "Status": p.status,
            "Reference": p.reference_no
        } for p in sorted(payments, key=lambda x: x.date, reverse=True)[:8]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No payments on record.")

db.close()

st.divider()
st.subheader("Quick Links")
qc1, qc2, qc3, qc4 = st.columns(4)
qc1.page_link("pages/2_Vehicles.py", label="🚙 Manage Vehicles")
qc2.page_link("pages/3_Violations.py", label="🚨 View Violations")
qc3.page_link("pages/4_Payments.py", label="💳 Make Payment")
qc4.page_link("pages/5_Documents.py", label="📁 Document Vault")
