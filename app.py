import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page config
st.set_page_config(page_title="Oracle Delay Analysis", layout="centered")
st.title("🧾 Oracle Delay Analysis Tool")
st.markdown("Upload your Excel or CSV file. Required columns: **Planned_End_Date** and **Actual_End_Date**.")

# Upload file
uploaded_file = st.file_uploader("📁 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Check required columns
        if 'Planned_End_Date' not in df.columns or 'Actual_End_Date' not in df.columns:
            st.error("❌ File must contain 'Planned_End_Date' and 'Actual_End_Date' columns.")
        else:
            df['Planned_End_Date'] = pd.to_datetime(df['Planned_End_Date'], errors='coerce')
            df['Actual_End_Date'] = pd.to_datetime(df['Actual_End_Date'], errors='coerce')
            df['Delay_Days'] = (df['Actual_End_Date'] - df['Planned_End_Date']).dt.days

            st.success("✅ Delay calculated successfully.")
            st.subheader("📊 Delay Summary")
            st.dataframe(df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']])

            # Prepare prompt for OpenAI
            sample = df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']].head(10).to_string(index=False)
            prompt = f"""
You are an Oracle Cloud project expert. Analyze the delays below:

{sample}

1. What trends do you see?
2. What might be the causes?
3. What actions should the delivery head take?
"""

            with st.spinner("🧠 Generating insights..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior Oracle Cloud program advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                result = response.choices[0].message.content
                st.subheader("📌 AI Insight")
                st.write(result)

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
