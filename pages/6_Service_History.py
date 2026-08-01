import streamlit as st
import pandas as pd
import datetime as dt
from utils.db import get_session, Vehicle, ServiceHistory
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Service History - DriveBD", page_icon="🔧", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("🔧 Vehicle Service History")
db = get_session()

my_vehicles = db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()

if not my_vehicles:
    st.info("Register a vehicle first to log service history.")
else:
    tab_view, tab_add = st.tabs(["Service Records", "Log New Service"])

    with tab_view:
        vehicle_choice = st.selectbox("Select vehicle", [f"{v.id} - {v.reg_number}" for v in my_vehicles])
        vid = int(vehicle_choice.split(" - ")[0])
        records = db.query(ServiceHistory).filter(ServiceHistory.vehicle_id == vid).order_by(
            ServiceHistory.service_date.desc()).all()
        if not records:
            st.info("No service records for this vehicle yet.")
        else:
            df = pd.DataFrame([{
                "Date": r.service_date, "Type": r.service_type, "Workshop": r.workshop,
                "Cost (BDT)": r.cost, "Mileage (km)": r.mileage_km, "Notes": r.notes
            } for r in records])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.metric("Total spent on this vehicle (BDT)", f"{sum(r.cost for r in records):,.0f}")

    with tab_add:
        with st.form("add_service"):
            vehicle_choice2 = st.selectbox("Vehicle", [f"{v.id} - {v.reg_number}" for v in my_vehicles], key="svc_vehicle")
            service_type = st.selectbox("Service Type", [
                "Engine Oil Change", "Brake Service", "Tire Replacement", "General Servicing",
                "AC Repair", "Battery Replacement", "Full Inspection"
            ])
            service_date = st.date_input("Service Date", value=dt.date.today())
            cost = st.number_input("Cost (BDT)", min_value=0, value=1000, step=100)
            workshop = st.text_input("Workshop Name")
            mileage = st.number_input("Mileage at service (km)", min_value=0, value=10000, step=100)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Service Record")
            if submitted:
                vid2 = int(vehicle_choice2.split(" - ")[0])
                r = ServiceHistory(
                    vehicle_id=vid2, service_date=service_date, service_type=service_type,
                    cost=cost, workshop=workshop, mileage_km=mileage, notes=notes
                )
                db.add(r)
                db.commit()
                log_activity(user["user_id"], f"Logged service record for vehicle ID {vid2}")
                st.success("Service record added.")
                st.rerun()

db.close()
