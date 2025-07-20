import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Oracle Project Delay Predictor", layout="centered")

st.title("📊 Oracle Project Delay Predictor")
st.write("Upload a project tracking Excel file to begin analysis:")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    if {'Planned_End', 'Actual_End'}.issubset(df.columns):
        # Convert dates
        df['Planned_End'] = pd.to_datetime(df['Planned_End'])
        df['Actual_End'] = pd.to_datetime(df['Actual_End'], errors='coerce')

        # Calculate delay
        df['Delay_Days'] = (df['Actual_End'] - df['Planned_End']).dt.days
        df['Delay_Days'] = df['Delay_Days'].fillna(0)

        st.subheader("📊 Delay Distribution")
        st.bar_chart(df['Delay_Days'])

        # AI Model: Predict Delay_Days based on other fields
        # Example: using Planned_End ordinal date
        df['Planned_Ordinal'] = df['Planned_End'].map(lambda x: x.toordinal())
        X = df[['Planned_Ordinal']]
        y = df['Delay_Days']

        # Train only on rows where Actual_End exists
        mask = df['Actual_End'].notna()
        model = LinearRegression()
        model.fit(X[mask], y[mask])

        # Predict for all rows
        df['Predicted_Delay'] = model.predict(X)

        st.subheader("🧠 AI-Predicted Delay (Days)")
        st.dataframe(df[['Project_ID', 'Task', 'Planned_End', 'Predicted_Delay']].head(10))

        st.subheader("📍 Most At-Risk Tasks (Predicted Delay > 5 days)")
        at_risk = df[df['Predicted_Delay'] > 5]
        if not at_risk.empty:
            st.dataframe(at_risk[['Project_ID', 'Task', 'Planned_End', 'Predicted_Delay']])
        else:
            st.success("No critical delays predicted 🎉")

    else:
        st.warning("⚠️ Your file must contain 'Planned_End' and 'Actual_End' columns.")
