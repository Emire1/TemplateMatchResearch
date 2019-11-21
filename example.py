from browsers_detector import *
import pyautogui


detection = auto_detect_desktop()
if detection is False:
    pyautogui.hotkey("win", "d")
    detection = auto_detect_desktop()
    if detection is False:
        print()
    else:
        open_link("brockport.edu")
else:
    open_link("brockport.edu")


