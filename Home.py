import streamlit as st
import pandas as pd
from helper import analyze_delay

st.set_page_config(page_title="Oracle Delay Predictor", layout="wide")

st.title("🔍 Oracle Delivery Delay Predictor - AI Powered")
st.write("Upload your Oracle Project Plan file (CSV) to assess delivery risks and AI-based delay predictions.")

uploaded_file = st.file_uploader("📤 Upload Oracle Project Plan (CSV format)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 AI Delay Risk Analysis")
    risk_df = analyze_delay(df)
    st.dataframe(risk_df)

    high_risk = risk_df[risk_df['Delay Risk'] == 'High']
    if not high_risk.empty:
        st.warning("⚠️ High-risk tasks detected. Please review.")
    else:
        st.success("✅ No high-delay risk tasks detected.")
else:
    st.info("Please upload a project CSV file to begin.")
