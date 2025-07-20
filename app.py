import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# Set up Streamlit page
st.set_page_config(page_title="Oracle Delay Analysis", layout="centered")
st.title("🧾 Oracle Delay Analysis Tool")
st.markdown("Upload your Excel or CSV file containing Oracle project timelines. Required columns: **Planned_End_Date** and **Actual_End_Date**.")

# Load API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# File uploader
uploaded_file = st.file_uploader("📁 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # Load DataFrame based on file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Check required columns
        required_cols = {'Planned_End_Date', 'Actual_End_Date'}
        if not required_cols.issubset(df.columns):
            st.error("❌ Your file must contain 'Planned_End_Date' and 'Actual_End_Date' columns.")
        else:
            # Convert to datetime
            df['Planned_End_Date'] = pd.to_datetime(df['Planned_End_Date'], errors='coerce')
            df['Actual_End_Date'] = pd.to_datetime(df['Actual_End_Date'], errors='coerce')

            # Calculate delay
            df['Delay_Days'] = (df['Actual_End_Date'] - df['Planned_End_Date']).dt.days

            st.success("✅ File uploaded and delays calculated.")
            st.subheader("📊 Delay Summary")
            st.dataframe(df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']])

            # Prepare input for OpenAI
            sample_rows = df[['Planned_End_Date', 'Actual_End_Date', 'Delay_Days']].head(10).to_string(index=False)

            prompt = f"""
You are an Oracle project management expert. Analyze the delay trends based on the following data:

{sample_rows}

1. What patterns do you observe in the delays?
2. What could be possible reasons for the delays in an Oracle Cloud implementation project?
3. What mitigation strategies should be adopted?
Please respond as if advising a Delivery Head.
"""

            # Call OpenAI Chat API using SDK v1.x format
            with st.spinner("🧠 Analyzing delays using OpenAI GPT-4..."):
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an Oracle program delay analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=700
                )

            result = response.choices[0].message.content
            st.subheader("📌 AI Insight")
            st.write(result)

    except Exception as e:
        st.error(f"⚠️ Error occurred: {str(e)}")
