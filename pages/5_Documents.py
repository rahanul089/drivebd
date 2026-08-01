import streamlit as st
import pandas as pd
import datetime as dt
from utils.db import get_session, Vehicle, Document
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Documents - DriveBD", page_icon="📁", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("📁 Document Vault")
db = get_session()

tab_view, tab_upload = st.tabs(["My Documents", "Upload New Document"])

with tab_view:
    docs = db.query(Document).filter(Document.user_id == user["user_id"]).all()
    if not docs:
        st.info("No documents uploaded yet.")
    else:
        for d in docs:
            badge = {"valid": "🟢", "expiring": "🟡", "expired": "🔴"}.get(d.status, "⚪")
            with st.expander(f"{badge} {d.doc_type} — {d.status.title()}"):
                c1, c2 = st.columns(2)
                c1.write(f"**Uploaded on:** {d.uploaded_on}")
                c1.write(f"**Linked vehicle:** {d.vehicle.reg_number if d.vehicle else 'N/A'}")
                c2.write(f"**Expiry date:** {d.expiry_date if d.expiry_date else 'N/A'}")
                c2.write(f"**File:** `{d.file_path}` (mock storage path)")
                if d.status == "expiring":
                    st.warning("This document is expiring soon — please renew it.")
                elif d.status == "expired":
                    st.error("This document has expired.")

with tab_upload:
    with st.form("upload_doc"):
        doc_type = st.selectbox("Document Type", [
            "NID", "Driving License", "Vehicle Registration", "Fitness Certificate", "Tax Token", "Insurance"
        ])
        my_vehicles = db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()
        vehicle_choice = st.selectbox(
            "Linked Vehicle (optional)",
            ["None"] + [f"{v.id} - {v.reg_number}" for v in my_vehicles]
        )
        has_expiry = doc_type in ("Fitness Certificate", "Tax Token", "Insurance")
        expiry = st.date_input("Expiry Date", value=dt.date.today()) if has_expiry else None
        uploaded_file = st.file_uploader("Upload file (PDF/JPG/PNG) — stored as mock reference only")
        submitted = st.form_submit_button("Upload")
        if submitted:
            vid = None if vehicle_choice == "None" else int(vehicle_choice.split(" - ")[0])
            status = "valid"
            if expiry:
                if expiry < dt.date.today():
                    status = "expired"
                elif (expiry - dt.date.today()).days < 60:
                    status = "expiring"
            file_path = f"/documents/{user['user_id']}_{doc_type.replace(' ', '_')}_{uploaded_file.name if uploaded_file else 'file'}"
            d = Document(
                user_id=user["user_id"], vehicle_id=vid, doc_type=doc_type, file_path=file_path,
                expiry_date=expiry, status=status
            )
            db.add(d)
            db.commit()
            log_activity(user["user_id"], f"Uploaded document: {doc_type}")
            st.success(f"{doc_type} uploaded successfully.")
            st.rerun()

db.close()
