import streamlit as st
import pandas as pd
import datetime as dt
from utils.db import get_session, Vehicle, Violation
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Violations - DriveBD", page_icon="🚨", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("🚨 Traffic Violations")

db = get_session()

if user["role"] == "admin":
    tab_view, tab_issue, tab_map = st.tabs(["All Violations", "Issue New Violation", "Violation Map"])
else:
    vehicle_ids = [v.id for v in db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()]
    tab_view, tab_map = st.tabs(["My Violations", "Violation Map"])

with tab_view:
    query = db.query(Violation)
    if user["role"] != "admin":
        query = query.filter(Violation.vehicle_id.in_(vehicle_ids)) if vehicle_ids else query.filter(Violation.id == -1)
    violations = query.all()

    status_filter = st.multiselect("Filter by status", ["unpaid", "paid", "appealed", "waived"],
                                    default=["unpaid", "paid", "appealed", "waived"])
    violations = [v for v in violations if v.status in status_filter]

    if not violations:
        st.info("No violations found.")
    else:
        df = pd.DataFrame([{
            "ID": v.id, "Vehicle": v.vehicle.reg_number, "Type": v.violation_type, "Date": v.date,
            "Location": v.location, "Fine (BDT)": v.fine_amount, "Status": v.status,
            "Officer": v.officer_name
        } for v in sorted(violations, key=lambda x: x.date, reverse=True)])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(violations)} violations | Unpaid fines: BDT {sum(v.fine_amount for v in violations if v.status=='unpaid'):,.0f}")

if user["role"] == "admin":
    with tab_issue:
        with st.form("issue_violation"):
            all_vehicles = db.query(Vehicle).all()
            vehicle_choice = st.selectbox("Vehicle", [f"{v.id} - {v.reg_number}" for v in all_vehicles])
            violation_type = st.selectbox("Violation Type", [
                "No Helmet", "Signal Breaking", "Over Speeding", "No Valid License", "Illegal Parking",
                "Fitness Certificate Expired", "Route Permit Violation", "Overloading",
                "Using Mobile While Driving", "Fake Registration Plate", "Tax Token Expired", "No Insurance"
            ])
            fine_amount = st.number_input("Fine Amount (BDT)", min_value=0, value=1000, step=100)
            location = st.text_input("Location")
            officer_name = st.text_input("Officer Name", value=user["name"])
            date = st.date_input("Date", value=dt.date.today())
            submitted = st.form_submit_button("Issue Violation")
            if submitted:
                vid = int(vehicle_choice.split(" - ")[0])
                viol = Violation(
                    vehicle_id=vid, violation_type=violation_type, date=date, location=location,
                    fine_amount=fine_amount, status="unpaid", officer_name=officer_name
                )
                db.add(viol)
                db.commit()
                log_activity(user["user_id"], f"Issued violation on vehicle ID {vid}")
                st.success("Violation issued successfully.")
                st.rerun()

with tab_map:
    all_violations_for_map = db.query(Violation).filter(Violation.latitude.isnot(None)).all()
    if user["role"] != "admin":
        all_violations_for_map = [v for v in all_violations_for_map if v.vehicle_id in vehicle_ids]
    if all_violations_for_map:
        map_df = pd.DataFrame([{"lat": v.latitude, "lon": v.longitude} for v in all_violations_for_map])
        st.map(map_df, size=20)
        st.caption("Approximate locations of recorded traffic violations across Bangladesh.")
    else:
        st.info("No geolocated violations to display.")

db.close()
