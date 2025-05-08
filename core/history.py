
import datetime
from config import HISTORY_FILE
from utils.tts import speak

def log_history(command, response):
    try:
        with open(HISTORY_FILE, "a") as file:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now}]\nCommand: {command}\nResponse: {response}\n\n")
    except Exception as e:
        print(f"Error logging history: {str(e)}")

def show_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = file.read()
        if history:
            speak("Here is your history:")
            print(history)
        else:
            speak("No history available.")
    except Exception as e:
        speak("Sorry, I couldn't read the history.")
        print(f"Error reading history: {str(e)}")

def clear_history():
    try:
        open(HISTORY_FILE, "w").close()
        speak("History has been cleared.")
        print("History cleared.")
    except Exception as e:
        speak("Sorry, I couldn't clear the history.")
        print(f"Error clearing history: {e}")
