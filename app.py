import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="Oracle Project Delay Analyzer", layout="wide")

st.title("📊 Oracle Project Delay Analyzer with AI Insights")

# Set your OpenAI API key (can also be set via st.secrets or environment)
openai.api_key = st.secrets["openai"]["api_key"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY")

# Upload file
uploaded_file = st.file_uploader("Upload Oracle Project Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.write("🔍 Preview of Uploaded Data")
        st.dataframe(df.head(20))

        if 'Planned_End_Date' in df.columns and 'Actual_End_Date' in df.columns:
            # Convert date columns
            df['Planned_End_Date'] = pd.to_datetime(df['Planned_End_Date'], errors='coerce')
            df['Actual_End_Date'] = pd.to_datetime(df['Actual_End_Date'], errors='coerce')
            df['Delay_Days'] = (df['Actual_End_Date'] - df['Planned_End_Date']).dt.days
            df['Delayed'] = df['Delay_Days'] > 0

            delayed_df = df[df['Delayed'] == True]

            st.subheader("🚨 Delayed Tasks Summary")
            st.write(delayed_df[['Task_Name', 'Planned_End_Date', 'Actual_End_Date', 'Delay_Days']])

            st.metric("Total Tasks", len(df))
            st.metric("Delayed Tasks", len(delayed_df))

            # Generate AI Insight
            if len(delayed_df) > 0 and st.button("🧠 Generate Delay Insights with AI"):
                sample_data = delayed_df[['Task_Name', 'Delay_Days']].head(10).to_string(index=False)
                prompt = f"""You are a project delivery expert for Oracle ERP/SCM transformations.

Here are delayed tasks from a project:

{sample_data}

Give possible reasons for delay and suggestions to avoid such delays in future."""

                with st.spinner("Generating AI insights..."):
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You're a senior Oracle project manager."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.6
                        )
                        ai_output = response['choices'][0]['message']['content']
                        st.success("AI-Powered Delay Insights")
                        st.markdown(ai_output)
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")
        else:
            st.warning("Your file must contain 'Planned_End_Date' and 'Actual_End_Date' columns.")
    except Exception as e:
        st.error(f"File processing error: {e}")
else:
    st.info("Please upload a .csv or .xlsx file to begin analysis.")
