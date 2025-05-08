
from fpdf import FPDF
import datetime
from utils.tts import speak

def save_response_to_pdf(response_text):
    try:
        filename = datetime.datetime.now().strftime("AI_Response_%Y%m%d_%H%M%S.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in response_text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf.output(filename)
        speak(f"Saved to {filename}")
    except Exception as e:
        speak("Error saving PDF")
        print(f"PDF error: {e}")
