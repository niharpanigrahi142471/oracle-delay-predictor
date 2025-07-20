import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_project_plan(project_text):
    prompt = f"""
You are an expert AI Project Consultant with deep experience in analyzing complex IT and transformation project plans.

Your task is to:
- Identify relevant AI use cases, risks, gaps, automation opportunities, and innovative possibilities.
- Suggest improvements to elevate the plan’s efficiency, intelligence, and strategic value.

Please analyze the following project plan and return structured recommendations under these headings:
1. 🔍 AI Opportunities
2. ⚠️ Risks or Gaps
3. ✅ Suggested Enhancements
4. 📊 Automation Areas
5. 💡 Innovation Ideas

Project Plan Input:
\"\"\"
{project_text}
\"\"\"

Be concise, insightful, and use clear bullet points under each heading. Avoid repetition.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # use "gpt-3.5-turbo" if GPT-4 is not available
            messages=[
                {"role": "system", "content": "You are a senior AI consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1200
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
