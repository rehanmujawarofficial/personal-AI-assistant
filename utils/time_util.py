
import datetime
from utils.tts import speak

def get_time():
    now = datetime.datetime.now()
    speak(now.strftime("The current time is %I:%M %p"))

def get_date():
    today = datetime.datetime.today()
    speak(today.strftime("Today's date is %A, %d %B %Y"))
