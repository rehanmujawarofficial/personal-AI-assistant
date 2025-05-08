
import google.generativeai as genai
from config import GENAI_API_KEY

genai.configure(api_key=GENAI_API_KEY)
genai_client = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt):
    try:
        response = genai_client.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "Gemini AI did not respond."
    except Exception as e:
        return f"Error: {str(e)}"
