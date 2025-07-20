import pandas as pd
import openai
import os
from datetime import datetime
from typing import Union

# ✅ Set OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Helper to load Excel or CSV
def load_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Only .xlsx and .csv files are supported")
    return df

# ✅ Compute delay days
def calculate_delay(df: pd.DataFrame) -> pd.DataFrame:
    if 'Planned_End_Date' not in df.columns or 'Actual_End_Date' not in df.columns:
        raise ValueError("Your file must contain 'Planned_End_Date' and 'Actual_End_Date' columns.")
    
    df['Planned_End_Date'] = pd.to_datetime(df['Planned_End_Date'], errors='coerce')
    df['Actual_End_Date'] = pd.to_datetime(df['Actual_End_Date'], errors='coerce')
    df['Delay_Days'] = (df['Actual_End_Date'] - df['Planned_End_Date']).dt.days
    return df

# ✅ Generate AI insights using latest OpenAI SDK (>=1.0.0)
def get_ai_insight(df: pd.DataFrame) -> str:
    prompt = f"""
You are a project management AI. Analyze the following project delay data and summarize insights, risks, and possible root causes:
{df[['Project_Name', 'Planned_End_Date', 'Actual_End_Date', 'Delay_Days']].to_string(index=False)}
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a senior project analyst."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ✅ Main
def main():
    file_path = input("Enter the path to your Excel or CSV file: ").strip()
    
    try:
        df = load_file(file_path)
        df = calculate_delay(df)
        print("\n📊 Delay Analysis Completed:")
        print(df[['Project_Name', 'Delay_Days']])

        print("\n🤖 Generating AI Insight...\n")
        insight = get_ai_insight(df)
        print("🔍 AI Insight:\n")
        print(insight)
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()
