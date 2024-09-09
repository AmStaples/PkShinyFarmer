import pyautogui
import pyscreeze
import PIL
import numpy
import pynput
from pynput.keyboard import Key, Controller
import time
import ctypes
from ctypes import wintypes
import random
import sys
import ctypes

user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def a():
    PressKey(0x41)
    time.sleep(0.5)
    ReleaseKey(0x41)
def d():
    PressKey(0x44)
    time.sleep(0.5)
    ReleaseKey(0x44)
def leftclick():
    PressKey(0x01)
    time.sleep(0.1)
    ReleaseKey(0x01)
    # you can change 0x30 to any key you want. For more info look at :
    # msdn.microsoft.com/en-us/library/dd375731


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

i = 1
while i < 6:
    try:
        x, b = pyautogui.locateCenterOnScreen('C:\Assignments\\shinx.png', confidence=0.8)
    except:
        a()
        d()

    else:
        sys.exit
        i = 7
        

    try:
        c, y = pyautogui.locateCenterOnScreen('C:\Assignments\\run.png', confidence=0.99)
    except:
        print()
    else:
        pyautogui.leftClick(x=c, y=y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
Mbox('CONGRATULATIONS!', 'SHINX FOUND!', 1)