import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oracle Project Analyzer", layout="centered")

st.title("📊 Oracle Project Delay Analyzer")
st.write("Upload your **Excel (.xlsx)** or **CSV (.csv)** file to begin analysis.")

# Upload Section
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # File type detection
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())

        # Basic Summary (you can extend here)
        st.write("### Basic Summary")
        st.write(df.describe())

        # Optional: Add your Oracle project-specific logic here

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

else:
    st.info("Please upload a file to begin.")
