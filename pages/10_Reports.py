import streamlit as st
import pandas as pd
from utils.db import get_session, Vehicle, Violation, Payment
from utils import auth
from utils.pdf_utils import generate_report_pdf

st.set_page_config(page_title="Reports - DriveBD", page_icon="🧾", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("🧾 Reports")
db = get_session()

report_type = st.selectbox("Select report", ["Violations Report", "Payments Report", "Vehicles Report"])

if user["role"] == "admin":
    vehicles = db.query(Vehicle).all()
else:
    vehicles = db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()
vehicle_ids = [v.id for v in vehicles]

if report_type == "Violations Report":
    q = db.query(Violation)
    if user["role"] != "admin":
        q = q.filter(Violation.vehicle_id.in_(vehicle_ids)) if vehicle_ids else q.filter(Violation.id == -1)
    records = q.all()
    df = pd.DataFrame([{
        "ID": v.id, "Vehicle": v.vehicle.reg_number, "Type": v.violation_type, "Date": str(v.date),
        "Location": v.location, "Fine (BDT)": v.fine_amount, "Status": v.status
    } for v in records])

elif report_type == "Payments Report":
    q = db.query(Payment)
    if user["role"] != "admin":
        q = q.filter(Payment.user_id == user["user_id"])
    records = q.all()
    df = pd.DataFrame([{
        "ID": p.id, "Amount (BDT)": p.amount, "Method": p.method, "Date": str(p.date),
        "Status": p.status, "Reference": p.reference_no
    } for p in records])

else:  # Vehicles report
    df = pd.DataFrame([{
        "ID": v.id, "Reg. Number": v.reg_number, "Make": v.make, "Model": v.model,
        "Year": v.year, "Type": v.vehicle_type, "Status": v.status
    } for v in vehicles])

st.dataframe(df, use_container_width=True, hide_index=True)

if not df.empty:
    c1, c2 = st.columns(2)
    csv_data = df.to_csv(index=False).encode("utf-8")
    c1.download_button("⬇️ Download as CSV", data=csv_data, file_name=f"{report_type.replace(' ', '_').lower()}.csv",
                        mime="text/csv")

    pdf_bytes = generate_report_pdf(
        title=report_type, subtitle=f"Generated for {user['name']} ({user['role'].title()})", df=df
    )
    c2.download_button("⬇️ Download as PDF", data=pdf_bytes, file_name=f"{report_type.replace(' ', '_').lower()}.pdf",
                        mime="application/pdf")
else:
    st.info("No data available for this report.")

db.close()
