import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# Load API key from secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Oracle Delay Analysis 🔍", layout="centered")

st.title("🧾 Oracle Delay Analysis Tool")
st.markdown("Upload your project Excel file. It must contain **Planned Date** and **Actual Date** columns.")

# File upload
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Check required columns
        if 'Planned Date' not in df.columns or 'Actual Date' not in df.columns:
            st.error("❌ Your Excel must contain 'Planned Date' and 'Actual Date' columns.")
        else:
            # Convert to datetime
            df['Planned Date'] = pd.to_datetime(df['Planned Date'])
            df['Actual Date'] = pd.to_datetime(df['Actual Date'])

            # Calculate delay
            df['Delay (days)'] = (df['Actual Date'] - df['Planned Date']).dt.days
            st.success("✅ File loaded and delay calculated.")

            st.subheader("📊 Delay Summary")
            st.dataframe(df[['Planned Date', 'Actual Date', 'Delay (days)']])

            # Build prompt for OpenAI
            delay_description = df[['Planned Date', 'Actual Date', 'Delay (days)']].to_string(index=False)
            prompt = f"""Analyze the delay patterns in the following Oracle project data. Suggest reasons and mitigation ideas:

{delay_description}
"""

            # Call OpenAI
            with st.spinner("Analyzing delays using OpenAI..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a project delay analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )

            analysis = response['choices'][0]['message']['content']
            st.subheader("🧠 AI Analysis")
            st.write(analysis)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
