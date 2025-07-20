import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# Set up Streamlit page
st.set_page_config(page_title="Oracle Delay Analysis", layout="centered")
st.title("🧾 Oracle Delay Analysis Tool")
st.markdown("Upload your Excel or CSV file containing Oracle project timelines. Required columns: **Planned_End_Date** and **Actual_End_Date**.")

# Load API key securely from .streamlit/secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Upload file (CSV or Excel)
uploaded_file = st.file_uploader("📁 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # Detect file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Check for required columns
        if 'Planned_End_Date' not in df.columns or 'Actual_End_Date' not in df.columns:
            st.error("❌ Your file must contain 'Planned_End_Date' and 'Actual_End_Date' columns.")
        else:
            # Convert dates
            df['Planned_End_Date'] = pd.to_datetime(df['Planned_End_Date'], errors='coerce')
            df['Actual_End_Date'] = pd.to_datetime(df['Actual_End_Date'], errors='coerce')

            # Calculate delay
            df['Delay_Days'] = (df['Actual_End_Date'] - df['Planned_End_Date']).dt.days

            st.success("✅ File uploaded and delays calculated.")

            # Show delay summary
            st.subheader("📊 Delay Summary")
            st.dataframe(df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']])

            # Format for prompt
            sample_rows = df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']].head(10).to_string(index=False)

            prompt = f"""
You are an Oracle project management expert. Analyze the delay trends based on the following data:

{sample_rows}

1. What patterns do you observe in the delays?
2. What could be possible reasons for the delays in an Oracle Cloud implementation project?
3. What mitigation strategies should be adopted?
Please respond as if advising a Delivery Head.
"""

            # AI Analysis
            with st.spinner("🧠 Analyzing delays using OpenAI GPT-4..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an Oracle program delay analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )

            result = response['choices'][0]['message']['content']
            st.subheader("📌 AI Insight")
            st.write(result)

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
