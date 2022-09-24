# Touch commands

def tap(x:float, y:float):
    return f"adb shell input tap {x} {y}"

def swipe(x1:float, y1:float, x2:float, y2:float, duration:int=None):
    if duration == None:
        return f"adb shell input swipe {x1} {y1} {x2} {y2} 1000"
    else:
        return f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"

def dragAndDrop(x1:float, y1:float, x2:float, y2:float, duration:int):
    return f"adb shell input draganddrop {x1} {y1} {x2} {y2} {duration}"

# System commands

def openApp(app:str):
    return f"adb shell monkey -p {app} -v 1"
