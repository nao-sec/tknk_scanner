import ctypes.wintypes
import random, time

User32 = ctypes.WinDLL('User32.dll')
GetSystemMetrics = User32.GetSystemMetrics

RESOLUTION = {
    "x": User32.GetSystemMetrics(0),
    "y": User32.GetSystemMetrics(1)
}

def move_mouse():
    x = random.randint(0, RESOLUTION["x"])
    y = random.randint(0, RESOLUTION["y"])

    User32.SetCursorPos(x, y)

while(1):
    move_mouse()
    time.sleep(0.1)

