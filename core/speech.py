
import speech_recognition as sr
from config import WAKE_WORD
from utils.tts import speak
from core.commands import execute_commands

def recognize_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            if WAKE_WORD in command:
                speak("Hello sir! How can I help you today?")
                execute_commands()
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError:
            print("Speech recognition service unavailable.")
