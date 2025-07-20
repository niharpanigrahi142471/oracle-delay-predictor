from dotenv import load_dotenv
import os
import openai

# Load variables from .env file
load_dotenv()
# Instead of using dotenv
# from dotenv import load_dotenv
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Use Streamlit secrets instead:
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Read the key securely
openai.api_key = os.getenv("OPENAI_API_KEY")
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Oracle Project Analyzer", layout="wide")

st.title("📊 Oracle Fusion Project Upload & Analyzer")

uploaded_file = st.file_uploader("Upload your Oracle project file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Detect file type
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("🔍 File Preview")
        st.dataframe(df.head())

        # Sample AI-like analysis
        st.subheader("📈 AI-Based Project Insights")

        modules = df['Module'].value_counts() if 'Module' in df.columns else None
        owners = df['Owner'].value_counts() if 'Owner' in df.columns else None

        if modules is not None:
            st.markdown("**Modules Distribution:**")
            st.bar_chart(modules)

        if owners is not None:
            st.markdown("**Ownership Load Distribution:**")
            st.bar_chart(owners)

        st.markdown("✅ Sample AI Insight: _Most open gaps are in Supply Chain & Revenue modules._")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a project file to begin.")
