import streamlit as st
import pandas as pd
import datetime as dt
from utils.db import get_session, Vehicle, Violation, Appeal
from utils import auth
from utils.auth import log_activity

st.set_page_config(page_title="Appeals - DriveBD", page_icon="⚖️", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("⚖️ Violation Appeals")
db = get_session()

tab_file, tab_status = st.tabs(["File an Appeal", "My Appeals"])

with tab_file:
    vehicle_ids = [v.id for v in db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()]
    appealable = db.query(Violation).filter(
        Violation.vehicle_id.in_(vehicle_ids), Violation.status == "unpaid"
    ).all() if vehicle_ids else []

    if not appealable:
        st.info("You have no unpaid violations eligible for appeal.")
    else:
        options = {f"#{v.id} - {v.violation_type} ({v.vehicle.reg_number}) - BDT {v.fine_amount:,.0f}": v for v in appealable}
        choice = st.selectbox("Select violation to appeal", list(options.keys()))
        reason = st.text_area("Reason for appeal", placeholder="Explain why you believe this fine should be waived...")
        if st.button("Submit Appeal"):
            if not reason.strip():
                st.error("Please provide a reason for your appeal.")
            else:
                violation = options[choice]
                appeal = Appeal(
                    violation_id=violation.id, user_id=user["user_id"], reason=reason,
                    status="pending", date=dt.date.today()
                )
                violation.status = "appealed"
                db.add(appeal)
                db.commit()
                log_activity(user["user_id"], f"Filed appeal for violation #{violation.id}")
                st.success("Your appeal has been submitted and is pending review.")
                st.rerun()

with tab_status:
    appeals = db.query(Appeal).filter(Appeal.user_id == user["user_id"]).order_by(Appeal.date.desc()).all()
    if not appeals:
        st.info("You haven't filed any appeals yet.")
    else:
        for a in appeals:
            badge = {"pending": "🟡", "approved": "🟢", "rejected": "🔴"}.get(a.status, "⚪")
            with st.container(border=True):
                st.write(f"{badge} Appeal #{a.id} for Violation #{a.violation_id} — **{a.status.title()}**")
                st.caption(f"Filed on {a.date}")
                st.write(f"Reason: {a.reason}")
                if a.admin_comment:
                    st.info(f"Admin comment: {a.admin_comment}")

db.close()
