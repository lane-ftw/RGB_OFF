import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32api
import subprocess
import socket
import time

# Define structures
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]

class POWERBROADCAST_SETTING(ctypes.Structure):
    _fields_ = [
        ("PowerSetting", GUID),
        ("DataLength", ctypes.wintypes.DWORD),
        ("Data", ctypes.c_ubyte * 1), 
    ]

# GUID for Console Display State (monitor on/off)
GUID_CONSOLE_DISPLAY_STATE = GUID(
    0x6FE69556, 0x704A, 0x47A0, (ctypes.c_ubyte * 8)(0x8F, 0x24, 0xC2, 0x8D, 0x93, 0x6F, 0xDA, 0x47)
)

# Message identifier for monitor power state changes
PBT_POWERSETTINGCHANGE = 0x8013

# Define Windows API functions
RegisterPowerSettingNotification = ctypes.windll.user32.RegisterPowerSettingNotification
RegisterPowerSettingNotification.argtypes = [wintypes.HANDLE, ctypes.POINTER(GUID), wintypes.DWORD]
RegisterPowerSettingNotification.restype = wintypes.HANDLE

# Function to check if OpenRGB is responsive
def is_openrgb_responding():
    try:
        with socket.create_connection(("localhost", 6742), timeout=1):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# Function to wait for OpenRGB to be ready
def wait_for_openrgb():
    while not is_openrgb_responding():
        time.sleep(1)

# Function to apply the OpenRGB profile
def set_openrgb_profile(profile):
    wait_for_openrgb()
    command = [r"C:\path\to\OpenRGB.exe", "--profile", f"{profile}.orp"]
    result = subprocess.run(command, capture_output=True, text=True)

# Window to handle power events
def window_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_POWERBROADCAST and wparam == PBT_POWERSETTINGCHANGE:
        power_setting = ctypes.cast(lparam, ctypes.POINTER(POWERBROADCAST_SETTING)).contents

        # Compare GUID with GUID_CONSOLE_DISPLAY_STATE
        if (power_setting.PowerSetting.Data1 == GUID_CONSOLE_DISPLAY_STATE.Data1 and 
            power_setting.PowerSetting.Data2 == GUID_CONSOLE_DISPLAY_STATE.Data2 and 
            power_setting.PowerSetting.Data3 == GUID_CONSOLE_DISPLAY_STATE.Data3 and 
            bytes(power_setting.PowerSetting.Data4) == bytes(GUID_CONSOLE_DISPLAY_STATE.Data4)):

            if power_setting.Data[0] == 1:
                set_openrgb_profile("on")  # Trigger when the screen is on
            elif power_setting.Data[0] == 0:
                set_openrgb_profile("off")  # Trigger when the screen is off

    return 0  # Ensures a valid LRESULT is always returned

# Function to create a hidden window to listen for display events
def listen_for_display_events():
    hinst = win32api.GetModuleHandle(None)
    wnd_class = win32gui.WNDCLASS()
    wnd_class.lpfnWndProc = window_proc
    wnd_class.hInstance = hinst
    wnd_class.lpszClassName = "HiddenMonitorListener"

    class_atom = win32gui.RegisterClass(wnd_class)
    hwnd = win32gui.CreateWindow(class_atom, "HiddenWindow", 0, 0, 0, 0, 0, 0, None, None, None)

    RegisterPowerSettingNotification(hwnd, ctypes.byref(GUID_CONSOLE_DISPLAY_STATE), win32con.DEVICE_NOTIFY_WINDOW_HANDLE)

    win32gui.PumpMessages()  # Start the message loop

if __name__ == "__main__":
    listen_for_display_events()
