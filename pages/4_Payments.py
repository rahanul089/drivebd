import streamlit as st
import pandas as pd
import datetime as dt
import random
from utils.db import get_session, Vehicle, Violation, Payment
from utils import auth
from utils.auth import log_activity
from utils.pdf_utils import generate_receipt_pdf

st.set_page_config(page_title="Payments - DriveBD", page_icon="💳", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("💳 Payment System")
db = get_session()

tab_pay, tab_history = st.tabs(["Pay a Fine", "Payment History"])

with tab_pay:
    vehicle_ids = [v.id for v in db.query(Vehicle).filter(Vehicle.owner_id == user["user_id"]).all()]
    unpaid = db.query(Violation).filter(
        Violation.vehicle_id.in_(vehicle_ids), Violation.status == "unpaid"
    ).all() if vehicle_ids else []

    if not unpaid:
        st.success("You have no unpaid fines. 🎉")
    else:
        st.write(f"You have **{len(unpaid)}** unpaid fine(s) totaling **BDT {sum(v.fine_amount for v in unpaid):,.0f}**")
        options = {f"#{v.id} - {v.violation_type} ({v.vehicle.reg_number}) - BDT {v.fine_amount:,.0f}": v for v in unpaid}
        choice = st.selectbox("Select violation to pay", list(options.keys()))
        method = st.selectbox("Payment Method", ["bKash", "Nagad", "Rocket", "Card", "Bank Transfer"])

        if st.button("Pay Now"):
            violation = options[choice]
            ref_no = f"TXN{random.randint(100000,999999)}"
            payment = Payment(
                violation_id=violation.id, user_id=user["user_id"], amount=violation.fine_amount,
                method=method, date=dt.date.today(), status="completed", reference_no=ref_no
            )
            violation.status = "paid"
            db.add(payment)
            db.commit()
            log_activity(user["user_id"], f"Paid fine #{violation.id} via {method}")
            st.success(f"Payment successful! Reference: {ref_no}")

            pdf_bytes = generate_receipt_pdf(
                title="DriveBD Payment Receipt",
                fields={
                    "Reference No": ref_no,
                    "Payer": user["name"],
                    "Vehicle": violation.vehicle.reg_number,
                    "Violation": violation.violation_type,
                    "Amount Paid (BDT)": f"{violation.fine_amount:,.0f}",
                    "Payment Method": method,
                    "Date": str(dt.date.today()),
                }
            )
            st.download_button("⬇️ Download Receipt (PDF)", data=pdf_bytes,
                                file_name=f"receipt_{ref_no}.pdf", mime="application/pdf")

with tab_history:
    payments = db.query(Payment).filter(Payment.user_id == user["user_id"]).order_by(Payment.date.desc()).all()
    if not payments:
        st.info("No payment history yet.")
    else:
        df = pd.DataFrame([{
            "Date": p.date, "Amount (BDT)": p.amount, "Method": p.method,
            "Reference": p.reference_no, "Status": p.status,
            "Violation": p.violation.violation_type if p.violation else "N/A"
        } for p in payments])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("Total Paid (BDT)", f"{sum(p.amount for p in payments):,.0f}")

db.close()
