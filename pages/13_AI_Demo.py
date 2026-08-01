"""
Mock AI vehicle-image violation demo.
This is a RULE-BASED SIMULATION for demo/portfolio purposes only — it does not run a real
computer-vision model. It analyzes basic image properties (brightness, color balance, size)
and maps them deterministically-but-randomly to a plausible "detection" result, purely to
illustrate what such a feature's UI/UX and API response shape could look like.
"""
import streamlit as st
import random
import hashlib
from PIL import Image
import numpy as np

st.set_page_config(page_title="AI Demo - DriveBD", page_icon="🤖", layout="wide")

st.title("🤖 Mock AI Violation Detection (Demo)")
st.warning("⚠️ This is a **simulated** demo, not a real AI model. It illustrates the intended "
           "feature and API response shape without performing real computer vision.")

uploaded_image = st.file_uploader("Upload a vehicle/traffic image", type=["jpg", "jpeg", "png"])

VIOLATION_LABELS = [
    "No Helmet Detected", "Illegal Parking", "Signal Violation", "Overloading",
    "No Violation Detected", "Fake/Obscured Plate Suspected", "Wrong Lane Usage"
]

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("Run Mock Detection"):
        with st.spinner("Analyzing image (simulated)..."):
            # Deterministic "pseudo-analysis" seeded by image bytes so repeated runs are stable
            arr = np.array(image.resize((64, 64)))
            digest = hashlib.md5(arr.tobytes()).hexdigest()
            seed = int(digest[:8], 16)
            rng = random.Random(seed)

            brightness = float(arr.mean())
            label = rng.choice(VIOLATION_LABELS)
            confidence = round(rng.uniform(0.55, 0.97), 2)

        st.subheader("Mock Detection Result")
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Label", label)
        col2.metric("Confidence", f"{confidence*100:.0f}%")
        col3.metric("Avg. Brightness", f"{brightness:.0f}/255")

        st.json({
            "endpoint": "/api/v1/ai/detect-violation",
            "model": "mock-vision-v0 (simulated)",
            "result": {
                "label": label,
                "confidence": confidence,
                "image_size": image.size,
                "notes": "This result is randomly generated for demonstration purposes."
            }
        })

        if label != "No Violation Detected":
            st.error(f"Potential violation flagged: **{label}** — an officer would review this "
                     f"in a real deployment before any fine is issued.")
        else:
            st.success("No violation flagged in this mock analysis.")
else:
    st.info("Upload an image to see the mock detection demo in action.")
