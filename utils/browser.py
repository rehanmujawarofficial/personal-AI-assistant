
import webbrowser
from utils.tts import speak

def search_on_chrome(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching for {query} on Chrome")
