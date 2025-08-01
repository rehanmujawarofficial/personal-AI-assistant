import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import datetime
import subprocess
import win32gui
import win32con
import webbrowser
import google.generativeai as genai
import time
from fpdf import FPDF

HISTORY_FILE = "history.txt"
VOICE_PASSWORD = "008" 
WAKE_WORD = "007"

# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty("rate", 190)
engine.setProperty("volume", 1)

def verify_password():
    speak("Please say the password to continue.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source)
            entered_password = recognizer.recognize_google(audio).lower()
            return entered_password == VOICE_PASSWORD.lower()
        except:
            speak("Sorry, I couldn't understand the password.")
            return False
 
# Function to show history
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

def log_history(command, response):
    try:
        with open(HISTORY_FILE, "a") as file:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now}]\nCommand: {command}\nResponse: {response}\n\n")
    except Exception as e:
        print(f"Error logging history: {str(e)}")

# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Welcome")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                if WAKE_WORD in command:
                    speak("Hello sir! How can I help you today?")
                    execute_commands()
                else:
                    print("Wake word not detected. Call me again...")
            except sr.UnknownValueError:
                print("Didn't catch that. Call me again...")
            except sr.RequestError:
                print("Error connecting to speech recognition service.")

# Command execution loop
def execute_commands():
    recognizer = sr.Recognizer()
    last_ai_response = ""  # Store last Gemini response
    with sr.Microphone() as source:
        while True:
            print("What can I do for you sir? (Say 'bye' to stop)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")
                response = ""  # For logging

                if "bye" in command:
                    response = "Assistant stopped. Say '007' to wake me again."
                    speak(response)
                    log_history(command, response)
                    break

                elif "open" in command:
                    app = command.replace("open ", "").strip()
                    response = f"Opening {app}"
                    open_application(app)
                    log_history(command, response)

                elif "search on chrome" in command:
                    query = command.replace("search on chrome", "").strip()
                    response = f"Searching for {query} on Chrome"
                    search_on_chrome(query)
                    log_history(command, response)

                elif "close" in command:
                    app = command.replace("close ", "").strip()
                    response = f"Closing {app}"
                    close_application(app)
                    log_history(command, response)

                elif "minimize" in command or "minimise" in command:
                    app = command.replace("minimize ", "").replace("minimise ", "").strip()
                    response = f"Minimizing {app}"
                    minimize_window(app)
                    log_history(command, response)

                elif "maximize" in command:
                    app = command.replace("maximize ", "").strip()
                    response = f"Maximizing {app}"
                    maximize_window(app)
                    log_history(command, response)

                elif "shutdown" in command:
                    response = "Shutting down the system"
                    shutdown_pc()
                    log_history(command, response)

                elif "restart" in command:
                    response = "Restarting the system"
                    restart_pc()
                    log_history(command, response)

                elif "sleep" in command:
                    response = "Putting system to sleep"
                    sleep_pc()
                    log_history(command, response)

                elif "show history" in command:
                    if verify_password():
                        show_history()
                        log_history(command, "History shown after correct password.")
                    else:
                        speak("Wrong password. Access denied.")
                        log_history(command, "Access denied due to wrong password.")

                elif "clear history" in command:
                    if verify_password():
                        clear_history()
                        speak("History cleared.")
                        log_history(command, "History cleared after correct password.")
                    else:
                        speak("Wrong password. Access denied.")
                        log_history(command, "Clear history blocked due to wrong password.")


                elif "current time" in command or "samay" in command:
                    now = datetime.datetime.now()
                    response = now.strftime("The current time is %I:%M %p.")
                    speak(response)
                    log_history(command, response)

                elif "date" in command or "aaj ki date" in command:
                    today = datetime.datetime.today()
                    response = today.strftime("Today's date is %A, %d %B %Y.")
                    speak(response)
                    log_history(command, response)

                elif any(word in command for word in ["ask", "what is","where", "create", "write", "who is", "explain", "how to", "make", "how", "when"]):
                    query = command.replace("ask", "").strip()
                    response = ask_gemini(query)
                    last_ai_response = response
                    print("AI response:", response)
                    log_history(command, response)

                elif "read it" in command or "read the answer" in command:
                    if last_ai_response:
                        speak(last_ai_response)
                        log_history(command, "Reading previous AI response.")
                    else:
                        response = "There is no response to read yet."
                        speak(response)
                        log_history(command, response)

                elif "download" in command or "save response" in command:
                    if last_ai_response:
                        save_response_to_pdf(last_ai_response)
                        log_history(command, "AI response saved as PDF.")
                    else:
                        response = "There is no response to save yet."
                        speak(response)
                        log_history(command, response)

                else:
                    response = "Sorry, I couldn't understand that. Please try again."
                    speak(response)
                    log_history(command, response)

            except sr.UnknownValueError:
                print("Sorry, I didn't understand.")
            except sr.RequestError:
                response = "Could not request results, check your internet connection."
                speak(response)
                log_history("RequestError", response)

# Speak text aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Gemini AI setup
GENAI_API_KEY = "AIzaSyDsA3rudK-vMfA4OkQXynU3BlsmHvrtgSE"
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

# App Controls
def open_application(app_name):
    speak(f"Opening {app_name}")
    os.system(f"start {app_name}")

def close_application(app_name):
    speak(f"Closing {app_name}")
    try:
        subprocess.run(f"taskkill /f /im {app_name}.exe", check=True, shell=True)
    except subprocess.CalledProcessError:
        speak(f"Could not close {app_name}. Make sure it is running.")

def get_window_by_name(app_name):
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd).lower()
            if app_name in window_text:
                extra.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

def minimize_window(app_name=None):
    if app_name:
        hwnd = get_window_by_name(app_name)
        if hwnd:
            speak(f"Minimizing {app_name}")
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        else:
            speak(f"Could not find {app_name} window")
    else:
        pyautogui.hotkey("win", "down")

def maximize_window(app_name=None):
    if app_name:
        hwnd = get_window_by_name(app_name)
        if hwnd:
            speak(f"Maximizing {app_name}")
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        else:
            speak(f"Could not find {app_name} window")
    else:
        pyautogui.hotkey("win", "up")

# System Controls
def shutdown_pc():
    speak("Shutting down the system")
    os.system("shutdown /s /t 5")

def restart_pc():
    speak("Restarting the system")
    os.system("shutdown /r /t 5")

def sleep_pc():
    speak("Putting system to sleep")
    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

# Date & Time
def get_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"The current time is {time_str}.")

def get_date():
    today = datetime.datetime.today()
    date_str = today.strftime("%A, %d %B %Y")
    speak(f"Today's date is {date_str}.")

# Search on Chrome
def search_on_chrome(query):
    speak(f"Searching for {query} on Chrome")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Save AI response to PDF
def save_response_to_pdf(response_text):
    try:
        now = datetime.datetime.now()
        filename = now.strftime("AI_Response_%Y%m%d_%H%M%S.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in response_text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf.output(filename)
        speak(f"The response has been saved to {filename}")
    except Exception as e:
        speak("Sorry, I couldn't save the file.")
        print(f"Error saving PDF: {e}")

# Clear history file
def clear_history():
    try:
        open(HISTORY_FILE, "w").close()
        speak("History has been cleared.")
        print("History cleared.")
    except Exception as e:
        speak("Sorry, I couldn't clear the history.")
        print(f"Error clearing history: {e}")

# Start the assistant
while True:
    recognize_speech()