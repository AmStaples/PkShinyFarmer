import ctypes as ct
import ctypes.wintypes as w
import time
import keyboard

SPACE = 0x020

#Add more buttons using the Scancode Column in this spreadsheet
# Name it whatever you need to. SCO39 converts to 0x39E
# https://docs.google.com/spreadsheets/d/1GSj0gKDxyWAecB3SIyEZ2ssPETZkkxn67gdIwL1zFUs/edit?gid=0#gid=0
KEYEVENTF_SCANCODE = 0x8
KEYEVENTF_UNICODE = 0x4 
KEYEVENTF_KEYUP = 0x2 
INPUT_KEYBOARD = 1
# not defined by wintypes
ULONG_PTR = ct.c_size_t
# ctypes.Structure is an object that stores 2 to 3 tuple items. 
# First being the name and second being the type of variable
class KEYBDINPUT(ct.Structure):
    _fields_ = [('wVk' , w.WORD),
                ('wScan', w.WORD),
                ('dwFlags', w.DWORD),
                ('time', w.DWORD),
                ('dwExtraInfo', ULONG_PTR)]

class MOUSEINPUT(ct.Structure):
    _fields_ = [('dx' , w.LONG),
                ('dy', w.LONG),
                ('mouseData', w.DWORD),
                ('dwFlags', w.DWORD),
                ('time', w.DWORD),
                ('dwExtraInfo', ULONG_PTR)]

class HARDWAREINPUT(ct.Structure):
    _fields_ = [('uMsg' , w.DWORD),
                ('wParamL', w.WORD),
                ('wParamH', w.WORD)]

class DUMMYUNIONNAME(ct.Union):
    _fields_ = [('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT)]

class INPUT(ct.Structure):
    _anonymous_ = ['u']
    _fields_ = [('type', w.DWORD),
                ('u', DUMMYUNIONNAME)]



def zerocheck(result, func, args): #Function calls the Windows API if something breaks and returns exception
    if result == 0:
        raise ct.WinError(ct.get_last_error())
    return result

user32 = ct.WinDLL('user32', use_last_error=True)
SendInput = user32.SendInput
SendInput.argtypes = w.UINT, ct.POINTER(INPUT), ct.c_int
SendInput.restype = w.UINT
SendInput.errcheck = zerocheck

def send_scancode(code, sleeptime):
    timer = sleeptime
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0, code, KEYEVENTF_SCANCODE, 0, 0)
    while (timer >= 0):
        SendInput(1, ct.byref(i), ct.sizeof(INPUT))
        time.sleep(0.025)
        timer = timer - 0.025
        print(timer)
        if keyboard.is_pressed('e'): #Escape figured out.
            break

    i.ki.dwFlags |= KEYEVENTF_KEYUP
    SendInput(1, ct.byref(i), ct.sizeof(INPUT))

send_scancode(SPACE, 1)