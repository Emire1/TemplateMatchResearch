# Template Match Research

The main purpose of this project is to create a lightweight script that can detect browsers on a user's screen. The browsers to be detected are chrome, firefox, edge, and opera. This project will serve as an API to detect the browsers. The project utilizes the [OpenCV library](https://docs.opencv.org/master/) with the help of [Adrian Rosebrock's](https://github.com/jrosebr1) [imutils library](https://github.com/jrosebr1/imutils) and his [template matching optimization](https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/).

## Installation

Use the [pip](https://pip.pypa.io/en/stable/) package manager to install the script.

```bash
pip install templateMatchResearch
```
or 

```bash
git clone https://github.com/emire1/TemplateMatchResearch
```

## Usage

```python
from browsers_detector import *

auto_detect_taskbar() # returns True if a browser is detected
detect_desktop("chrome") # moves mouse to location of browser and return True if browser is detected
detect_taskbar("opera") # moves mouse to location of browser and return True if browser is detected
```

## Logging into BlackBoard with browser_detector

```python
# This automatically detects any browser on the desktop
# to open it and go to the blackboard link.
from object_detection import *
import pyautogui
from time import sleep
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
```

## Updates
This is still a continuing project and will be updated most times, unfortunately, this is only tested on windows operating system as of now

## The Functions

### grab_screen(): 
> #### This function takes a screenshot and saves it into the "data/screenshots" folder and it is saved as "screen_shot.JPG". This will also convert the image into grayscale, detect the edges of the image and return it for detection.
```python
grab_screen() 
# returns image
```

### load_template(image): 
> *image* = name of any file located in the "data/templates" folder

> #### This function takes an image file from the "templates" folder, read it as grayscale, detect the edges and return it for detection. If there is an error None is returned.
```python
load_template("chrome_taskbar.JPG") 
# returns template or None if there is an error
```

### start_scaling_match(template, screen_shot, scale, threshold):
>  *template* = the return value from the load_template() method.
 
>  *screen_shot* = The return value from the grab_screen() method.

>  *scale* = the default value is "u" meaning scale up and it could be changed to "d" to scale down. This is used to determine if the main image should be scaled up during the detection process. 

>  *threshold* = the threshold determines whether the image is detected or not. The default value is .30
 
> #### This function takes in the template object, screen_shot object, a scale value, and a threshold. This function adopts a [template matching algorithm](https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/) which optimize the template-matching function from the [OpenCV library](https://docs.opencv.org/master/). The algorithm is basically scaling either up or down while applying the template-matching function and comparing the value of the match to the threshold until the value is greater than or equal to the threshold then the location or coordinates (x, y) of the match is returned with a boolean(next_image) value of False. If the value is less than the threshold then the location would be (0,0) with a next_image boolean of True. the next_image is used to determine if a different image should be used to detect a browser.

```python
template = load_template("chrome_desktop.JPG")
screen_shot = grab_screen()
start_scaling_match(template, screen_shot, "d", .75)
# if image is found returns x, y, next_image=False else return 0, 0, next_image=True
# or
# it could be called like:
start_scaling_match(load_template("chrome_taskbar.JPG"), grab_screen(), "d", .50) 
```

### process(template, scale):
>  *template* = the actual file name of the browser
 
>  *scale* = the default value is "u" meaning scale up and it could be changed to "d" to scale down. This is used to determine if the main image should be scaled up during the detection process. 

 
> #### This function calls the load_template(), grab_screen(), and start_scaling_match() combine them together to gain the absolute position of the match on the screen and a boolean value. It takes in a template object and a scale value to determine whether the image should be scale up or down during the matching process.

```python
process("chrome_taskbar.JPG", "u")
# returns x, y of match and next_image=False if a match is found.
```

### auto_detect_taskbar(): 
> #### This function will automatically detect any of the browsers on the Windows taskbar. If a match is found the mouse pointer would be moved to the location of the match and a boolean value of True is returned. If there is no match False is returned.
```python
auto_detect_taskbar() 
# returns True if the match is found and False if the match is not found
```

### auto_detect_desktop(): 
> #### This function will automatically detect any of the browsers on the Windows desktop. If a match is found the mouse pointer would be moved to the location of the match and a boolean value of True is returned. If there is no match False is returned.
```python
auto_detect_taskbar() 
# returns True if the match is found and False if the match is not found
```

### detect_taskbar(browser): 
> *browser* = name of any of the browsers (chrome, opera, edge, firefox)

> #### This function will try to detect the browser on the Windows taskbar and if it is found it will return True and move the mouse pointer to the location of the match. If no match was found it will return False.
```python
detect_taskbar("chrome") 
# returns True if a match is found and False if there were no matches.
```

### detect_desktop(browser): 
> *browser* = name of any of the browsers (chrome, opera, edge, firefox)

> #### This function will try to detect the browser on the Windows desktop and if it is found it will return True and move the mouse pointer to the location of the match. If no match was found it will return False.
```python
detect_desktop("firefox") 
# returns True if a match is found and False if there were no matches.
```

### open_link(url): 
> *url* = the actual url to be typed into the browser

> #### This function types in the link automatically in the browser and  goes to the url. If the url is empty it returns false and returns True otherwise.
```python
open_link("brockport.edu") 
# returns False if url is empty and returns True if the url is not empty
```

### open_with_start(url): 
> *url* = the actual url to be typed into the browser

> #### This function types in the link automatically in the start menu and  it will open the url with the default browser of the system. If the url is empty it returns false and returns True otherwise.
```python
open_with_start("suny.brockport.edu") 
# returns False if url is empty and returns True if the url is not empty
```

### send_email(message, heading): 
> *message* = the message to be sent
> *title* = the title of the message. the default value is "" or an empty string

> #### This function attempts to send an email after a user is logged into their blackboard account
```python
send_email("Hello World!", "Hello!") 
```
