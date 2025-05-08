
import speech_recognition as sr
from utils.tts import speak
from config import VOICE_PASSWORD

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
