import openai import pandas as pd from datetime import datetime import os

--- CONFIGURATION ---

openai.api_key = os.getenv("OPENAI_API_KEY")  # Or set directly MODEL = "gpt-4" FILE_PATH = "sample_project_delay_data.xlsx"  # Replace with .csv if needed

--- LOAD DATA ---

def load_data(file_path): if file_path.endswith(".csv"): df = pd.read_csv(file_path) elif file_path.endswith(".xlsx"): df = pd.read_excel(file_path) else: raise ValueError("Unsupported file format") return df

--- PROCESS DATA ---

def compute_delays(df): df["Planned_End_Date"] = pd.to_datetime(df["Planned_End_Date"]) df["Actual_End_Date"] = pd.to_datetime(df["Actual_End_Date"]) df["Delay_Days"] = (df["Actual_End_Date"] - df["Planned_End_Date"]).dt.days return df

--- GENERATE INSIGHTS ---

def generate_ai_insights(df): delay_summary = df[["Project_Name", "Delay_Days", "Owner", "Status"]].to_dict(orient="records") prompt = f""" You are a project management AI assistant. Analyze the following project delays: {delay_summary}

Give insights on causes of delay, suggest corrective actions, and identify risky owners or patterns. Provide insights in bullet points. """

response = openai.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}]
)
return response.choices[0].message.content

--- MAIN ---

if name == "main": df = load_data(FILE_PATH) df = compute_delays(df) insights = generate_ai_insights(df) print("\n--- AI Insights ---\n") print(insights)

