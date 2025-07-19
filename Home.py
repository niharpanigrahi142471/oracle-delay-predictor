# Home.py

import streamlit as st
from PIL import Image

# Logo (Optional)
st.image("https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.png", width=150)

# Title
st.title("Oracle Delay Predictor – AI App")

# Subtitle
st.subheader("⚙️ Predict Order Processing Delays in Oracle UIM / OSM / BRM Flow")

# Overview
st.markdown("""
This app uses a trained AI model to predict potential **order delays** in the Oracle provisioning flow based on:
- Order type (Prepaid/Postpaid/Device)
- SIM or Device status
- Fulfillment path and orchestration stage
- Real-time exception signals

Simply input the current order status and system stage below to get a delay prediction in seconds.
""")

# Input section
st.header("📥 Enter Order Details")
order_type = st.selectbox("Order Type", ["Prepaid", "Postpaid", "Bundled", "Device"])
orchestration_stage = st.selectbox("Current Orchestration Stage", ["Initiated", "Pending SIM Activation", "Fulfillment", "Plan Activation"])
system_flag = st.radio("Any Alert in BRM?", ["Yes", "No"])
sla_remaining = st.slider("Remaining SLA Time (mins)", 1, 240, 60)

# Predict button
if st.button("🔍 Predict Delay Risk"):
    # Simple mock logic
    delay_risk = "High" if orchestration_stage == "Pending SIM Activation" and system_flag == "Yes" else "Low"
    st.success(f"🚦 Predicted Delay Risk: **{delay_risk}**")
    st.info("You may need to escalate to fulfillment team.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + AI for Oracle cloud ops teams.")
