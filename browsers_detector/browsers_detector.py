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
        image = cv2.imread(f"{directory}data/screenshots/screen_shot.JPG")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = imutils.auto_canny(image)
        return image
    except cv2.error:
        print("Make sure you have 'data/screenshots' folder")
        return None
    return image


def load_template(image):
    try:
        template = cv2.imread(f"{directory}/data/templates/{image}", 0)
        template = imutils.auto_canny(template)
    except cv2.error:
        print("Input one of the names in the 'data/templates' folder in order to detect")
        return None
    return template


def start_scaling_match(template, screen_shot, scale="u", threshold=.40):
    template_height, template_width = template.shape[:2]
    found = None
    next_image = False
    resized = None
    for each_scale in np.linspace(0.2, 1.0, 20)[::-1]:
        if scale == "u":
            resized = imutils.resize(screen_shot, width=int(screen_shot.shape[1] * each_scale))
        elif scale == "d":
            resized = imutils.resize(screen_shot, width=int(screen_shot.shape[1] / each_scale))
        else:
            print("Please use 'scl=u' for scaling up or 'scl=d' for scaling down.")
            return resized is None
        r = screen_shot.shape[1] / float(resized.shape[1])
        if resized.shape[0] < template_height or resized.shape[1] < template_width:
            break
        result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + template_width) * r), int((maxLoc[1] + template_height) * r))
        # print(maxVal)
        # cv2.rectangle(screen_shot, (startX, startY), (endX, endY), (255, 0, 0), 4)
        # cv2.imshow("Image", screen_shot)
        # cv2.waitKey(0)
        if maxVal <= threshold:
            next_image = True
            # print("the value is less than the threshold")
            return 0, 0, next_image
        return ((startX + endX) / 2), ((startY + endY) / 2), next_image


def process(template, scale):
    x, y, next_image = start_scaling_match(load_template(template), grab_screen(), scale)
    return x, y, next_image


def auto_detect_taskbar():
    browsers = [
        "chrome_taskbar.JPG",
        "opera_taskbar.JPG",
        "firefox_taskbar.JPG",
        "edge_taskbar.JPG"
    ]

    value = None

    for browser in browsers:
        x, y, next_img = process(browser, "d")
        if next_img is False:
            moveTo(x, y)
            value = True
            return value
        elif next_img is True:
            x, y, next_img = process(browser, "u")
            if next_img is False:
                moveTo(x, y)
                value = True
                return value
    if value is None:
        return False


def auto_detect_desktop():
    browsers = [
        "chrome_desktop.JPG",
        "opera_desktop.JPG",
        "firefox_desktop.JPG",
        "edge_desktop.JPG"
    ]
    value = None

    for browser in browsers:
        x, y, next_img = process(browser, "d")
        if next_img is False:
            moveTo(x, y, duration=1)
            value = True
            return value
        elif next_img is True:
            x, y, next_img = process(browser, "u")
            if next_img is False:
                moveTo(x, y)
                value = True
                return value
    if value is None:
        return False


def detect_taskbar(browser):
    browser = browser.lower()
    browsers = {
        "edge": "edge_taskbar.JPG",
        "opera": "opera_taskbar.JPG",
        "firefox": "firefox_taskbar.JPG",
        "chrome": "chrome_taskbar.JPG"
    }
    value = None
    for key in browsers:
        if browser == key:
            x, y, next_img = process(browsers[key], "d")
            if next_img is False:
                moveTo(x, y)
                value = True
                return value
            elif next_img is True:
                x, y, next_img = process(browsers[key], "u")
                if next_img is False:
                    moveTo(x, y)
                    value = True
                    return value
    if value is None:
        return False


def detect_desktop(browser):
    browser = browser.lower()
    browsers = {
        "edge": "edge_desktop.JPG",
        "opera": "opera_desktop.JPG",
        "firefox": "firefox_desktop.JPG",
        "chrome": "chrome_desktop.JPG"
    }
    value = None
    for key in browsers:
        if browser == key:
            x, y, next_img = process(browsers[key], "d")
            if next_img is False:
                moveTo(x, y)
                value = True
                return value
            elif next_img is True:
                x, y, next_img = process(browsers[key], "u")
                if next_img is False:
                    moveTo(x, y)
                    value = True
                    return value
    if value is None:
        return False


def open_link(url):
    url = str(url)
    if url == "":
        return False
    else:
        sleep(.5)
        hotkey("win", "up")
        hotkey("ctrl", "l")
        typewrite("brockport.open.suny.edu")
        sleep(.5)
        press("enter")
        return True
