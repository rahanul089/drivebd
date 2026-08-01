"""
Mock BRTA (Bangladesh Road Transport Authority) API demo.
Simulates the kind of lookups a real BRTA integration might expose, using local DB data
as a stand-in for the external government system. Not affiliated with or endorsed by BRTA.
"""
import streamlit as st
import datetime as dt
import random
from utils.db import get_session, Vehicle, User
from utils import auth

st.set_page_config(page_title="Mock BRTA API - DriveBD", page_icon="🏛️", layout="wide")
auth.require_login()

st.title("🏛️ Mock BRTA API Demo")
st.caption("Simulated government API endpoints for demo purposes. No real BRTA system is contacted.")

db = get_session()


def mock_brta_vehicle_lookup(reg_number: str):
    v = db.query(Vehicle).filter(Vehicle.reg_number == reg_number).first()
    if not v:
        return {"status": "error", "message": "Vehicle not found in BRTA mock registry."}
    return {
        "status": "success",
        "endpoint": "/api/v1/brta/vehicle/verify",
        "data": {
            "registration_number": v.reg_number,
            "make": v.make, "model": v.model, "year": v.year,
            "vehicle_class": v.vehicle_type,
            "fitness_status": random.choice(["Valid", "Expired", "Pending Renewal"]),
            "tax_token_status": random.choice(["Valid", "Expired"]),
            "registration_status": v.status,
        }
    }


def mock_brta_license_lookup(license_no: str):
    u = db.query(User).filter(User.license_no == license_no).first()
    if not u:
        return {"status": "error", "message": "License number not found in BRTA mock registry."}
    return {
        "status": "success",
        "endpoint": "/api/v1/brta/license/verify",
        "data": {
            "license_no": u.license_no, "holder_name": u.name,
            "license_class": random.choice(["Professional", "Non-Professional"]),
            "issue_date": str(dt.date(random.randint(2015, 2023), random.randint(1, 12), 1)),
            "expiry_date": str(dt.date(random.randint(2026, 2030), random.randint(1, 12), 1)),
            "status": random.choice(["Active", "Suspended"]),
        }
    }


tab1, tab2 = st.tabs(["Vehicle Fitness/Tax Lookup", "Driving License Verification"])

with tab1:
    st.write("**Endpoint:** `GET /api/v1/brta/vehicle/verify?reg_number=...`")
    reg = st.text_input("Enter registration number", placeholder="e.g. DHAKA METRO-GA-12-3456-1234")
    if st.button("Lookup Vehicle", key="lookup_vehicle"):
        result = mock_brta_vehicle_lookup(reg.strip())
        st.json(result)

with tab2:
    st.write("**Endpoint:** `GET /api/v1/brta/license/verify?license_no=...`")
    lic = st.text_input("Enter driving license number", placeholder="e.g. DL-DHK-123456")
    if st.button("Lookup License", key="lookup_license"):
        result = mock_brta_license_lookup(lic.strip())
        st.json(result)

st.divider()
st.info("💡 Tip: try a registration number or license number from the seeded data "
        "(check `data/vehicles.csv` or `data/users.csv`) to see a successful response.")

db.close()
