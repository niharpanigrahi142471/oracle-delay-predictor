import streamlit as st
import pandas as pd
import openai

# Page config
st.set_page_config(page_title="Oracle Fusion Analyzer", layout="wide")
st.title("📊 Oracle Fusion Project Upload & Analyzer")

# Set OpenAI key (use secrets in deployment)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Upload section
uploaded_file = st.file_uploader("📂 Upload your Oracle project file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read uploaded file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Normalize column names (strip and lowercase)
        df.columns = df.columns.str.strip().str.lower()

        st.success("✅ File uploaded and processed!")
        st.subheader("📑 Preview")
        st.dataframe(df.head(10))

        # Show charts only if required columns exist
        if 'module' in df.columns:
            st.subheader("📊 Modules Distribution")
            st.bar_chart(df['module'].value_counts())
        else:
            st.warning("⚠️ 'Module' column not found (even with case-insensitive match).")

        if 'owner' in df.columns:
            st.subheader("👤 Owner Distribution")
            st.bar_chart(df['owner'].value_counts())
        else:
            st.warning("⚠️ 'Owner' column not found (even with case-insensitive match).")

    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
else:
    st.info("📁 Please upload a file to continue.")
