import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

st.set_page_config(
    page_title="Oracle Delay Predictor",
    page_icon="🔮",
    layout="centered"
)

# -------- Landing Page Title --------
st.title("🔮 Oracle Delay Predictor")
st.markdown("""
Welcome to the **Oracle Delay Predictor** — an AI-powered tool designed to predict potential delivery delays in Oracle Cloud ERP projects based on project inputs.

Upload your project configuration or enter sample data below to get started.
""")

st.markdown("---")

# -------- Sample Form Input --------
st.header("📥 Enter Project Parameters")
client_type = st.selectbox("Client Type", ["Telecom", "Retail", "BFSI", "Manufacturing"])
project_size = st.selectbox("Project Size", ["Small", "Medium", "Large"])
customization_level = st.slider("Customization Level (0 to 10)", 0, 10, 5)
integration_points = st.number_input("Integration Points", min_value=0, value=5)
team_experience = st.selectbox("Team Experience Level", ["Low", "Medium", "High"])

# -------- Prediction Logic --------
if st.button("🔎 Predict Delay Risk"):
    # Load mock model (replace with actual model later)
    try:
        model = joblib.load("oracle_model.pkl")  # If you trained a real model
    except:
        model = None

    # Dummy logic for demo
    risk_score = (customization_level * 2 + integration_points) / 10
    if team_experience == "Low":
        risk_score += 2
    elif team_experience == "High":
        risk_score -= 1

    st.markdown("---")
    st.subheader("📊 Prediction Result")
    if risk_score < 4:
        st.success("✅ Low Risk of Delay")
    elif risk_score < 7:
        st.warning("⚠️ Medium Risk of Delay")
    else:
        st.error("🚨 High Risk of Delay")

    st.markdown(f"**Score:** {round(risk_score, 2)}")

# -------- Footer --------
st.markdown("---")
st.markdown("""
Made with ❤️ using [Streamlit](https://streamlit.io/)  
[GitHub Repo](https://github.com/niharpanigrahi142471/oracle-delay-predictor)
""")
