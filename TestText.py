import ctypes as ct
import ctypes.wintypes as w
import time
import keyboard
KEYEVENTF_SCANCODE = 0x8
KEYEVENTF_UNICODE = 0x4 #
KEYEVENTF_KEYUP = 0x2 #
SPACE = 0x1E
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



def zerocheck(result, func, args):
    if result == 0:
        raise ct.WinError(ct.get_last_error())
    return result

user32 = ct.WinDLL('user32', use_last_error=True)
SendInput = user32.SendInput
SendInput.argtypes = w.UINT, ct.POINTER(INPUT), ct.c_int
SendInput.restype = w.UINT
SendInput.errcheck = zerocheck

def send_scancode(code, sleeptime):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0, code, KEYEVENTF_SCANCODE, 0, 0)
    SendInput(1, ct.byref(i), ct.sizeof(INPUT))
    time.sleep(sleeptime)
    i.ki.dwFlags |= KEYEVENTF_KEYUP
    SendInput(1, ct.byref(i), ct.sizeof(INPUT))

def press_key(Scancode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=Scancode))
    SendInput(1, ct.byref(x), ct.sizeof(x))

def release_key(Scancode) :
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=Scancode,
                            dwFlags=KEYEVENTF_KEYUP))
    SendInput(1, ct.byref(x), ct.sizeof(x))

def key_input(code, sleeptime) :
    press_key(code)
    time.sleep(sleeptime)
    release_key(code)
send_scancode(SPACE, 2)
#key_input(SPACE, 2)


"""
import ctypes
import ctypes.wintypes as w
import functools
import inspect
import time

SPACE = 0x39E

#Think about this like defining Variables
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [('uVk', w.DWORD),
                ('wScan', w.DWORD),
                ('dwFlags', w.DWORD),
                ('time', w.DWORD),
                ('dwExtraInfo', w.DWORD)]
# ctypes.Structure is an object that stores 2 to 3 tuple items. 
# First being the name and second being the type of variable
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [('uMsg', w.DWORD),
                ('wParamL', w.WORD), #When in rome do as the romans do
                ('wParamH', w.WORD)]
    
class DUMMYUNIONNAME(ctypes.Union):
    _fields_ = [('hi', HARDWAREINPUT),
                ('ki', KEYBDINPUT)]
class INPUT(ctypes.Structure):
    _anonymous_ = ['u']
    _fields_ = [('type', w.DWORD),
                ('u', DUMMYUNIONNAME)]
print(ctypes.sizeof(INPUT))
size = ctypes.sizeof(INPUT)
print(size)
def zerocheck(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error()) #WinError grabs the Windows API to get the
    return result #string representation of an error code and return an exception
user32 = ctypes.WinDLL('user32', use_last_error=True)

SendInput = ctypes.windll.user32.SendInput #Ties Windows/C SendInput to py variable SendInput
SendInput.argtypes = [w.UINT, ctypes.POINTER(INPUT), ctypes.c_int] #Set what arguments Sendinput can handle
SendInput.restype = w.UINT #specify the return type
#SendInput.errcheck = zerocheck #Specify error check

INPUT_KEYBOARD = 1
KEYEVENTF_SCANCODE = 0x8E
KEYEVENTF_KEYUP = 0x2E

def send_scancode(code):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0, code, KEYEVENTF_SCANCODE, 0, 0)
    SendInput(1, ctypes.byref(i), (ctypes.sizeof(INPUT)))
    i.ki.dwFlags |= KEYEVENTF_KEYUP
    SendInput(1, ctypes.byref(i), (ctypes.sizeof(INPUT)))
    print("Sent")

send_scancode(SPACE)
"""
