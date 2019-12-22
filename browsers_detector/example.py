from browsers_detector import *
from pyautogui import *
from time import *

url = "brockport.open.suny.edu"
message = "This is just a test so don't panic!"
detection = auto_detect_desktop()
if detection is False:
    # pyautogui.hotkey("win", "d")
    detection = auto_detect_desktop()
    if detection is False:
        detection = auto_detect_taskbar()
        if detection is False:
            open_with_start(url)
            send_email(message)
        else:
            keyDown("shift")
            click()
            sleep(.3)
            keyUp("shift")
            hotkey("ctrl", "tab")
            open_link(url)
            send_email(message)
    else:
        doubleClick()
        open_link(url)
        send_email(message)
else:
    doubleClick()
    open_link(url)
    send_email(message)

# print("chrome****desktop")
# detect_desktop("chrome")
# sleep(2)
# print("firefox****desktop")
# detect_desktop("firefox")
# sleep(2)
# print("edge*****desktop")
# detect_desktop("edge")
# sleep(2)
# print("opera*****desktop")
# detect_desktop("opera")
# sleep(2)
#
# print("chrome****taskbar")
# detect_taskbar("chrome")
# sleep(2)
# print("firefox****taskbar")
# detect_taskbar("firefox")
# sleep(2)
# print("edge*****taskbar")
# detect_taskbar("edge")
# sleep(2)
# print("opera*****taskbar")
# detect_taskbar("opera")
# sleep(2)
