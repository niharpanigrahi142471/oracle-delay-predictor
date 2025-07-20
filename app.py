import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# Configure Streamlit page
st.set_page_config(page_title="Oracle Delay Analysis 🔍", layout="centered")
st.title("🧾 Oracle Delay Analysis Tool")
st.markdown("Upload your Oracle project Excel file with **Planned Date** and **Actual Date** columns.")

# Load API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# File upload
uploaded_file = st.file_uploader("📁 Upload Excel file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # Read file based on extension
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Validate required columns
        if 'Planned Date' not in df.columns or 'Actual Date' not in df.columns:
            st.error("❌ Excel must contain 'Planned Date' and 'Actual Date' columns.")
        else:
            # Convert to datetime
            df['Planned Date'] = pd.to_datetime(df['Planned Date'], errors='coerce')
            df['Actual Date'] = pd.to_datetime(df['Actual Date'], errors='coerce')

            # Remove rows with invalid dates
            df = df.dropna(subset=['Planned Date', 'Actual Date'])

            # Calculate delay
            df['Delay (days)'] = (df['Actual Date'] - df['Planned Date']).dt.days
            st.success("✅ File loaded and delays calculated.")

            st.subheader("📊 Delay Summary")
            st.dataframe(df[['Planned Date', 'Actual Date', 'Delay (days)']])

            # Prepare data for AI analysis
            delay_data_text = df[['Planned Date', 'Actual Date', 'Delay (days)']].head(10).to_string(index=False)
            prompt = f"""You are an Oracle Project Delay Analyst.

Below is the extracted delay data from an Oracle implementation project. Based on the patterns, suggest possible reasons for delays and 3 mitigation strategies:

{delay_data_text}
"""

            # Call OpenAI
            with st.spinner("🧠 Analyzing delays using AI..."):
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a project delay analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )

            ai_analysis = response.choices[0].message.content
            st.subheader("📌 AI Insights")
            st.markdown(ai_analysis)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
