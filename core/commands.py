import datetime
import speech_recognition as sr

from core.ai import ask_gemini
from core.history import log_history, show_history, clear_history
from core.password import verify_password
from utils.tts import speak
from utils.time_util import get_time, get_date
from utils.system_control import shutdown_pc, restart_pc, sleep_pc
from utils.browser import search_on_chrome
from utils.app_control import open_application, close_application, minimize_window, maximize_window
from utils.pdf_exporter import save_response_to_pdf

def execute_commands():
    recognizer = sr.Recognizer()
    last_ai_response = ""

    with sr.Microphone() as source:
        while True:
            print("What can I do for you sir?")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")
                response = ""

                if "bye" in command:
                    response = "Assistant stopped .if you want any help, i am hear just call me with bro"
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

                elif "minimize" in command:
                    app = command.replace("minimize ", "").strip()
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

                elif "show my history" in command:
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

                elif "current time" in command:
                    now = datetime.datetime.now()
                    response = now.strftime("The current time is %I:%M %p.")
                    speak(response)
                    log_history(command, response)

                elif "date" in command:
                    today = datetime.datetime.today()
                    response = today.strftime("Today's date is %A, %d %B %Y.")
                    speak(response)
                    log_history(command, response)

                elif any(word in command for word in ["ask", "what is", "where", "create", "write", "who is", "explain", "how to", "make", "how", "when"]):
                    query = command.replace("ask", "").strip()
                    response = ask_gemini(query)
                    last_ai_response = response
                    print("AI response:", response)
                    log_history(command, response)

                elif "read it" in command:
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
