import streamlit as st
import pandas as pd
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client using v1.x+ syntax
client = OpenAI(api_key=openai_api_key)

st.set_page_config(page_title="Oracle Delay Predictor 🔍", layout="wide")

st.title("📊 Oracle Delay Insight - AI Powered")
st.markdown("Upload your project sheet with **Planned Date** and **Actual Date** to get smart delay analysis.")

uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if "Planned Date" not in df.columns or "Actual Date" not in df.columns:
            st.error("Your Excel must contain 'Planned Date' and 'Actual Date' columns.")
        else:
            df["Planned Date"] = pd.to_datetime(df["Planned Date"], errors='coerce')
            df["Actual Date"] = pd.to_datetime(df["Actual Date"], errors='coerce')

            df["Delay (days)"] = (df["Actual Date"] - df["Planned Date"]).dt.days
            st.success("✅ Data processed successfully.")
            st.dataframe(df.head(10), use_container_width=True)

            # Prepare insight summary
            delay_summary = f"""
            Summary of Delays:
            - Total Records: {len(df)}
            - Delayed Tasks: {(df['Delay (days)'] > 0).sum()}
            - On-time or Early Tasks: {(df['Delay (days)'] <= 0).sum()}
            - Average Delay: {df['Delay (days)'].mean():.2f} days
            """

            with st.expander("📄 Delay Summary"):
                st.text(delay_summary)

            # Send prompt to OpenAI for insight
            st.subheader("🔍 AI Insights from Delay Patterns")

            sample_rows = df[["Planned Date", "Actual Date", "Delay (days)"]].dropna().head(20).to_string(index=False)

            prompt = (
                "You are a project delivery expert. Analyze the following project milestone data, "
                "highlight any patterns or risks of delay, and suggest improvements.\n\n"
                f"{sample_rows}\n\n"
                "Give insights in 4-5 bullet points."
            )

            if openai_api_key:
                with st.spinner("🧠 Analyzing with GPT..."):
                    try:
                        completion = client.chat.completions.create(
                            model="gpt-4",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.5,
                            max_tokens=500
                        )
                        insights = completion.choices[0].message.content
                        st.markdown(insights)
                    except Exception as e:
                        st.error(f"OpenAI API Error: {e}")
            else:
                st.warning("🔑 Missing OpenAI API key. Please set it in your `.env` or environment variables.")
    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
