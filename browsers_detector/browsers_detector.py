import cv2
import imutils
import numpy as np
from pyautogui import *
from time import sleep
from pathlib import Path
from os import path

directory = path.join(path.dirname(__file__))
directory = Path(__file__).parent


def grab_screen():
    try:
        screenshot(f"{directory}/data/screenshots/screen_shot.JPG")
        image = cv2.imread(f"{directory}/data/screenshots/screen_shot.JPG")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = imutils.auto_canny(image)
        return image
    except cv2.error:
        print("Make sure you have 'data/screenshots' folder")
        return None
    return image


def load_template(image, load_type):
    try:
        template = cv2.imread(f"{directory}/data/templates/{image}", load_type)
        template = imutils.auto_canny(template)
    except cv2.error:
        print("Input one of the names in the 'data/templates' folder in order to detect")
        return None
    return template


def start_scaling_match(template, screen_shot, threshold=.35):
    template_height, template_width = template.shape[:2]
    found = None
    next_image = False
    for each_scale in np.linspace(0.1, 1.0, 20)[::-1]:
        resized = imutils.resize(screen_shot, width=int(screen_shot.shape[1] * each_scale))
        r = screen_shot.shape[1] / float(resized.shape[1])
        if resized.shape[0] < template_height or resized.shape[1] < template_width:
            break
        result = cv2.matchTemplate(resized, template, cv2.TM_CCORR_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + template_width) * r), int((maxLoc[1] + template_height) * r))
        print(maxVal)
        # cv2.rectangle(screen_shot, (startX, startY), (endX, endY), (255, 0, 0), 4)
        # cv2.imshow("Image", screen_shot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if maxVal <= threshold:
            for another_scale in np.linspace(0.1, 1.0, 20)[::-1]:
                resized = imutils.resize(screen_shot, width=int(screen_shot.shape[1] / another_scale))
                r = screen_shot.shape[1] * float(resized.shape[1])
                # if resized.shape[0] > template_height or resized.shape[1] > template_width:
                #     break
                result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
                if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)
                (_, maxLoc, r) = found
                (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
                (endX, endY) = (int((maxLoc[0] + template_width) * r), int((maxLoc[1] + template_height) * r))
                print(maxVal)
                # cv2.rectangle(screen_shot, (startX, startY), (endX, endY), (255, 0, 0), 4)
                # cv2.imshow("Image", screen_shot)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                if maxVal <= threshold:
                    next_image = True
                    return 0, 0, next_image
                return ((startX + endX) / 2), ((startY + endY) / 2), next_image
        return ((startX + endX) / 2), ((startY + endY) / 2), next_image


def process(template, th=.30):
    x, y, next_image = start_scaling_match(load_template(template, 0), grab_screen(), th)
    return x, y, next_image


def auto_detect():
    if auto_detect_taskbar():
        return True
    elif auto_detect_desktop() is False:
        hotkey("win", "d")
    elif auto_detect_desktop():
        return True
    else:
        return False


def auto_detect_taskbar():
    browsers = [
        "chrome_taskbar.JPG",
        "opera_taskbar.JPG",
        "firefox_taskbar.JPG",
        "edge_taskbar.JPG"
    ]

    for browser in browsers:
        x, y, next_img = process(browser)
        if next_img is False:
            moveTo(x, y)
            return True
        else:
            return False


def auto_detect_desktop():
    browsers = [
        "chrome_desktop.JPG",
        "opera_desktop.JPG",
        "firefox_desktop.JPG",
        "edge_desktop.JPG"
    ]

    for browser in browsers:
        x, y, next_img = process(browser)
        if next_img is False:
            moveTo(x, y, duration=1)
            return True
        else:
            return False


def detect_taskbar(browser):
    browser = browser.lower()
    browsers = {
        "edge": "edge_taskbar.JPG",
        "opera": "opera_taskbar.JPG",
        "firefox": "firefox_taskbar.JPG",
        "chrome": "chrome_taskbar.JPG"
    }

    for key in browsers:
        if browser == key:
            x, y, next_img = process(browsers[key], .30)
            if next_img is False:
                moveTo(x, y)
                return True
            else:
                return False


def detect_desktop(browser):
    browser = browser.lower()
    browsers = {
        "edge": "edge_desktop.JPG",
        "opera": "opera_desktop.JPG",
        "firefox": "firefox_desktop.JPG",
        "chrome": "chrome_desktop.JPG"
    }
    for key in browsers:
        if browser == key:
            x, y, next_img = process(browsers[key], .40)
            if next_img is False:
                moveTo(x, y)
                return True
            else:
                return False


def open_link(url):
    url = str(url)
    if url == "":
        return False
    else:
        sleep(1)
        hotkey("win", "up")
        hotkey("ctrl", "l")
        typewrite(url)
        sleep(1)
        press("enter")
        sleep(6)
        press("tab")
        sleep(1)
        press("enter")
        return True


def open_with_start(url):
    if url == "":
        return False
    else:
        sleep(.5)
        press("win")
        typewrite(url)
        press("enter")
        sleep(1)
        hotkey("win", "up")
        hotkey("ctrl", "l")
        sleep(4)
        press("tab")
        sleep(1)
        press("enter")
        return True


def send_email(message, title=""):
    sleep(9)
    hotkey("alt", "shift", "m")
    sleep(1)
    press("tab", 5, .1)
    sleep(1)
    press("enter")
    sleep(2)
    press("tab", 10, .1)
    sleep(1)
    press("enter")
    sleep(2)
    press("tab", 27, .1)
    press("enter")
    sleep(2)
    typewrite(title)
    sleep(1)
    press('tab', 2, .1)
    sleep(1)
    typewrite(message)
    sleep(1)
    press("tab", 4, .1)
    # press("enter")
