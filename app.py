import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Streamlit config
st.set_page_config(page_title="Oracle Project Analyzer", layout="wide")
st.title("📊 Oracle Fusion Project Upload & Analyzer")

# Read OpenAI key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key and "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set up OpenAI client
client = OpenAI(api_key=openai_api_key)

# File uploader
uploaded_file = st.file_uploader("Upload your Oracle project file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("🔍 File Preview")
        st.dataframe(df.head())

        # Normalize column names
        df.columns = [col.strip().capitalize() for col in df.columns]

        # Charts
        if 'Module' in df.columns:
            modules = df['Module'].value_counts()
            st.markdown("### 📌 Modules Distribution")
            st.bar_chart(modules)

        if 'Owner' in df.columns:
            owners = df['Owner'].value_counts()
            st.markdown("### 🧑 Ownership Load Distribution")
            st.bar_chart(owners)

        # Prepare prompt
        st.subheader("🤖 AI-Based Project Insight")

        sample_rows = df.head(10).to_dict(orient='records')
        insight_prompt = (
            "You are an Oracle Project Analyzer AI. "
            "Based on the below project data, give smart insights in 3 bullet points. "
            "Focus on gaps, ownership concentration, and module-wise risks.\n\n"
            f"Data Sample:\n{sample_rows}"
        )

        with st.spinner("Generating insights..."):
            chat_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in Oracle Fusion project analysis."},
                    {"role": "user", "content": insight_prompt}
                ],
                temperature=0.3
            )

            insight = chat_response.choices[0].message.content
            st.markdown("### 📌 AI Insight:")
            st.markdown(insight)

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
else:
    st.info("📤 Please upload a project file to begin.")
