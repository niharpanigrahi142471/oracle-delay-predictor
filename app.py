import streamlit as st
import pandas as pd
import openai

# Set page
st.set_page_config(page_title="Oracle Fusion Analyzer", layout="wide")
st.title("📊 Oracle Fusion Project Analyzer with AI Insights")

# Get OpenAI key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Upload file
uploaded_file = st.file_uploader("📂 Upload Oracle project (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        st.success("✅ File uploaded successfully!")
        st.subheader("🔍 Preview")
        st.dataframe(df.head(10))

        # Show module chart
        if 'module' in df.columns:
            st.subheader("📊 Module Distribution")
            st.bar_chart(df['module'].value_counts())
        else:
            st.warning("⚠️ 'Module' column not found.")

        # Show owner chart
        if 'owner' in df.columns:
            st.subheader("👤 Owner Distribution")
            st.bar_chart(df['owner'].value_counts())
        else:
            st.warning("⚠️ 'Owner' column not found.")

        # --- AI Insights ---
        st.subheader("🧠 AI Insights on Oracle Fusion Project")

        # Prepare a summary text
        data_preview = df.head(20).to_string(index=False)

        prompt = f"""
You are a senior Oracle ERP transformation consultant. Based on this project data (first 20 rows), give 5 concise insights:

Project Data:
{data_preview}

Output format:
1. Key pain points across modules
2. Overloaded owners or teams
3. Possible duplicate modules or overlaps
4. Suggested governance improvements
5. Transformation risks to watch
"""

        # Call OpenAI
        with st.spinner("🧠 Thinking... generating insights..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior Oracle implementation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=500
            )

            gpt_output = response['choices'][0]['message']['content']
            st.success("✅ Insights generated successfully!")
            st.markdown(gpt_output)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📥 Please upload a file to begin.")
