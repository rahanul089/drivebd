import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_session, Vehicle, Violation, Payment
from utils import auth

st.set_page_config(page_title="Analytics - DriveBD", page_icon="📈", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("📈 Analytics")
db = get_session()

if user["role"] == "admin":
    violations = db.query(Violation).all()
    payments = db.query(Payment).all()
else:
    vehicle_ids = [v.id for v in db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()]
    violations = db.query(Violation).filter(Violation.vehicle_id.in_(vehicle_ids)).all() if vehicle_ids else []
    payments = db.query(Payment).filter(Payment.user_id == user["user_id"]).all()

if not violations:
    st.info("Not enough data to generate analytics yet.")
else:
    df_v = pd.DataFrame([{
        "type": v.violation_type, "status": v.status, "fine": v.fine_amount,
        "month": v.date.strftime("%Y-%m")
    } for v in violations])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Violations by Type")
        type_counts = df_v["type"].value_counts().reset_index()
        type_counts.columns = ["Violation Type", "Count"]
        fig1 = px.bar(type_counts, x="Violation Type", y="Count", color="Count",
                      color_continuous_scale="Blues")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Violation Status Breakdown")
        status_counts = df_v["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig2 = px.pie(status_counts, names="Status", values="Count", hole=0.4,
                      color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Violations Over Time")
    monthly = df_v.groupby("month").size().reset_index(name="Violations")
    fig3 = px.line(monthly, x="month", y="Violations", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Fines Collected vs Outstanding")
    collected = sum(v.fine_amount for v in violations if v.status == "paid")
    outstanding = sum(v.fine_amount for v in violations if v.status == "unpaid")
    waived = sum(v.fine_amount for v in violations if v.status == "waived")
    fig4 = px.bar(x=["Collected", "Outstanding", "Waived"], y=[collected, outstanding, waived],
                  labels={"x": "Category", "y": "BDT"}, color=["Collected", "Outstanding", "Waived"],
                  color_discrete_map={"Collected": "#0B5FFF", "Outstanding": "#FF6B6B", "Waived": "#999"})
    st.plotly_chart(fig4, use_container_width=True)

db.close()
