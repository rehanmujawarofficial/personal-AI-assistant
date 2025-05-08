
import os
from utils.tts import speak

def shutdown_pc():
    speak("Shutting down")
    os.system("shutdown /s /t 5")

def restart_pc():
    speak("Restarting")
    os.system("shutdown /r /t 5")

def sleep_pc():
    speak("Sleeping now")
    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
