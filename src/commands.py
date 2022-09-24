import os
from datetime import datetime

# Touch commands

def tap(x:float, y:float):
    return f"shell input tap {x} {y}"

def swipe(x1:float, y1:float, x2:float, y2:float, duration:int=None):
    if duration == None:
        return f"shell input swipe {x1} {y1} {x2} {y2} 1000"
    else:
        return f"shell input swipe {x1} {y1} {x2} {y2} {duration}"

def dragAndDrop(x1:float, y1:float, x2:float, y2:float, duration:int):
    return f"shell input draganddrop {x1} {y1} {x2} {y2} {duration}"

# System commands

def openApp(app:str):
    return f"shell monkey -p {app} -v 1"

# Verification commands

def captureImage():
    imageName = f"{datetime.now().day}{datetime.now().month}{datetime.now().year}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}"
    return f"shell screencap /sdcard/{imageName}.png"

def getImage(image_name:str, result_folder:str):
    return f"pull /sdcard/{image_name} {result_folder}"

