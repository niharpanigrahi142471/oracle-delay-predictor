import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(
    page_title="Oracle Delay Predictor",
    page_icon="📊",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.success("Select a page on the sidebar.")

# --- Title ---
st.markdown("""
<div style="text-align:center; padding:20px 0;">
    <h1 style="color:#4F8BF9;">📊 Oracle Delay Predictor</h1>
    <p>Predict order/project delays across Oracle Cloud systems using AI-powered logic.</p>
</div>
""", unsafe_allow_html=True)

# --- File Upload Section ---
st.header("📥 Upload Your CSV Data")
uploaded_file = st.file_uploader("Upload your Oracle project delay CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview Uploaded Data", df.head())
    # Optional: show summary stats
    st.write("### Delay Summary", df["Status"].value_counts())

else:
    st.info("📁 Please upload a CSV file to see live predictions and data analysis.")

# --- Features Section ---
st.markdown("---")
st.markdown("### 🔍 How It Works")
st.markdown("""
- Upload your Oracle project CSV (with columns: Project_ID, Region, Module, Start_Date, End_Date, Status, SLA_Days, Actual_Days)
- View uploaded data preview  
- See delay status distribution  
""")

# --- Optional Diagram ---
image_path = "images/oracle_diagram.png"
if os.path.exists(image_path):
    st.image(image_path, caption="System Diagram", use_column_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ by Nihar • [GitHub Repo](https://github.com/niharpanigrahi142471/oracle-delay-predictor)")
