import streamlit as st
import pandas as pd
import openai
import os

# Setup Streamlit page
st.set_page_config(page_title="Oracle Fusion Project Analyzer", layout="wide")

# Set OpenAI key from Streamlit secrets (preferred for deployed apps)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

st.title("📊 Oracle Fusion Project Upload & Analyzer")

uploaded_file = st.file_uploader("Upload your Oracle project file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    try:
        # Detect file type and read
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("🔍 File Preview")
        st.dataframe(df.head(10))

        # --- AI-Based Analysis ---
        st.subheader("📈 AI-Based Project Insights")

        # Module distribution
        if "Module" in df.columns:
            module_counts = df["Module"].value_counts()
            st.markdown("**Modules Distribution:**")
            st.bar_chart(module_counts)
        else:
            st.warning("⚠️ 'Module' column not found in the file.")

        # Owner distribution
        if "Owner" in df.columns:
            owner_counts = df["Owner"].value_counts()
            st.markdown("**Ownership Load Distribution:**")
            st.bar_chart(owner_counts)
        else:
            st.warning("⚠️ 'Owner' column not found in the file.")

        # Sample Insight
        st.markdown("✅ _Sample AI Insight: Most open gaps are in Supply Chain & Revenue modules._")

    except Exception as e:
        st.error(f"❌ Error while reading or analyzing file: {e}")
else:
    st.info("📂 Please upload a project file to begin.")
