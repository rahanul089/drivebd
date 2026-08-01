import streamlit as st
import pandas as pd
import datetime as dt
from utils.db import get_session, Vehicle
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Vehicles - DriveBD", page_icon="🚙", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("🚙 Vehicle Management")

db = get_session()

tab_list, tab_add = st.tabs(["My Vehicles" if user["role"] != "admin" else "All Vehicles", "Register New Vehicle"])

with tab_list:
    query = db.query(Vehicle)
    if user["role"] != "admin":
        query = query.filter(Vehicle.owner_id == user["user_id"])
    vehicles = query.all()

    if not vehicles:
        st.info("No vehicles registered yet. Use the 'Register New Vehicle' tab to add one.")
    else:
        search = st.text_input("🔍 Search by registration number, make or model")
        rows = []
        for v in vehicles:
            rows.append({
                "ID": v.id, "Reg. Number": v.reg_number, "Owner": v.owner.name if user["role"] == "admin" else None,
                "Make": v.make, "Model": v.model, "Year": v.year, "Type": v.vehicle_type, "Status": v.status,
                "Registered On": v.registered_on
            })
        df = pd.DataFrame(rows)
        if user["role"] != "admin":
            df = df.drop(columns=["Owner"])
        if search:
            mask = df.apply(lambda r: search.lower() in str(r).lower(), axis=1)
            df = df[mask]
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Update Vehicle Status")
        vehicle_choice = st.selectbox("Select vehicle", [f"{v.id} - {v.reg_number}" for v in vehicles])
        if vehicle_choice:
            vid = int(vehicle_choice.split(" - ")[0])
            selected = db.query(Vehicle).get(vid)
            new_status = st.selectbox("Status", ["active", "suspended", "scrapped"],
                                       index=["active", "suspended", "scrapped"].index(selected.status))
            if st.button("Update Status"):
                selected.status = new_status
                db.commit()
                log_activity(user["user_id"], f"Updated vehicle {selected.reg_number} status to {new_status}")
                st.success("Vehicle status updated.")
                st.rerun()

with tab_add:
    with st.form("add_vehicle"):
        c1, c2 = st.columns(2)
        with c1:
            reg_number = st.text_input("Registration Number (e.g. DHAKA METRO-GA-12-3456)")
            make = st.text_input("Make (e.g. Toyota)")
            model = st.text_input("Model (e.g. Corolla)")
        with c2:
            year = st.number_input("Year", min_value=1990, max_value=dt.date.today().year, value=2020)
            vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Bus", "Truck", "CNG"])
            engine_no = st.text_input("Engine Number")
        chassis_no = st.text_input("Chassis Number")
        submitted = st.form_submit_button("Register Vehicle")
        if submitted:
            if not reg_number or not make:
                st.error("Registration number and make are required.")
            else:
                existing = db.query(Vehicle).filter(Vehicle.reg_number == reg_number).first()
                if existing:
                    st.error("A vehicle with this registration number already exists.")
                else:
                    v = Vehicle(
                        owner_id=user["user_id"], reg_number=reg_number, make=make, model=model,
                        year=int(year), vehicle_type=vehicle_type, engine_no=engine_no,
                        chassis_no=chassis_no, status="active"
                    )
                    db.add(v)
                    db.commit()
                    log_activity(user["user_id"], f"Registered new vehicle {reg_number}")
                    st.success(f"Vehicle {reg_number} registered successfully.")
                    st.rerun()

db.close()
