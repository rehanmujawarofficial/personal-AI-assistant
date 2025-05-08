
import os
import subprocess
import pyautogui
import win32gui
import win32con
from utils.tts import speak

def open_application(app_name):
    speak(f"Opening {app_name}")
    os.system(f"start {app_name}")

def close_application(app_name):
    try:
        subprocess.run(f"taskkill /f /im {app_name}.exe", check=True, shell=True)
        speak(f"Closed {app_name}")
    except subprocess.CalledProcessError:
        speak(f"Failed to close {app_name}")

def get_window_by_name(app_name):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and app_name in win32gui.GetWindowText(hwnd).lower():
            windows.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

def minimize_window(app_name):
    hwnd = get_window_by_name(app_name)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def maximize_window(app_name):
    hwnd = get_window_by_name(app_name)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
