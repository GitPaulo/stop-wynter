from pynput import keyboard
import time
import platform
import subprocess
import threading
import tkinter as tk
import configparser
from tkinter import messagebox

TIME_WINDOW = 0.5  # Time window to detect burst of key presses (in seconds)
MAX_KEYS = 10 # Number of simultaneous key presses to trigger the lock

recent_keypresses = []
keyboard_disabled = False
os_name = platform.system()

config = configparser.ConfigParser()
config.read('config.ini')
try:
    keyboard_device_id = config['Keyboard']['DeviceID'] # edit in config.ini
    print(f"Keyboard Device ID: {keyboard_device_id}")
except KeyError:
    print("Could not find the DeviceID in the config file.")


def disable_keyboard_windows():
    subprocess.run(['devcon', 'disable', keyboard_device_id], check=True)

def enable_keyboard_windows():
    subprocess.run(['devcon', 'enable', keyboard_device_id], check=True)

def disable_keyboard_macos():
    print("TODO")

def enable_keyboard_macos():
    print("TODO")

def disable_keyboard_linux():
    subprocess.run(['xinput', 'set-prop', keyboard_device_id, 'Device Enabled', '0'], check=True)

def enable_keyboard_linux():
    subprocess.run(['xinput', 'set-prop', keyboard_device_id, 'Device Enabled', '1'], check=True)

def reenable_keyboard_via_gui():
    def on_enable():
        global keyboard_disabled
        keyboard_disabled = False
        print("Keyboard re-enabled")
        if os_name == 'Windows':
            enable_keyboard_windows()
        elif os_name == 'Darwin':
            enable_keyboard_macos()
        elif os_name == 'Linux':
            enable_keyboard_linux()
        else:
            print(f"Unsupported OS: {os_name}")
        root.destroy()

    root = tk.Tk()
    root.title("Keyboard Disabled")
    tk.Label(root, text="Keyboard has been disabled due to suspicious activity.").pack(pady=10)
    tk.Button(root, text="Enable Keyboard", command=on_enable).pack(pady=10)
    root.mainloop()

def on_press(key):
    global keyboard_disabled, recent_keypresses

    if keyboard_disabled:
        return

    current_time = time.time()
    recent_keypresses.append(current_time)
    recent_keypresses = [kp for kp in recent_keypresses if current_time - kp < TIME_WINDOW]

    if len(recent_keypresses) >= MAX_KEYS:
        print("Sus activity detected, attempting to disable keyboard...")
        try:
            if os_name == 'Windows':
                disable_keyboard_windows()
            elif os_name == 'Darwin':
                disable_keyboard_macos()
            elif os_name == 'Linux':
                disable_keyboard_linux()
            else:
                print(f"Unsupported OS: {os_name}")
                return 
            keyboard_disabled = True
        except Exception as e:
            print(f"Failed to disable keyboard: {e}")
        threading.Thread(target=reenable_keyboard_via_gui).start()

def on_release(key):
    pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
