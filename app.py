import os
from dotenv import load_dotenv
import openai
import streamlit as st
import pandas as pd

# Load environment variables from .env (for local dev)
load_dotenv()

# Read OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="AI Code Insight", layout="wide")
st.title("🤖 AI-Powered Code Insight")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

if not openai.api_key:
    st.error("❌ OpenAI API key not found. Set `OPENAI_API_KEY` as an environment variable or secret.")
else:
    if uploaded_file is not None:
        try:
            code = uploaded_file.read().decode("utf-8")

            # Call OpenAI to get insights
            with st.spinner("Generating AI insights..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior software architect. Review the given Python code and provide concise insights: possible bugs, improvements, structure flaws, naming issues, or optimization ideas."},
                        {"role": "user", "content": code}
                    ],
                    temperature=0.3
                )

                ai_insight = response['choices'][0]['message']['content']
                st.markdown("### ✅ AI Code Insight")
                st.success(ai_insight)

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")
    else:
        st.info("👆 Please upload a `.py` file to analyze.")
