import streamlit as st
import pandas as pd
from io import StringIO
from openai import OpenAI  # Updated import

# Page setup
st.set_page_config(page_title="Oracle Project Delay Analyzer", layout="wide")

# Header
st.title("📊 Oracle Project Delay Analyzer (Powered by OpenAI GPT)")

# File uploader
uploaded_file = st.file_uploader("Upload your delay data file (CSV)", type="csv")

# API client setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Process uploaded file
if uploaded_file is not None:
    # Read the CSV
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Show preview
        st.subheader("🧾 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Allow user to select relevant columns
        st.subheader("🔧 Select Columns for Analysis")
        task_col = st.selectbox("Task/Activity Column", df.columns)
        start_col = st.selectbox("Planned Start Date", df.columns)
        end_col = st.selectbox("Planned End Date", df.columns)
        actual_end_col = st.selectbox("Actual End Date", df.columns)

        if st.button("Analyze Delay"):
            try:
                # Prepare prompt for GPT
                delay_data = df[[task_col, start_col, end_col, actual_end_col]].copy()
                delay_data.columns = ["Task", "Planned Start", "Planned End", "Actual End"]

                csv_string = delay_data.to_csv(index=False)
                prompt = (
                    "Analyze the following project delay data for patterns, root causes, and suggest mitigations:\n"
                    f"{csv_string}\n"
                    "Focus on systemic issues, resource constraints, scope changes, and possible Oracle project challenges."
                )

                # GPT Call with updated SDK usage
                with st.spinner("Analyzing delays using OpenAI..."):
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a project delay analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=800
                    )

                analysis = response.choices[0].message.content
                st.subheader("🧠 AI-Powered Analysis")
                st.markdown(analysis)

            except Exception as e:
                st.error(f"⚠️ Error during analysis: {e}")

    except Exception as e:
        st.error(f"❌ Failed to read the file: {e}")
else:
    st.info("📥 Please upload a CSV file with Oracle project data.")
