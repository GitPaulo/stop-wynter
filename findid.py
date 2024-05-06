import platform
import subprocess

os_name = platform.system()

def list_keyboard_ids_windows():
    output = subprocess.run(['devcon', 'status', '=keyboard'], capture_output=True, text=True)
    print("Windows Keyboard Device IDs (full details):")
    print(output.stdout)
    print("You're going to want to look at events and see which one was last used probably.")

def list_keyboard_ids_macos():
    output = subprocess.run(['ioreg', '-l'], capture_output=True, text=True)
    print("macOS Keyboard Device IDs:")
    for line in output.stdout.splitlines():
        if 'AppleUSBKeyboard' in line:
            print(line)

def list_keyboard_ids_linux():
    output = subprocess.run(['xinput', 'list'], capture_output=True, text=True)
    print("Linux Keyboard Device IDs:")
    for line in output.stdout.splitlines():
        if 'keyboard' in line.lower():
            print(line)

try:
  if os_name == 'Windows':
        list_keyboard_ids_windows()
  elif os_name == 'Darwin':
        list_keyboard_ids_macos()
  elif os_name == 'Linux':
        list_keyboard_ids_linux()
  else:
    print(f"Unsupported OS: {os_name}")
except Exception as e:
    print(f"Error ({os_name}) listing keyboard IDs: {e}")
