import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title
st.title("📊 Oracle Delay Predictor with AI Insights")

# File uploader
uploaded_file = st.file_uploader("Upload Oracle Delay Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        # Simple delay analysis
        if 'Planned Date' in df.columns and 'Actual Date' in df.columns:
            df['Delay (Days)'] = (pd.to_datetime(df['Actual Date']) - pd.to_datetime(df['Planned Date'])).dt.days
            avg_delay = df['Delay (Days)'].mean()

            st.subheader("📈 Delay Analysis")
            st.metric("Average Delay (Days)", round(avg_delay, 2))
            st.bar_chart(df['Delay (Days)'])

            # Generate AI Insight
            st.subheader("🧠 AI Insight")
            sample_data = df[['Module', 'Planned Date', 'Actual Date', 'Delay (Days)']].dropna().head(5).to_dict()

            prompt = (
                "You are an expert project manager. Analyze the following delay data and provide 3 key insights "
                "on why delays might be happening and suggest improvements:\n\n"
                f"{sample_data}"
            )

            try:
                with st.spinner("Generating AI insights..."):
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant for project delay analysis."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5,
                        max_tokens=300
                    )
                    insight = response.choices[0].message.content
                    st.markdown(f"**AI Insight:**\n\n{insight}")
            except Exception as e:
                st.error(f"Failed to generate AI insight: {e}")

        else:
            st.error("Your Excel must contain 'Planned Date' and 'Actual Date' columns.")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# Footer
st.caption("Developed for Oracle Delay Prediction 🔍")
